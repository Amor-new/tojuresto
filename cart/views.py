from django.shortcuts import render, get_object_or_404
from .cart import Cart
from tojuweb.models import Product
from django.http import JsonResponse
from django.contrib import messages

def cart_summary(request):
	# Get the cart
	cart = Cart(request)
	cart_products = cart.get_prods
	quantities = cart.get_quants
	totals = cart.cart_total()
	return render(request, "cart_summary.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals})


def cart_add(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product_qty = int(request.POST.get('product_qty', 1))

        product = Product.objects.get(id=product_id)
        cart = Cart(request)
        cart.add(product, product_qty)

    
        return JsonResponse({'cart_count': len(cart)})







def cart_delete(request):
	cart = Cart(request)
	if request.POST.get('action') == 'post':
		product_id = int(request.POST.get('product_id'))
		cart.delete(product=product_id)

		response = JsonResponse({'product':product_id})
		messages.success(request, ("Item Deleted From Shopping Cart..."))
		return response


def cart_update(request):
	cart = Cart(request)
	if request.POST.get('action') == 'post':
		# Get stuff
		product_id = int(request.POST.get('product_id'))
		product_qty = int(request.POST.get('product_qty'))

		cart.update(product=product_id, quantity=product_qty)

		response = JsonResponse({'qty':product_qty})
		
		messages.success(request, ("Your Cart Has Been Updated..."))
		return response

