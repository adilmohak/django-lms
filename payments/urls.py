from django.urls import path
from . import views

urlpatterns = [
    # path('gateways/', views.payment_gateways, name="gateways"),

    path('paypal/', views.payment_paypal, name="paypal"),
    path('stripe/', views.payment_stripe, name="stripe"),
    path('coinbase/', views.payment_coinbase, name="coinbase"),
    path('paylike/', views.payment_paylike, name="paylike"),

    # path('charge/', views.charge, name="charge"),
    path('thank_you/', views.thank_you, name="thank_you"),


    path('charge/', views.charge, name='charge'), # new
    path('', views.PaymentGetwaysView.as_view(), name='home_'),
]
