# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/account/apikeys
stripe.api_key = "sk_test_51IcEVZHbzY4cUA9T3BZdDayN4gmbJyXuaLCzpLT15HZoOmC17G7CxeEdXeIHSWyhYfxpljsclzzjsFukYNqJTbrW00tv3qIbN2"

intent = stripe.PaymentIntent.create(
  amount=1099,
  currency='usd',
)
