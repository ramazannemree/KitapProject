from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from .models import Basket
from products.models import Product
from kullanici.models import User

@login_required(login_url='home')
def basket_process(request,id):
    product = Product.objects.get(id=id)
    
    if Basket.objects.filter(product_id=product.id,user=request.user).exists():
        Basket.objects.get(product_id=product.id,user=request.user).delete()
    else:
        Basket.objects.create(product=product,user=request.user)
        
def add_basket(request,id):
    basket_process(request,id)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER","/products"))

def basket_list(request):
    products_in_basket,products_count,total_price = basket_product_list(request)
    context = {
        'total_price' : total_price,
        'products' : products_in_basket,
        'products_count' : products_count,
        'user' : request.user
    }

    return render(request,'products/basket.html',context)


def basket_product_list (request):
    products = None
    products_count = 0
    products_in_basket = []
    total_price = 0
    if request.user.is_authenticated:
        products = Basket.objects.filter(user=request.user)
        products_count = products.count()
        for i in products:
            products_in_basket.append(i.product)
            total_price += i.product.price
    
    return products_in_basket, products_count, total_price

def navbar_basket(request):
    products_in_basket, products_count, total_price = basket_product_list(request)
    context = {
        'total_price' : total_price,
        'products' : products_in_basket,
        'products_count' : products_count,
    }
    return context


def basket_details(request):
    context = navbar_basket(request)
    return render(request,'products/checkout-details.html',context)

def basket_payment(request):
    context = navbar_basket(request)
    return render(request,'products/checkout-payment.html',context)

def basket_review(request):
    context = navbar_basket(request)
    return render(request,'products/checkout-review.html',context)

def basket_complete(request):
    context = navbar_basket(request)
    return render(request,'products/checkout-complete.html',context)