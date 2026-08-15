"""Client portal views added in the portal-completion phase:
messages/tickets, notifications, and profile management."""
from django.contrib import messages as flash
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, UpdateView, CreateView, View

from .forms import ClientMessageForm, ClientProfileForm
from .mixins import ClientRequiredMixin
from .models import ClientMessage, ClientNotification


class ClientMessageListView(ClientRequiredMixin, ListView):
    model = ClientMessage
    template_name = 'client/messages/list.html'
    context_object_name = 'tickets'
    paginate_by = 10

    def get_queryset(self):
        qs = ClientMessage.objects.filter(client=self.request.user).order_by('-created_at')
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['status_choices'] = ClientMessage.MESSAGE_STATUS_CHOICES
        ctx['current_status'] = self.request.GET.get('status', '')
        return ctx


class ClientMessageCreateView(ClientRequiredMixin, CreateView):
    model = ClientMessage
    form_class = ClientMessageForm
    template_name = 'client/messages/form.html'
    success_url = reverse_lazy('client_messages')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['client'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.client = self.request.user
        flash.success(self.request, 'Your message has been sent. We usually respond within 24 hours.')
        return super().form_valid(form)


class ClientMessageDetailView(ClientRequiredMixin, DetailView):
    model = ClientMessage
    template_name = 'client/messages/detail.html'
    context_object_name = 'ticket'

    def get_queryset(self):
        return ClientMessage.objects.filter(client=self.request.user)


class ClientNotificationListView(ClientRequiredMixin, ListView):
    model = ClientNotification
    template_name = 'client/notifications/list.html'
    context_object_name = 'notifications'
    paginate_by = 20

    def get_queryset(self):
        return ClientNotification.objects.filter(client=self.request.user).order_by('-created_at')


class ClientNotificationReadView(ClientRequiredMixin, View):
    def post(self, request, pk):
        notification = get_object_or_404(ClientNotification, pk=pk, client=request.user)
        notification.mark_as_read()
        next_url = request.POST.get('next') or 'client_notifications'
        return redirect(next_url)


class ClientNotificationReadAllView(ClientRequiredMixin, View):
    def post(self, request):
        ClientNotification.objects.filter(client=request.user, is_read=False).update(
            is_read=True, read_at=timezone.now())
        return redirect('client_notifications')


class ClientProfileView(ClientRequiredMixin, UpdateView):
    form_class = ClientProfileForm
    template_name = 'client/profile.html'
    success_url = reverse_lazy('client_profile')

    def get_object(self, queryset=None):
        return self.request.user.client_profile

    def form_valid(self, form):
        flash.success(self.request, 'Profile updated.')
        return super().form_valid(form)
