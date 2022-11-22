# import requests
# import json
# import uuid 
import json
import uuid
import requests

from django.contrib.auth.models import User 
# from multiprocessing import context
# from urllib import request
from django.shortcuts import redirect, render, HttpResponse, redirect 
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from userprofile.models import *
from userprofile.forms import *
from store.models import *
from store.forms import *
from  . models import *
from  . forms import *
# from django.http import HttpResponse

# CRUD 
# C = Create (POST)
# R = Read (GET)
# U = Update (PUT, PATCH) 
# D = Delete (DELETE)

# Create your views here.
@login_required(login_url= 'signin')
def details(request):
    logout(request)
    return redirect('signin')
    
def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid:
            form.save()
            messages.success(request, 'Thanks you for contactin us!......')
            return redirect('index')
        else:
            messages.error(request, form.errors)
            return redirect('index')
    return render(request, 'index.html')
        
def index(request):
    category = Category.objects.all()
    context = {
        'adeyemi': category,
    }

    return render(request, 'index.html', context)

def categories(request):
    categories = Category.objects.all()
    # categories = Category.objects.get()
    # categories = Category.objects.filter()
    context = {
        'categories':categories,
    }
    return render(request, 'categories.html', context)

def product(request):
    product = Product.objects.all()
    context = {
        'product':product,
    }
    return render(request, 'product.html', context)

def category(request, id, slug):
    category = Product.objects.filter(category_id=id)
    context = {
        'category':category,
    }
    return render(request, 'category.html', context)
    
@login_required(login_url='signin')
def details(request, id):
    details = Product.objects.get(pk=id)
    context = {
        'details': details,
    }
    return render(request, 'details.html', context)

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username= username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Welcome to Team cyber dev store!.....')
            return redirect('index')
        else:
            messages.error(request, 'invalid username/password. Input correct details......')
            return redirect('signin')
    return render(request, 'signin.html')
    
@login_required(login_url='signin')
def signout(request):
    logout(request)
    return redirect('signin')

def signup(request):
    form = SignupForm()
    if request.method == "POST":
        address = request.POST['address']
        state = request.POST['state']
        gender = request.POST['gender']
        nationality = request.POST['nationality']
        phone = request.POST['phone']
        pix = request.POST['pix']
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            newprofile = Profile(user=user)
            newprofile.username = user.username
            newprofile.first_name = user.first_name
            newprofile.last_name = user.last_name
            newprofile.email = user.email
            newprofile.phone = phone
            newprofile.state = state
            newprofile.address = address
            newprofile.nationality = nationality
            newprofile.pix = pix
            newprofile.save()
            login(request, user)
            messages.success(request, f'Congratulations, {user.username}, Your Registration is Susseceful')
            return redirect('index')
        else:
            messages.error(request, form.errors)
            return redirect('signup')
    return render(request, 'signup.html')

@login_required(login_url='signin')
def profile(request):
    profile = Profile.objects.get(user__username = request.user.username)
    context = {
        'profile':profile
    }

    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def profile_update(request):
    profile = Profile.objects.get(user__username = request.user.username)
    update = ProfileUpdate(instance=request.user.profile)
    if request.method == 'POST':
        update = ProfileUpdate(request.POST, request.FILES, instance=request.user.profile)
        if update.is_valid():
            user = update.save()
            new = user.first_name
            messages.success(request, f'Congratulations {{new}}, Your update as bean succesful.......')
            return redirect('profile')
        else:
            messages.error(request, update.errors)
            return redirect('profile_update')
    context = {
        'profile':profile,
        'update':update,
    }
    return render(request, 'profile_update.html', context)

@login_required(login_url='signin')
def password(request):
    profile = Profile.objects.get(user__username = request.user.username)
    form = PasswordChangeForm(request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            update_session_auth_hash(request, user)
            user = form.save()
            messages.success(request, 'Password Change Successful!......')
            return redirect('profile')
        else:
            messages.error(request, form.errors)
            return redirect('password')
    context = {
        'form':form,
    }
    return render(request, 'password.html', context)

@login_required(login_url='signin')
def cart(request):
    if request.method == 'POST':
        quant = int(request.POST['quantity'])
        item_id = request.POST['product_id']
        product = Product.objects.get(pk=item_id)
        order_num = Profile.objects.get(user__username = request.user.username)
        order_on = order_num.id
        cart = Cart.objects.filter(user__username=request.user.username, paid=False)
        if cart: 
            basket = Cart.objects.filter(product_id=product.id, user__username = request.user.username, paid=False).first()
            if basket:
                basket.quantity += quant
                basket.amount = product.price * product.quantity
                basket.save()
                messages.success(request, ' product added successfully!.....')
                return redirect('product')
            else:
                newitem = Cart()
                newitem.user = request.user
                newitem.product = product
                newitem.price = product.price
                newitem.quantity = quant
                newitem.amount = product.price *quant
                newitem.title_g = product.title_r
                newitem.order_on = order_num
                newitem.paid = False
                newitem.save()
                messages.success(request, 'product added successfully!......')
                return redirect('product')
        else:
            newcart = Cart()
            newcart.user = request.user
            newcart.product = product
            newcart.price = product.price
            newcart.amount = product.price * quant
            newcart.quantity = quant
            newcart.order_on = order_num
            newcart.title_g = product.title_r
            newcart.paid = False
            newcart.save()
            messages.success(request, 'product added successfully!........')
            return redirect('product')
    return redirect('product')

@login_required(login_url='signin')
def shopcart(request):
    profile = Profile.objects.get(user__username = request.user.username)
    trolley = Cart.objects.filter(user__username = request.user.username, paid=False)

    subtotal = 0
    vat = 0
    total = 0

    for cart in trolley:
        subtotal += cart.price * cart.quantity

    vat = 0.075 * subtotal

    total = subtotal + vat 

    context = {
        'trolley':trolley,
        'profile':profile,
        'subtotal':subtotal,
        'vat':vat,
        'total':total,
    }

    return render(request, 'displaycart.html', context)

@login_required(login_url='signin')
def deleteitem(request):
    if request.method == 'POST':

        item_id = request.POST['item_id']
        item_delete = Cart.objects.get(pk=item_id)
        item_delete.delete()
        messages.success(request, 'Cart deleted successfully!......')
        return redirect('shopcart')

@login_required(login_url='signin')
def change(request):
    if request.method == 'POST':
        item_id = request.POST['item_id']
        quant = int(request.POST['quant'])
        modify = Cart.objects.get(pk=item_id)
        modify.quantity += quant
        modify.amount = modify.price * modify.quantity
        modify.save()
        messages.success(request, 'Cart modified successfully!......')
        return redirect('shopcart')

@login_required(login_url='signin')
def checkout(request):
    profile = Profile.objects.get(user__username = request.user.username)
    trolley = Cart.objects.filter(user__username = request.user.username, paid=False)

    subtotal = 0
    vat = 0
    total = 0

    for cart in trolley:
        subtotal += cart.price * cart.quantity

    vat = 0.075 * subtotal

    total = subtotal + vat 

    context = {
        'trolley':trolley,
        'profile':profile,
        'total':total,
    }

    return render(request, 'checkout.html', context)

@login_required(login_url='signin')
def pay(request):
    if request.method == 'POST':
        api_key = 'sk_test_c954256f1310ef10e5081494b9dbfd15d7f696c1'
        curl = 'https://api.paystack.co/transaction/initialize'
        cburl = 'http://54.173.247.14/callback/'
        # cburl = 'http://127.0.0.1:8000/callback/'
        ref = str(uuid.uuid4())
        profile = Profile.objects.get(user__username = request.user.username)
        shop_code = profile.id 
        total = float(request.POST['total']) * 100
        user = User.objects.get(username=request.user.username)
        first_name = user.first_name
        last_name = user.last_name
        phone = request.POST['phone']
        headers = {'Authorization': f'Bearer {api_key}'}
        data = {'reference': ref, 'callback_url': cburl, 'email': user.email, 'amount': int(total), 'order_number': shop_code, 'currency': 'NGN'}

        try :
            r = requests.post(curl, headers= headers, json= data)
        except Exception:
            messages.error(request, 'Network busy, Try again later')
        else:
            transback = json.loads(r.text)
            rdurl = transback['data']['authorization_url']

            account = Payment()
            account.user = user
            account.first_name = user.first_name
            account.last_name = user.last_name
            account.phone = phone
            account.amount = total/100
            account.paid = True
            account.pay_code = ref
            account.shop_code = shop_code
            account.save()
            return redirect(rdurl)
    return redirect('checkout')

@login_required(login_url='signin')
def callback(request):
    profile = Profile.objects.get(user__username = request.user.username)
    trolley = Cart.objects.filter(user__username = request.user.username, paid = False)
    payment = Payment.objects.filter(user__username = request.user.username, paid = True)

    for items in trolley:
        items.paid = True
        items.save()

        stock = Product.objects.get(pk = items.product_id)
        stock.max_quantity -= items.quantity 
        stock.save()

    context = {
        'profile':profile,
        'trolley':trolley,
    }
    return render(request, 'callback.html', context)

def search(request):
    if request.method =='POST':
        items = request.POST['search']
        searched = Q(Q(title_r__icontains=items) | Q(price__icontains = items) | Q(slug__icontains = items))
        searched_items = Category.objects.filter(searched)
        context = {
            'items':items,
            'searched_items':searched_items,
        }
        return render(request, 'search.html', context)
    else:
        return render(request,'search.html')

def history(request):
    profile = Profile.objects.get(user__username= request.user.username)
    trolley = Cart.objects.filter(user__username = request.user.username, paid = True)

    subtotal = 0
    vat = 0
    total = 0

    for items in trolley:
        subtotal += items.price * items.quantity

        vat = 0.075 * subtotal

        total = subtotal + vat

        context ={
            'trolley':trolley,
            'total':total,
            'profile':profile,
        }
        return render(request, 'history.html', context)












































































































































    # def contact(request):
    #     form = ContactForm()
    #     if request.method == 'POST':
    #         form = ContactForm(request.POST)
    #         if form.is_valid:
    #             form.save()
    #             messages.success(request, 'Thanks you for contactin us!......')
    #             return redirect('index')
    #         else:
    #             messages.error(request, form.error)
    #             return redirect('index')
    #     return redirect('index')

    # category = Category.objects.all() = query 
    # query_set =  Models.objects(manager).methods of query
    # (i.e all, filter, exclude, get)

    # querie
    # query_sets
