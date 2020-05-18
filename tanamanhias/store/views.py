# view nya si app store
from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart,cartData,guestOrder

from django.contrib.auth import authenticate, login, logout

from django.shortcuts import render, redirect


def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']


    print(request.method)
    if request.method == 'POST':
        print(request.POST["Logout"])
        if request.POST["Logout"] == "Logout":
            logout(request)
        return redirect('login')



    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)

def cart(request):

	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)


def checkout(request):

	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def index(request):
    return render(request,'store/index.html')

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
	return JsonResponse('Payment submitted..', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	return JsonResponse('Payment submitted..', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)


    else:
       customer,order = guestOrder(request,data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == order.get_cart_total:
            order.complete = True
    order.save()

    if order.shipping == True:
         ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )

    return JsonResponse('Payment submitted..', safe=False)

def cart(request):

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		#Create empty cart for now for non-logged in user
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart = {}
			print('CART:', cart)

		items = []
		order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
		cartItems = order['get_cart_items']

		for i in cart:
			#We use try block to prevent items in cart that may have been removed from causing error
			try:
				cartItems += cart[i]['quantity']

				product = Product.objects.get(id=i)
				total = (product.price * cart[i]['quantity'])

				order['get_cart_total'] += total
				order['get_cart_items'] += cart[i]['quantity']

				item = {
					'id':product.id,
					'product':{'id':product.id,'name':product.name, 'price':product.price,
					'imageURL':product.imageURL}, 'quantity':cart[i]['quantity'],
					'digital':product.digital,'get_total':total,
					}
				items.append(item)

				if product.digital == False:
					order['shipping'] = True
			except:
				pass


	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)


