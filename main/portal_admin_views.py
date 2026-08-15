"""Staff dashboard views for managing the client portal:
orders, deliverables, clients, and client messages."""
from django.contrib import messages as flash
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Count, Q, Sum
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView, DetailView, ListView, UpdateView, View,
)

from .forms import (
    AdminReplyForm, ClientAILimitForm, ClientDeliverableUploadForm, ClientOrderForm,
)
from .mixins import StaffRequiredMixin
from .models import (
    ClientDeliverable, ClientMessage, ClientNotification, ClientOrder,
    ClientProfile, ServiceInquiry,
)


# ---------- Orders ----------

class DashboardOrderListView(StaffRequiredMixin, ListView):
    model = ClientOrder
    template_name = 'dashboard/orders/list.html'
    context_object_name = 'orders'
    paginate_by = 20

    def get_queryset(self):
        qs = (ClientOrder.objects
              .select_related('client', 'service_inquiry', 'service_inquiry__service')
              .annotate(deliverable_count=Count('deliverables'))
              .order_by('-created_at'))
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(order_number__icontains=q) | Q(client__email__icontains=q) |
                Q(service_inquiry__project_title__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['status_choices'] = ClientOrder.ORDER_STATUS_CHOICES
        ctx['current_status'] = self.request.GET.get('status', '')
        ctx['q'] = self.request.GET.get('q', '')
        ctx['page_title'] = 'Client Orders'
        return ctx


class DashboardOrderCreateView(StaffRequiredMixin, CreateView):
    model = ClientOrder
    form_class = ClientOrderForm
    template_name = 'dashboard/orders/form.html'

    def get_initial(self):
        initial = super().get_initial()
        inquiry_id = self.request.GET.get('inquiry')
        if inquiry_id:
            inquiry = ServiceInquiry.objects.filter(pk=inquiry_id, order__isnull=True).first()
            if inquiry:
                initial['service_inquiry'] = inquiry
                client = inquiry.client or User.objects.filter(
                    client_profile__isnull=False, email__iexact=inquiry.client_email).first()
                if client:
                    initial['client'] = client
        return initial

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = 'Create Order'
        inquiry_id = self.request.GET.get('inquiry')
        if inquiry_id:
            ctx['from_inquiry'] = ServiceInquiry.objects.filter(pk=inquiry_id).first()
            if ctx['from_inquiry'] and not self.get_initial().get('client'):
                ctx['no_client_match'] = True
        return ctx

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
        except IntegrityError:
            # order_number race under threaded workers: retry once
            form.instance.pk = None
            form.instance.order_number = ''
            response = super().form_valid(form)
        ClientNotification.objects.create(
            client=self.object.client,
            title='New Order Created',
            message=f'Order {self.object.order_number} has been created for you.',
            notification_type='order_update',
            order=self.object,
        )
        flash.success(self.request, f'Order {self.object.order_number} created.')
        return response

    def get_success_url(self):
        return reverse('dashboard_order_detail', args=[self.object.pk])


class DashboardOrderDetailView(StaffRequiredMixin, DetailView):
    model = ClientOrder
    template_name = 'dashboard/orders/detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['deliverables'] = self.object.deliverables.order_by('-created_at')
        ctx['order_messages'] = self.object.messages.order_by('-created_at')
        ctx['payments'] = getattr(self.object, 'payments', None)
        ctx['page_title'] = f'Order {self.object.order_number}'
        return ctx


class DashboardOrderUpdateView(StaffRequiredMixin, UpdateView):
    model = ClientOrder
    form_class = ClientOrderForm
    template_name = 'dashboard/orders/form.html'

    def form_valid(self, form):
        if 'status' in form.changed_data:
            ClientNotification.objects.create(
                client=self.object.client,
                title='Order Status Updated',
                message=(f'Order {self.object.order_number} is now: '
                         f'{form.instance.get_status_display()}.'),
                notification_type='order_update',
                order=self.object,
            )
        flash.success(self.request, 'Order updated.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = f'Edit {self.object.order_number}'
        return ctx

    def get_success_url(self):
        return reverse('dashboard_order_detail', args=[self.object.pk])


class DashboardDeliverableUploadView(StaffRequiredMixin, CreateView):
    model = ClientDeliverable
    form_class = ClientDeliverableUploadForm
    template_name = 'dashboard/orders/deliverable_upload.html'

    def dispatch(self, request, *args, **kwargs):
        self.order = get_object_or_404(ClientOrder, pk=kwargs['order_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.order = self.order
        response = super().form_valid(form)
        if self.object.status == 'ready':
            ClientNotification.objects.create(
                client=self.order.client,
                title='New Deliverable Ready',
                message=f'"{self.object.title}" is ready to download in order {self.order.order_number}.',
                notification_type='delivery_ready',
                order=self.order,
                deliverable=self.object,
            )
        flash.success(self.request, 'Deliverable uploaded.')
        return response

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['order'] = self.order
        ctx['page_title'] = f'Upload Deliverable — {self.order.order_number}'
        return ctx

    def get_success_url(self):
        return reverse('dashboard_order_detail', args=[self.order.pk])


# ---------- Clients ----------

class DashboardClientListView(StaffRequiredMixin, ListView):
    model = ClientProfile
    template_name = 'dashboard/clients/list.html'
    context_object_name = 'clients'
    paginate_by = 20

    def get_queryset(self):
        qs = (ClientProfile.objects.select_related('user')
              .annotate(order_count=Count('user__orders'))
              .order_by('-created_at'))
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(user__email__icontains=q) | Q(user__first_name__icontains=q) |
                Q(mobile__icontains=q) | Q(company__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '')
        ctx['page_title'] = 'Clients'
        return ctx


class DashboardClientDetailView(StaffRequiredMixin, DetailView):
    model = ClientProfile
    template_name = 'dashboard/clients/detail.html'
    context_object_name = 'client_profile'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.object.user
        ctx['orders'] = user.orders.order_by('-created_at')
        ctx['inquiries'] = user.service_inquiries.order_by('-created_at')
        ctx['ai_form'] = ClientAILimitForm(instance=self.object)
        ctx['total_paid'] = user.orders.aggregate(s=Sum('paid_amount'))['s'] or 0
        ctx['page_title'] = user.get_full_name() or user.email
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ClientAILimitForm(request.POST, instance=self.object)
        if form.is_valid():
            form.save()
            flash.success(request, 'AI settings updated for this client.')
        return redirect('dashboard_client_detail', pk=self.object.pk)


# ---------- Client messages (tickets) ----------

class DashboardClientMessageListView(StaffRequiredMixin, ListView):
    model = ClientMessage
    template_name = 'dashboard/client_messages/list.html'
    context_object_name = 'tickets'
    paginate_by = 20

    def get_queryset(self):
        qs = ClientMessage.objects.select_related('client', 'order').order_by('-created_at')
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['status_choices'] = ClientMessage.MESSAGE_STATUS_CHOICES
        ctx['current_status'] = self.request.GET.get('status', '')
        ctx['open_count'] = ClientMessage.objects.filter(status='open').count()
        ctx['page_title'] = 'Client Messages'
        return ctx


class DashboardClientMessageDetailView(StaffRequiredMixin, DetailView):
    model = ClientMessage
    template_name = 'dashboard/client_messages/detail.html'
    context_object_name = 'ticket'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['reply_form'] = AdminReplyForm(instance=self.object)
        ctx['page_title'] = self.object.subject
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = AdminReplyForm(request.POST, instance=self.object)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.admin_user = request.user
            ticket.responded_at = timezone.now()
            ticket.save()
            ClientNotification.objects.create(
                client=ticket.client,
                title='Reply to your message',
                message=f'We replied to "{ticket.subject}". Open your messages to read it.',
                notification_type='system',
            )
            flash.success(request, 'Reply sent to client.')
        return redirect('dashboard_client_message_detail', pk=self.object.pk)
