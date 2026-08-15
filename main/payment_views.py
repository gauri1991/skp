"""Payment flows: Razorpay (modal + webhook), Stripe (Checkout + webhook),
manual/UPI (client reference + admin confirmation)."""
import json
from decimal import Decimal, InvalidOperation

from django.contrib import messages as flash
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, UpdateView, View

from .forms import PaymentGatewayForm
from .mixins import ClientRequiredMixin, StaffRequiredMixin
from .models import ClientOrder, PaymentGateway, PaymentTransaction


def _active_gateways():
    return PaymentGateway.objects.filter(is_active=True).order_by('display_order')


def _balance_due(order):
    return (order.quoted_amount or Decimal('0')) - (order.paid_amount or Decimal('0'))


def _parse_amount(raw, order):
    """Validate a client-submitted amount against the order balance."""
    try:
        amount = Decimal(str(raw)).quantize(Decimal('0.01'))
    except (InvalidOperation, TypeError, ValueError):
        return None, 'Invalid amount.'
    if amount <= 0:
        return None, 'Amount must be positive.'
    balance = _balance_due(order)
    if balance <= 0:
        return None, 'This order has no balance due.'
    if amount > balance:
        return None, f'Amount exceeds the balance due (₹{balance}).'
    return amount, ''


# ================= Client payment flows =================

class ClientOrderPayView(ClientRequiredMixin, View):
    template_name = 'client/payments/pay.html'

    def get(self, request, pk):
        order = get_object_or_404(ClientOrder, pk=pk, client=request.user)
        return render(request, self.template_name, {
            'order': order,
            'balance_due': _balance_due(order),
            'gateways': _active_gateways(),
        })


class RazorpayCreateView(ClientRequiredMixin, View):
    """AJAX: create a Razorpay order + local transaction for checkout.js."""

    def post(self, request, order_pk):
        order = get_object_or_404(ClientOrder, pk=order_pk, client=request.user)
        gateway = _active_gateways().filter(gateway_type='razorpay').first()
        if gateway is None or not gateway.key_id or not gateway.key_secret:
            return JsonResponse({'success': False, 'error': 'Razorpay is not available right now.'})
        amount, err = _parse_amount(request.POST.get('amount'), order)
        if amount is None:
            return JsonResponse({'success': False, 'error': err})

        import razorpay
        client = razorpay.Client(auth=(gateway.key_id, gateway.key_secret))
        transaction = PaymentTransaction.objects.create(
            order=order, client=request.user, gateway=gateway,
            amount=amount, status='created')
        try:
            rzp_order = client.order.create({
                'amount': int(amount * 100),  # paise
                'currency': 'INR',
                'receipt': transaction.receipt_no,
                'notes': {'order_number': order.order_number},
            })
        except Exception as exc:
            transaction.status = 'failed'
            transaction.notes = f'Order create failed: {exc}'
            transaction.save()
            return JsonResponse({'success': False, 'error': 'Could not start the payment. Try again.'})
        transaction.gateway_order_id = rzp_order['id']
        transaction.save(update_fields=['gateway_order_id'])
        return JsonResponse({
            'success': True,
            'key_id': gateway.key_id,
            'razorpay_order_id': rzp_order['id'],
            'amount': int(amount * 100),
            'currency': 'INR',
            'name': 'Sumithra KP',
            'description': f'Payment for {order.order_number}',
            'prefill': {'email': request.user.email,
                        'contact': request.user.client_profile.mobile},
            'callback_data': {'transaction_id': transaction.pk},
        })


class RazorpayCallbackView(ClientRequiredMixin, View):
    """Checkout handler success POST -> verify signature -> mark paid."""

    def post(self, request):
        transaction_id = request.POST.get('transaction_id')
        payment_id = request.POST.get('razorpay_payment_id', '')
        rzp_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        transaction = get_object_or_404(
            PaymentTransaction, pk=transaction_id, client=request.user,
            gateway__gateway_type='razorpay')
        if transaction.gateway_order_id != rzp_order_id:
            return JsonResponse({'success': False, 'error': 'Order mismatch.'})

        import razorpay
        client = razorpay.Client(auth=(transaction.gateway.key_id, transaction.gateway.key_secret))
        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': rzp_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature,
            })
        except Exception:
            transaction.status = 'failed'
            transaction.notes = 'Signature verification failed.'
            transaction.save()
            return JsonResponse({'success': False, 'error': 'Payment verification failed.'})
        transaction.mark_paid(payment_id=payment_id, signature=signature)
        return JsonResponse({'success': True,
                             'redirect': reverse('client_order_detail', args=[transaction.order_id])})


class StripeCheckoutView(ClientRequiredMixin, View):
    def post(self, request, order_pk):
        order = get_object_or_404(ClientOrder, pk=order_pk, client=request.user)
        gateway = _active_gateways().filter(gateway_type='stripe').first()
        if gateway is None or not gateway.key_secret:
            flash.error(request, 'Stripe is not available right now.')
            return redirect('client_order_pay', pk=order.pk)
        amount, err = _parse_amount(request.POST.get('amount'), order)
        if amount is None:
            flash.error(request, err)
            return redirect('client_order_pay', pk=order.pk)

        import stripe
        stripe.api_key = gateway.key_secret
        transaction = PaymentTransaction.objects.create(
            order=order, client=request.user, gateway=gateway,
            amount=amount, status='created')
        base = f"{request.scheme}://{request.get_host()}"
        try:
            session = stripe.checkout.Session.create(
                mode='payment',
                client_reference_id=str(transaction.pk),
                customer_email=request.user.email,
                line_items=[{
                    'price_data': {
                        'currency': 'inr',
                        'unit_amount': int(amount * 100),
                        'product_data': {'name': f'Order {order.order_number}'},
                    },
                    'quantity': 1,
                }],
                success_url=f"{base}{reverse('stripe_success')}?tx={transaction.pk}",
                cancel_url=f"{base}{reverse('stripe_cancel')}?tx={transaction.pk}",
            )
        except Exception as exc:
            transaction.status = 'failed'
            transaction.notes = f'Session create failed: {exc}'
            transaction.save()
            flash.error(request, 'Could not start the Stripe payment. Try again.')
            return redirect('client_order_pay', pk=order.pk)
        transaction.gateway_order_id = session.id
        transaction.save(update_fields=['gateway_order_id'])
        return redirect(session.url)


class StripeSuccessView(ClientRequiredMixin, View):
    def get(self, request):
        tx = request.GET.get('tx')
        transaction = PaymentTransaction.objects.filter(pk=tx, client=request.user).first()
        if transaction and transaction.status != 'paid':
            flash.info(request, 'Payment received — confirmation usually lands within a minute.')
        elif transaction:
            flash.success(request, 'Payment confirmed. Thank you!')
        return redirect('client_order_detail', pk=transaction.order_id) if transaction \
            else redirect('client_orders')


class StripeCancelView(ClientRequiredMixin, View):
    def get(self, request):
        tx = request.GET.get('tx')
        transaction = PaymentTransaction.objects.filter(pk=tx, client=request.user).first()
        if transaction and transaction.status == 'created':
            transaction.status = 'failed'
            transaction.notes = 'Cancelled by client.'
            transaction.save()
        flash.info(request, 'Payment cancelled.')
        return redirect('client_order_pay', pk=transaction.order_id) if transaction \
            else redirect('client_orders')


class ManualPaymentSubmitView(ClientRequiredMixin, View):
    def post(self, request, order_pk):
        order = get_object_or_404(ClientOrder, pk=order_pk, client=request.user)
        gateway = _active_gateways().filter(gateway_type='manual').first()
        if gateway is None:
            flash.error(request, 'Manual payment is not available right now.')
            return redirect('client_order_pay', pk=order.pk)
        amount, err = _parse_amount(request.POST.get('amount'), order)
        if amount is None:
            flash.error(request, err)
            return redirect('client_order_pay', pk=order.pk)
        reference = (request.POST.get('reference') or '').strip()
        if not reference:
            flash.error(request, 'Please enter the UPI/bank transaction reference.')
            return redirect('client_order_pay', pk=order.pk)
        PaymentTransaction.objects.create(
            order=order, client=request.user, gateway=gateway,
            amount=amount, status='pending', reference_note=reference)
        flash.success(request, 'Payment reference submitted. We will confirm it shortly.')
        return redirect('client_order_detail', pk=order.pk)


# ================= Webhooks =================

@csrf_exempt
def webhook_razorpay(request):
    if request.method != 'POST':
        return HttpResponse(status=405)
    gateway = PaymentGateway.objects.filter(gateway_type='razorpay').first()
    if gateway is None or not gateway.webhook_secret:
        return HttpResponse(status=400)

    import razorpay
    signature = request.headers.get('X-Razorpay-Signature', '')
    body = request.body.decode('utf-8')
    try:
        razorpay.Utility(None).verify_webhook_signature(body, signature, gateway.webhook_secret)
    except Exception:
        return HttpResponse(status=400)

    try:
        event = json.loads(body)
    except json.JSONDecodeError:
        return HttpResponse(status=400)
    if event.get('event') == 'payment.captured':
        payment = event['payload']['payment']['entity']
        rzp_order_id = payment.get('order_id', '')
        transaction = PaymentTransaction.objects.filter(
            gateway_order_id=rzp_order_id).exclude(status='paid').first()
        if transaction:
            transaction.mark_paid(payment_id=payment.get('id', ''))
    return HttpResponse(status=200)


@csrf_exempt
def webhook_stripe(request):
    if request.method != 'POST':
        return HttpResponse(status=405)
    gateway = PaymentGateway.objects.filter(gateway_type='stripe').first()
    if gateway is None or not gateway.webhook_secret:
        return HttpResponse(status=400)

    import stripe
    try:
        event = stripe.Webhook.construct_event(
            request.body, request.headers.get('Stripe-Signature', ''),
            gateway.webhook_secret)
    except Exception:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        transaction = PaymentTransaction.objects.filter(
            pk=session.get('client_reference_id')).exclude(status='paid').first()
        if transaction and transaction.gateway_order_id == session.get('id'):
            transaction.mark_paid(payment_id=session.get('payment_intent', '') or '')
    return HttpResponse(status=200)


# ================= Dashboard =================

class DashboardPaymentListView(StaffRequiredMixin, ListView):
    model = PaymentTransaction
    template_name = 'dashboard/payments/list.html'
    context_object_name = 'payments'
    paginate_by = 25

    def get_queryset(self):
        qs = (PaymentTransaction.objects
              .select_related('order', 'client', 'gateway').order_by('-created_at'))
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['status_choices'] = PaymentTransaction.STATUS_CHOICES
        ctx['current_status'] = self.request.GET.get('status', '')
        ctx['pending_count'] = PaymentTransaction.objects.filter(status='pending').count()
        ctx['gateways'] = PaymentGateway.objects.all()
        ctx['page_title'] = 'Payments'
        return ctx


class DashboardPaymentConfirmView(StaffRequiredMixin, View):
    def post(self, request, pk):
        transaction = get_object_or_404(PaymentTransaction, pk=pk, status='pending')
        transaction.mark_paid(confirmed_by=request.user)
        flash.success(request, f'Payment {transaction.receipt_no} confirmed.')
        return redirect('dashboard_payments')


class DashboardGatewayUpdateView(StaffRequiredMixin, UpdateView):
    model = PaymentGateway
    form_class = PaymentGatewayForm
    template_name = 'dashboard/payments/gateway_form.html'
    success_url = reverse_lazy('dashboard_payments')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['page_title'] = f'Configure {self.object.display_name}'
        return ctx

    def form_valid(self, form):
        flash.success(self.request, 'Gateway settings saved.')
        return super().form_valid(form)
