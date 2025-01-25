from django.core.mail import send_mail
from django.conf import settings


def send_order_confirmation(order, price):
    subject = f"Подтверждение заказа #{order.id}"
    message = (
        f"Спасибо за ваш заказ, {order.user.username}!\n\n"
        f"Детали заказа:\n"
        f"Сумма: {price} RUB\n\n"
        f"Мы уведомим вас о дальнейшей обработке заказа."
    )
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [order.user.email]

    send_mail(subject, message, email_from, recipient_list)