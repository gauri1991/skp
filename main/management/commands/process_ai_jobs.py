"""Cron worker for async (video) AI generations.

Run every minute. Lockfile-guarded so overlapping cron fires are no-ops.
- queued  -> submit to the provider, store provider_job_id, mark running
- running -> poll; on success download the video into private storage,
             mark succeeded and notify the client; on failure record the error.
"""
import os

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils import timezone

from main.ai import AIProviderError, get_adapter
from main.models import AIGeneration, ClientNotification

LOCK_PATH = os.path.join(settings.BASE_DIR, '.ai_jobs.lock')
STALE_LOCK_SECONDS = 30 * 60
MAX_JOB_AGE_HOURS = 6  # give up on jobs stuck running longer than this


class Command(BaseCommand):
    help = 'Submit and poll queued/running async AI generations (video).'

    def handle(self, *args, **options):
        if not self._acquire_lock():
            self.stdout.write('Another run is active; exiting.')
            return
        try:
            self._submit_queued()
            self._poll_running()
        finally:
            self._release_lock()

    # ----- lock -----
    def _acquire_lock(self):
        try:
            fd = os.open(LOCK_PATH, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
            return True
        except FileExistsError:
            try:
                age = timezone.now().timestamp() - os.path.getmtime(LOCK_PATH)
                if age > STALE_LOCK_SECONDS:
                    os.unlink(LOCK_PATH)
                    return self._acquire_lock()
            except OSError:
                pass
            return False

    def _release_lock(self):
        try:
            os.unlink(LOCK_PATH)
        except OSError:
            pass

    # ----- work -----
    def _fail(self, generation, message):
        generation.status = 'failed'
        generation.error = message[:1000]
        generation.completed_at = timezone.now()
        generation.save(update_fields=['status', 'error', 'completed_at'])
        self.stdout.write(self.style.WARNING(f'#{generation.pk} failed: {message[:120]}'))

    def _submit_queued(self):
        for generation in AIGeneration.objects.filter(
                status='queued', feature__feature_type='video').select_related(
                'feature', 'feature__provider')[:10]:
            feature = generation.feature
            if feature is None or not feature.provider.is_active:
                self._fail(generation, 'Feature or provider no longer available.')
                continue
            try:
                adapter = get_adapter(feature.provider, feature.model_override or None)
                job_id = adapter.submit_video(generation.rendered_prompt, generation.inputs)
            except AIProviderError as exc:
                self._fail(generation, str(exc))
                continue
            except Exception as exc:
                self._fail(generation, f'Unexpected submit error: {exc}')
                continue
            generation.provider_job_id = job_id
            generation.status = 'running'
            generation.started_at = timezone.now()
            generation.save(update_fields=['provider_job_id', 'status', 'started_at'])
            self.stdout.write(f'#{generation.pk} submitted as {job_id}')

    def _poll_running(self):
        cutoff = timezone.now() - timezone.timedelta(hours=MAX_JOB_AGE_HOURS)
        for generation in AIGeneration.objects.filter(
                status='running', feature__feature_type='video').select_related(
                'feature', 'feature__provider')[:20]:
            if generation.started_at and generation.started_at < cutoff:
                self._fail(generation, 'Timed out waiting for the video provider.')
                continue
            feature = generation.feature
            if feature is None:
                self._fail(generation, 'Feature was deleted while the job ran.')
                continue
            try:
                adapter = get_adapter(feature.provider, feature.model_override or None)
                result = adapter.poll_video(generation.provider_job_id)
            except AIProviderError as exc:
                self._fail(generation, str(exc))
                continue
            except Exception as exc:
                self._fail(generation, f'Unexpected poll error: {exc}')
                continue

            if result.status == 'running':
                continue
            if result.status == 'failed':
                self._fail(generation, result.error or 'Provider reported failure.')
                continue

            # succeeded
            video_bytes = result.video_bytes
            if video_bytes is None and result.video_url:
                try:
                    video_bytes = adapter.download_video(result.video_url)
                except AIProviderError as exc:
                    self._fail(generation, str(exc))
                    continue
            if not video_bytes:
                self._fail(generation, 'Provider returned no video content.')
                continue

            generation.output_file.save(f'gen_{generation.pk}.mp4',
                                        ContentFile(video_bytes), save=False)
            generation.output_mime = 'video/mp4'
            generation.status = 'succeeded'
            generation.completed_at = timezone.now()
            generation.save()
            ClientNotification.objects.create(
                client=generation.client,
                title='Your AI video is ready',
                message=f'"{generation.feature_title}" finished generating. '
                        'Open AI Tools > History to view it.',
                notification_type='system',
            )
            self.stdout.write(self.style.SUCCESS(f'#{generation.pk} succeeded'))
