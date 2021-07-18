from django.urls import path

from . import views

app_name = "invoice"

urlpatterns = [
    path("invoices/", views.InvoiceCreateListAPIView.as_view(), name="invoices"),
    path(
        "create-checkout-session/<pk>/",
        views.CreateCheckoutSessionView.as_view(),
        name="create-checkout-session",
    ),
    path("invoices-pay/<pk>/", views.InvoicePage.as_view(), name="check-out-session"),
    path("cancel/", views.CancelView.as_view(), name="cancel"),
    path("success/", views.SuccessView.as_view(), name="success"),
    path("webhooks/stripe/", views.stripe_webhook, name="web_hook"),
    path(
        "create-payment-intent/<pk>/",
        views.StripeIntentView.as_view(),
        name="create-payment-intent",
    ),
    path("home/", views.homepage, name="home-page"),
]
