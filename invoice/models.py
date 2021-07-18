from django.db import models
import bitlyshortener

YOUR_DOMAIN = "http://127.0.0.1:8000/api"
BITLY_ACCESS_TOKEN = "a44a9d4a0a61e5bc7dfa04047117db7511d474aa"


class Invoice(models.Model):
    invoice_number = models.CharField(
        max_length=20, null=False, blank=False, unique=True
    )
    client_name = models.CharField(max_length=100, null=False, blank=False)
    client_email = models.CharField(max_length=100, null=False, blank=False)
    project_name = models.CharField(max_length=256, null=False, blank=False)
    amount = models.IntegerField(default=0, null=False)
    paid = models.BooleanField(default=False)
    url = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.invoice_number

    def add_url(self):
        url = YOUR_DOMAIN + f"/invoices-pay/{self.id}/"
        self.url = url
        self.save()
