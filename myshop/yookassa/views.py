import os
from dotenv import load_dotenv
from yookassa import Configuration, Payment
from django.views import View
from django.shortcuts import get_object_or_404
from Order.models import Order

load_dotenv()

Configuration.account_id = os.getenv('YOKASSA_SHOP_ID')
Configuration.secret_key = os.getenv('YOKASSA_SECRET_KEY')

class PaymentView(View):
    def process_payment(self,request):
        order_id = request.POST.get('order_id')
        order = get_object_or_404(Order, id=order_id)
        amount = order.price
        order_id = order.id
        payment = Payment.create({
            "amount": {
                "value": f"{amount}.00",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "http://127.0.0.1:8000/payment_success"
            },
            "capture": True,
            "description": f"Заказ {order_id}"
        })
        confirmation_url = payment.confirmation.confirmation_url
        return confirmation_url