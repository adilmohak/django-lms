from django.urls import path
from . import views

urlpatterns = [
    path('', views.PaymentGetwaysView.as_view(), name='payment_gateways'),
    # path('gateways/', views.payment_gateways, name="gateways"),

    path('paypal/', views.payment_paypal, name="paypal"),
    path('stripe/', views.payment_stripe, name="stripe"),
    path('coinbase/', views.payment_coinbase, name="coinbase"),
    path('paylike/', views.payment_paylike, name="paylike"),
    
    path('create_invoice/', views.create_invoice, name="create_invoice"),
    path('invoice_detail/<int:id>/', views.invoice_detail, name="invoice_detail"),

    # path('charge/', views.charge, name="charge"),
    path('payment-succeed/', views.payment_succeed, name="payment-succeed"),

    path('charge/', views.charge, name='charge'), # new

    path('complete/', views.paymentComplete, name="complete"),
    path('gopay_payment/', views.gopay_payment, name="gopay_payment"),
]
