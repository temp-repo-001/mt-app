from django.db import models

# Create your models here.

from django.db import models

# Create your models here.
# from auth_app.models import MetaModel


class Invoice(models.Model):
    invoice_number = models.CharField(
        max_length=20, null=False, blank=False, unique=True
    )
    client_name = models.CharField(max_length=100, null=False, blank=False)
    client_email = models.CharField(max_length=100, null=False, blank=False)
    project_name = models.CharField(max_length=256, null=False, blank=False)
    amount = models.IntegerField(default=0, null=False)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.invoice_number
