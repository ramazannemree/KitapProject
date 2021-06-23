from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from favorites.models import Favorites
from products.models import Product
from basket.views import basket_product_list

@login_required(login_url='home')
def favorite_process(request,id):
    product = Product.objects.get(id=id)
    
    if Favorites.objects.filter(product_id=product.id,user=request.user).exists():
        Favorites.objects.get(product_id=product.id,user=request.user).delete()
    else:
        Favorites.objects.create(product=product,user=request.user)
        
def add_favorite(request,id):
    favorite_process(request,id)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER","/products"))

def favorite_list(request):
    products_in_basket,products_count,total_price = basket_product_list(request)
    favorites = Favorites.objects.filter(user=request.user)
    favarites_count = favorites.count()
    products=[]
    for i in favorites:
        products.append(i.product)
    context = {
        'total_price' : total_price,
        'products' : products_in_basket,
        'products_count' : products_count,
        'favorites' : products,
        'favarites_count' : favarites_count,
        'user' : request.user
    }
    return render(request,'products/favorite_list.html',context)