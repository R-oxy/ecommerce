from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.models import Group
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .utils import cookieCart, cartData, guestOrder
from .decorators import unauthenticated_user, allowed_users, admin_only

#create your views here:


@unauthenticated_user
def loginPage(request):
    page = 'login_page'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store')

    return render(request, 'store/Login_Register.html', {'page': page})


def logoutPage(request):
    logout(request)
    return redirect('login_page')


@unauthenticated_user
def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm(request, request.POST)

    if request.method == 'POST':
        form = CustomUserCreationForm(request, request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name = 'customer')
            user.groups.add(group)

            messages.success(request, 'Account created successfully for' + username)

            user = authenticate(request, username=username, password=request.POST['password1'])

            if user is not None:
                login(request, user)
                return redirect('store')

    context = {'form': form, 'page': page}
    return render(request, 'store/Login_Register.html', context)


def store(request):

    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


@csrf_exempt
def UpdateDescription(request):
    if request.method == 'POST':
        # Handle the form submission
        # Get the product ID and description from the request data
        productId = request.POST.get('productId')
        description = request.POST.get('description')

        # Validate the form data
        if not productId or not description:
            # Return an error if the form data is invalid
            return render(request, 'store/View_Item.html', {'error': 'Invalid form data'})

        # Update the product description in the database
        # You can use the product_id and description variables to update the product in the database
        product = Product.objects.get(id=productId)
        product.description = description
        product.save()

        # Render the updated description on the page
        return render(request, 'store/View_Item.html', {'description': description})
    else:
        # Render the view template
        return render(request, 'store/View_Item.html')


def ViewItem(request):

    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/View_Item.html', context)


def cart(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


@login_required(login_url='login_page')
def checkout(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

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


from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

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

    return JsonResponse('Payment complete', safe=False)


