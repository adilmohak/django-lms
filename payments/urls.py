from django.urls import path
from . import views

urlpatterns = [
    path('', views.PaymentGetwaysView.as_view(), name='payment_gateways'),

    path('paypal/', views.payment_paypal, name="paypal"),
    path('stripe/', views.payment_stripe, name="stripe"),
    path('coinbase/', views.payment_coinbase, name="coinbase"),
    path('paylike/', views.payment_paylike, name="paylike"),
    
    path('stripe-charge/', views.stripe_charge, name='stripe_charge'),
    path('gopay-charge/', views.gopay_charge, name="gopay_charge"),

    path('payment-succeed/', views.payment_succeed, name="payment-succeed"),
    path('complete/', views.paymentComplete, name="complete"),
    path('create-invoice/', views.create_invoice, name="create_invoice"),
    path('invoice-detail/<int:id>/', views.invoice_detail, name="invoice_detail"),
]
