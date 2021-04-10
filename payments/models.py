from django.db import models
from django.contrib.auth.views import get_user_model

User = get_user_model()


class Invoice(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	total = models.FloatField(null=True, blank=True)
	amount = models.FloatField(null=True, blank=True)
	payment_complete = models.BooleanField(default=False)
	invoice_code = models.CharField(max_length=200, blank=True, null=True)
