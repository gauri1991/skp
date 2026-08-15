"""Access-control mixins separating the staff dashboard from the client portal."""
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Allow only staff/superuser accounts into the admin dashboard."""

    raise_exception = False  # redirect to login rather than 403

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        # A logged-in client hitting a dashboard URL gets sent to their portal,
        # not a confusing 403 page.
        if self.request.user.is_authenticated and hasattr(self.request.user, 'client_profile'):
            from django.shortcuts import redirect
            return redirect('client_dashboard')
        return super().handle_no_permission()


class ClientRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """Allow only users with a client profile into the client portal."""

    login_url = '/client/login/'

    def get_login_url(self):
        return f"{self.login_url}?type=client"

    def test_func(self):
        return hasattr(self.request.user, 'client_profile')

    def handle_no_permission(self):
        if self.request.user.is_authenticated and self.request.user.is_staff:
            from django.shortcuts import redirect
            return redirect('dashboard_home')
        return super().handle_no_permission()
