import json
import stripe
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from django.views.generic import TemplateView
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from .models import Invoice
from .serializers import InvoiceSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY


class InvoicePage(TemplateView):
    template_name = "landing.html"

    def get_context_data(self, **kwargs):
        invoice_id = self.kwargs["pk"]
        invoice = Invoice.objects.get(id=invoice_id)
        context = super(InvoicePage, self).get_context_data(**kwargs)
        context.update(
            {"invoice": invoice, "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY}
        )
        return context


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"


class InvoiceCreateListAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination
    queryset = Invoice.objects.all()
    filter_backends = [filters.SearchFilter]
    serializer_class = InvoiceSerializer
    search_fields = [
        "id",
        "invoice_number",
        "client_name",
        "client_email",
        "project_name",
        "paid",
    ]


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        invoice_id = self.kwargs["pk"]
        invoice = Invoice.objects.get(id=invoice_id)
        print(invoice)
        YOUR_DOMAIN = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "inr",
                        "unit_amount": invoice.amount,
                        "product_data": {
                            "invoice_number": invoice.invoice_number,
                        },
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=YOUR_DOMAIN + "/success/",
            cancel_url=YOUR_DOMAIN + "/cancel/",
        )
        return JsonResponse({"id": checkout_session.id})


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    try:
        stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    return HttpResponse(status=200)


class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            req_json = json.loads(request.body)
            customer = stripe.Customer.create(email=req_json["email"])
            invoice_id = self.kwargs["pk"]
            invoice = Invoice.objects.get(id=invoice_id)
            intent = stripe.PaymentIntent.create(
                amount=invoice.amount * 100,
                currency="inr",
                customer=customer["id"],
                metadata={"invoice_id": invoice.id},
            )
            invoice.paid = True
            invoice.save()
            return JsonResponse({"clientSecret": intent["client_secret"]})
        except Exception as e:
            return JsonResponse({"error": str(e)})


def homepage(request):
    invoices = Invoice.objects.all()
    return render(request, "home.html", context={"invoices": invoices})
