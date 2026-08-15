"""AI platform views: dashboard AI Studio (staff) + client AI workspace."""
import json
import mimetypes

from django.contrib import messages as flash
from django.core.files.base import ContentFile
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView, View,
)

from .ai import AIProviderError, get_adapter
from .forms import AIProviderForm, ServiceAIFeatureForm, build_feature_input_form
from .mixins import ClientRequiredMixin, StaffRequiredMixin
from .models import AIGeneration, AIProvider, Service, ServiceAIFeature

SAFE_IMAGE_TYPES = {'image/png', 'image/jpeg', 'image/webp', 'image/gif'}


# ================= Dashboard: AI Studio =================

class AIProviderListView(StaffRequiredMixin, ListView):
    model = AIProvider
    template_name = 'dashboard/ai/providers_list.html'
    context_object_name = 'providers'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'AI Providers'
        return ctx


class AIProviderCreateView(StaffRequiredMixin, CreateView):
    model = AIProvider
    form_class = AIProviderForm
    template_name = 'dashboard/ai/provider_form.html'
    success_url = reverse_lazy('dashboard_ai_providers')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Add AI Provider'
        return ctx

    def form_valid(self, form):
        flash.success(self.request, 'Provider saved.')
        return super().form_valid(form)


class AIProviderUpdateView(StaffRequiredMixin, UpdateView):
    model = AIProvider
    form_class = AIProviderForm
    template_name = 'dashboard/ai/provider_form.html'
    success_url = reverse_lazy('dashboard_ai_providers')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = f'Edit {self.object.name}'
        return ctx

    def form_valid(self, form):
        flash.success(self.request, 'Provider updated.')
        return super().form_valid(form)


class AIProviderDeleteView(StaffRequiredMixin, DeleteView):
    model = AIProvider
    template_name = 'dashboard/ai/provider_confirm_delete.html'
    success_url = reverse_lazy('dashboard_ai_providers')


class AIProviderTestView(StaffRequiredMixin, View):
    """AJAX 'Test connection' button."""

    def post(self, request, pk):
        provider = get_object_or_404(AIProvider, pk=pk)
        try:
            adapter = get_adapter(provider)
            message = adapter.test_connection()
            return JsonResponse({'success': True, 'message': message})
        except AIProviderError as exc:
            return JsonResponse({'success': False, 'error': str(exc)})
        except Exception as exc:  # defensive: never 500 the dashboard button
            return JsonResponse({'success': False, 'error': f'Unexpected error: {exc}'})


class AIFeatureListView(StaffRequiredMixin, ListView):
    model = ServiceAIFeature
    template_name = 'dashboard/ai/features_list.html'
    context_object_name = 'features'

    def get_queryset(self):
        return (ServiceAIFeature.objects
                .select_related('service', 'provider')
                .order_by('service__display_order', 'display_order'))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        services = {}
        for feature in ctx['features']:
            services.setdefault(feature.service, []).append(feature)
        ctx['features_by_service'] = services
        ctx['page_title'] = 'AI Features'
        return ctx


class AIFeatureCreateView(StaffRequiredMixin, CreateView):
    model = ServiceAIFeature
    form_class = ServiceAIFeatureForm
    template_name = 'dashboard/ai/feature_form.html'
    success_url = reverse_lazy('dashboard_ai_features')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Add AI Feature'
        return ctx

    def form_valid(self, form):
        flash.success(self.request, 'AI feature saved.')
        return super().form_valid(form)


class AIFeatureUpdateView(StaffRequiredMixin, UpdateView):
    model = ServiceAIFeature
    form_class = ServiceAIFeatureForm
    template_name = 'dashboard/ai/feature_form.html'
    success_url = reverse_lazy('dashboard_ai_features')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = f'Edit {self.object.title}'
        return ctx

    def form_valid(self, form):
        flash.success(self.request, 'AI feature updated.')
        return super().form_valid(form)


class AIFeatureDeleteView(StaffRequiredMixin, DeleteView):
    model = ServiceAIFeature
    template_name = 'dashboard/ai/feature_confirm_delete.html'
    success_url = reverse_lazy('dashboard_ai_features')


class AIGenerationLogView(StaffRequiredMixin, ListView):
    model = AIGeneration
    template_name = 'dashboard/ai/generations_list.html'
    context_object_name = 'generations'
    paginate_by = 25

    def get_queryset(self):
        qs = AIGeneration.objects.select_related('client', 'feature').order_by('-created_at')
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)
        client = self.request.GET.get('client')
        if client:
            qs = qs.filter(client__email__icontains=client)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['status_choices'] = AIGeneration.STATUS_CHOICES
        ctx['current_status'] = self.request.GET.get('status', '')
        ctx['client_q'] = self.request.GET.get('client', '')
        ctx['page_title'] = 'AI Generations'
        return ctx


# ================= Client: AI Workspace =================

def _quota_for(client_profile, feature):
    return client_profile.ai_daily_limit or feature.daily_limit_per_client


class ClientAIIndexView(ClientRequiredMixin, TemplateView):
    template_name = 'client/ai/index.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        services = (Service.objects.filter(is_active=True, ai_features__is_active=True,
                                           ai_features__provider__is_active=True)
                    .distinct().order_by('display_order'))
        ctx['services'] = services
        ctx['ai_enabled'] = self.request.user.client_profile.ai_enabled
        return ctx


class ClientAIServiceView(ClientRequiredMixin, TemplateView):
    template_name = 'client/ai/service_features.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        service = get_object_or_404(Service, slug=kwargs['service_slug'], is_active=True)
        features = (service.ai_features.filter(is_active=True, provider__is_active=True)
                    .select_related('provider'))
        profile = self.request.user.client_profile
        feature_data = []
        for feature in features:
            used = AIGeneration.used_today(self.request.user, feature)
            limit = _quota_for(profile, feature)
            feature_data.append({
                'feature': feature,
                'form': build_feature_input_form(feature),
                'used': used, 'limit': limit,
                'remaining': max(0, limit - used),
            })
        ctx['service'] = service
        ctx['feature_data'] = feature_data
        ctx['ai_enabled'] = profile.ai_enabled
        return ctx


class ClientAIRunView(ClientRequiredMixin, View):
    """POST -> run a text/image feature synchronously, or queue a video job."""

    def post(self, request, pk):
        feature = get_object_or_404(
            ServiceAIFeature.objects.select_related('provider', 'service'),
            pk=pk, is_active=True, provider__is_active=True)
        profile = request.user.client_profile

        if not profile.ai_enabled:
            return JsonResponse({'status': 'failed',
                                 'error': 'AI features are disabled for your account.'})

        limit = _quota_for(profile, feature)
        used = AIGeneration.used_today(request.user, feature)
        if used >= limit:
            return JsonResponse({'status': 'failed', 'remaining': 0,
                                 'error': f'Daily limit reached ({limit}/day for this tool). '
                                          'Try again tomorrow.'})

        form = build_feature_input_form(feature, data=request.POST, files=request.FILES)
        if not form.is_valid():
            return JsonResponse({'status': 'failed',
                                 'error': '; '.join(f'{k}: {v[0]}' for k, v in form.errors.items())})

        inputs, upload = {}, None
        for name, value in form.cleaned_data.items():
            if hasattr(value, 'read'):  # uploaded file
                upload = value
                inputs[name] = value.name
            else:
                inputs[name] = value

        class SafeDict(dict):
            def __missing__(self, key):
                return f'{{{key}}}'

        rendered = feature.user_prompt_template.format_map(SafeDict(inputs))
        system_prompt = feature.system_prompt
        if feature.output_guidance:
            system_prompt += '\n\n' + feature.output_guidance

        generation = AIGeneration.objects.create(
            client=request.user, feature=feature,
            feature_title=feature.title, provider_name=feature.provider.name,
            model_used=feature.effective_model,
            inputs=inputs, rendered_prompt=rendered,
            status='queued' if feature.feature_type == 'video' else 'running',
            started_at=timezone.now(),
        )
        if upload is not None:
            generation.input_file.save(upload.name, upload, save=True)

        if feature.feature_type == 'video':
            return JsonResponse({'status': 'queued', 'id': generation.pk,
                                 'message': 'Video generation queued. This usually takes a few minutes.',
                                 'remaining': max(0, limit - used - 1)})

        images = None
        if upload is not None:
            mime = mimetypes.guess_type(upload.name)[0] or 'image/png'
            if mime in SAFE_IMAGE_TYPES:
                generation.input_file.open('rb')
                images = [(generation.input_file.read(), mime)]
                generation.input_file.close()

        try:
            adapter = get_adapter(feature.provider, feature.model_override or None)
            if feature.feature_type == 'image':
                result = adapter.generate_image(rendered, input_images=images)
                ext = mimetypes.guess_extension(result.mime_type) or '.png'
                generation.output_file.save(f'gen_{generation.pk}{ext}',
                                            ContentFile(result.content), save=False)
                generation.output_mime = result.mime_type
            else:
                result = adapter.generate_text(system_prompt, rendered, images=images)
                generation.output_text = result.text
                generation.tokens_input = result.tokens_in
                generation.tokens_output = result.tokens_out
            generation.status = 'succeeded'
            generation.completed_at = timezone.now()
            generation.save()
        except AIProviderError as exc:
            generation.status = 'failed'
            generation.error = str(exc)
            generation.completed_at = timezone.now()
            generation.save()
            return JsonResponse({'status': 'failed', 'error': str(exc),
                                 'remaining': max(0, limit - used)})
        except Exception:
            generation.status = 'failed'
            generation.error = 'Unexpected internal error.'
            generation.completed_at = timezone.now()
            generation.save()
            return JsonResponse({'status': 'failed',
                                 'error': 'Something went wrong. Please try again.'})

        payload = {'status': 'succeeded', 'id': generation.pk,
                   'remaining': max(0, limit - used - 1)}
        if generation.output_text:
            payload['output_text'] = generation.output_text
        if generation.output_file:
            payload['file_url'] = reverse('client_ai_file', args=[generation.pk])
            payload['mime'] = generation.output_mime
        return JsonResponse(payload)


class ClientAIStatusView(ClientRequiredMixin, View):
    """Polling endpoint for queued/running (video) generations."""

    def get(self, request, pk):
        generation = get_object_or_404(AIGeneration, pk=pk, client=request.user)
        payload = {'status': generation.status}
        if generation.status == 'succeeded':
            if generation.output_text:
                payload['output_text'] = generation.output_text
            if generation.output_file:
                payload['file_url'] = reverse('client_ai_file', args=[generation.pk])
                payload['mime'] = generation.output_mime
        elif generation.status == 'failed':
            payload['error'] = generation.error or 'Generation failed.'
        return JsonResponse(payload)


class ClientAIFileView(ClientRequiredMixin, View):
    """Auth-gated streaming of an AI output (image/video) from private storage."""

    def get(self, request, pk):
        generation = get_object_or_404(AIGeneration, pk=pk, client=request.user)
        if not generation.output_file:
            raise Http404
        return FileResponse(generation.output_file.open('rb'),
                            content_type=generation.output_mime or 'application/octet-stream')


class ClientAIHistoryView(ClientRequiredMixin, ListView):
    model = AIGeneration
    template_name = 'client/ai/history.html'
    context_object_name = 'generations'
    paginate_by = 10

    def get_queryset(self):
        return (AIGeneration.objects.filter(client=self.request.user)
                .select_related('feature', 'feature__service').order_by('-created_at'))
