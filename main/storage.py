"""Private file storage for client deliverables and AI outputs.

Files stored here live OUTSIDE MEDIA_ROOT, so the public /media/ URL route
can never serve them. Access happens only through authenticated views that
stream a FileResponse after ownership checks.
"""
from django.conf import settings
from django.core.files.storage import FileSystemStorage


class PrivateMediaStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('location', settings.PRIVATE_MEDIA_ROOT)
        # No base_url: calling .url() should fail loudly instead of leaking a path
        kwargs.setdefault('base_url', None)
        super().__init__(*args, **kwargs)


private_storage = PrivateMediaStorage()
