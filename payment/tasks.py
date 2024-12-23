from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

@shared_task
def send_confirmation_email_task(order_id, shipping_data):
    from payment.models import Order, ShippingAddress

    # Fetch order and shipping details
    order = Order.objects.get(id=order_id)
    shipping_address = ShippingAddress.objects.get(id=shipping_data['id'])

    # Render the email template with dynamic data
    subject = f"Order Confirmation - {order.reference}"
    recipient_email = shipping_address.shipping_email
    message = render_to_string('email_confirmation.html', {
        'order': order,
        'shipping_address': shipping_address,
    })

    # Send email
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient_email],
    )
    email.content_subtype = "html"  # Specify that this is an HTML email
    email.send(fail_silently=False)
