from django.db import models
from django.conf import settings


class Invoice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total = models.FloatField(null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    payment_complete = models.BooleanField(default=False)
    invoice_code = models.CharField(max_length=200, blank=True, null=True)
