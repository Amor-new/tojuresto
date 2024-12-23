from django.shortcuts import render, redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from tojuweb.models import Product, Profile
import datetime
import uuid, requests
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse
from .tasks import send_confirmation_email_task
from django.contrib.auth.models import AnonymousUser
from django.core.mail import send_mail


def checkout(request):
	cart = Cart(request)
	cart_products = cart.get_prods
	quantities = cart.get_quants
	totals = cart.cart_total()
	shipping_form = ShippingForm(request.POST or None)
	return render(request, "checkout.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})




def billing_info(request):
    if request.method == "POST":
        cart = Cart(request)
        shipping_form = ShippingForm(request.POST)

        if not shipping_form.is_valid():
            messages.error(request, "Please fill out all required fields correctly.")
            return redirect('cart_summary')

        # Store shipping details in the session
        request.session['shipping_details'] = shipping_form.cleaned_data

        # Generate Paystack payment payload
        email = shipping_form.cleaned_data['shipping_email']
        transaction_ref = str(uuid.uuid4())
        cart_total = float(cart.cart_total())  # Convert Decimal to float
        paystack_data = {
            "email": email,
            "amount": int(cart_total * 100),  # Convert to kobo
            "reference": transaction_ref,
            "callback_url": request.build_absolute_uri(reverse('payment_success')),
        }

        # Save transaction reference in the session
        request.session['transaction_ref'] = transaction_ref
        request.session['cart_total'] = cart_total  # Store as float

        # Make the Paystack API call
        paystack_url = "https://api.paystack.co/transaction/initialize"
        headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}

        try:
            response = requests.post(paystack_url, json=paystack_data, headers=headers)
            response_data = response.json()

            if response.status_code == 200 and response_data.get('status'):
                return redirect(response_data['data']['authorization_url'])

            messages.error(request, response_data.get('message', "Payment initialization failed."))
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Error initializing payment: {e}")
    
    return redirect('cart_summary')





def payment_success(request):
    transaction_ref = request.session.get('transaction_ref')

    if not transaction_ref:
        messages.error(request, "No transaction reference found.")
        return redirect('cart_summary')

    url = f"https://api.paystack.co/transaction/verify/{transaction_ref}"
    headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}

    try:
        response = requests.get(url, headers=headers)
        response_data = response.json()

        if response.status_code == 200 and response_data.get('status'):
            cart = Cart(request)

            # Strict retrieval of shipping details
            shipping_details = request.session.get('shipping_details')
            if not shipping_details:
                messages.error(request, "Shipping details are missing. Please provide them before proceeding.")
                return redirect('cart_summary')

            # Check for duplicate transactions
            if Order.objects.filter(reference=transaction_ref).exists():
                messages.error(request, "This transaction has already been processed.")
                return redirect('cart_summary')

            # Create the order
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                full_name=shipping_details['shipping_full_name'],
                email=shipping_details['shipping_email'],
                shipping_address=shipping_details['shipping_address1'],
                amount_paid=request.session.get('cart_total', 0),
                reference=transaction_ref,
                date_ordered=datetime.datetime.now(),
            )

            # Save the order items
            for product, quantity in zip(cart.get_prods(), cart.get_quants()):
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price
                )

            # Save the shipping address
            ShippingAddress.objects.create(
                user=request.user if request.user.is_authenticated else None,
                **shipping_details
            )

            # Send confirmation email
            try:
                subject = "Order Confirmation"
                message = "Thank you for your order. Your order is being processed."
                from_email = "akintoladamilare24@gmail.com"  # Replace with your email
                recipient_email = shipping_details['shipping_email']

                send_mail(subject, message, from_email, [recipient_email], fail_silently=False)
                messages.success(request, f"Order confirmed! A confirmation email has been sent to {recipient_email}.")
            except Exception as e:
                messages.error(request, f"Order confirmed, but we couldn't send the confirmation email: {str(e)}.")
                
            # Clear session data after successful operation
            request.session['cart'] = {}
            request.session.modified = True
            request.session.pop('shipping_details', None)
            request.session.pop('transaction_ref', None)
            request.session.pop('cart_total', None)

            # Render the order confirmation page
            context = {
                'order': order,
                'shipping_address': shipping_details,
            }
            return render(request, 'payment_success.html', context)

        else:
            messages.error(request, "Payment verification failed. Please try again.")
            return redirect('cart_summary')

    except requests.exceptions.RequestException as e:
        messages.error(request, f"Unable to verify payment: {str(e)}. Please contact support.")
        return redirect('cart_summary')