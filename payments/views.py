from django.shortcuts import render
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY
# stripe.ApplePayDomain.create(
#   domain_name='example.com',
# )

# def payment_gateways(request):
# 	print(settings.STRIPE_PUBLISHABLE_KEY)
# 	context = {
# 		'key': settings.STRIPE_PUBLISHABLE_KEY
# 	}
# 	return render(request, 'payments/payment_gateways.html', context)


def payment_paypal(request):
	return render(request, 'payments/paypal.html', context={})


def payment_stripe(request):
	return render(request, 'payments/stripe.html', context={})


def payment_coinbase(request):
	return render(request, 'payments/coinbase.html', context={})


def payment_paylike(request):
	return render(request, 'payments/paylike.html', context={})


def thank_you(request):
	return render(request, 'payments/thank_you.html', context={})


# def charge(request):
# 	if request.method == 'POST':
# 		charge = stripe.Charge.create(
# 			amount=500,
# 			currency='eur',
# 			description='Payment GetWays',
# 			source=request.POST['stripeToken']
# 		)
# 		return render(request, 'payments/charge.html')





from django.views.generic.base import TemplateView

class PaymentGetwaysView(TemplateView):
    template_name = 'payments/payment_gateways.html'

    def get_context_data(self, **kwargs): # new
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        context['amount'] = 500
        context['description'] = "Stripe Payment"
        return context



def charge(request): # new
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=500,
            currency='usd',
            description='A Django charge',
            source=request.POST['stripeToken']
        )
        return render(request, 'payments/charge.html')
