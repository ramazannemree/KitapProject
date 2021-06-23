from basket.models import Basket
from django.contrib import messages
from django.db.models.aggregates import Count
from django.http.response import HttpResponse
from products.models import Category, Product,ProductImages
from products.forms import addProductForm,ImageForm
from comment.models import Comment
from comment.forms import CommentForm
from django.shortcuts import redirect, render
from django.forms import modelformset_factory
from django.db.models import Avg,Max,Min
from favorites.models import Favorites
from django.contrib.auth.decorators import login_required
import json
from basket.views import basket_product_list

def home(request):
    products_in_basket,products_count,total_price = basket_product_list(request)
    categories = Category.objects.all()
    context ={
        'total_price' : total_price,
        'products_in_basket' : products_in_basket,
        'products_count' : products_count,
        'categories' : categories
    }
    return render(request,'products/homepage.html',context)

#My products
@login_required(login_url='home')
def view_products(request):
    products_in_basket,products_count,total_price = basket_product_list(request)
    products = Product.objects.filter(user_id=request.user.id)
    
    if request.method == 'POST':
        ordering = request.POST['ordering']
        if ordering == "Eklenme Tarihi":
            products = products.order_by('-updated_time')
        elif ordering == "Ürün Adı":
            products = products.order_by('product_name')
        elif ordering == "Fiyat":
            products = products.order_by('price')  
    context = {
        'total_price' : total_price,
        'products_in_basket' : products_in_basket,
        'products_count' : products_count,
        'products': products, 
    }
    return render(request,'products/my_products.html',context)

#Add_product_yönlendirme
def add_product_yonlendirme(request,form,Image_formset):
    products_in_basket,products_count,total_price = basket_product_list(request)
    if request.method == 'POST':
        form = border_form_input(form)
    formset = Image_formset(queryset=ProductImages.objects.none())
    context = {
        'total_price' : total_price,
        'products_in_basket' : products_in_basket,
        'products_count' : products_count,
        'form' : form,
        'formset' : formset,
    }
    return render(request, "products/add-product.html",context)

#Add_image
def add_image(formset,form_save):
    for form_image in formset.cleaned_data:
        if form_image:
            image = form_image['image']
            photo = ProductImages(product = form_save, image=image)
            photo.save()

#Add product
@login_required(login_url='home')
def add_product(request):
    ImageFormSet = modelformset_factory(ProductImages,form=ImageForm,extra=5)
    form = addProductForm(data=request.POST or None)
    if request.method == 'POST':
        formset = ImageFormSet(request.POST, request.FILES, queryset=ProductImages.objects.none())
        if form.is_valid() and formset.is_valid():
            form_save = form.save(commit=False)
            form_save.user = request.user
            if formset[0].cleaned_data.get('image') != None: 
                pass

            else:
                messages.success(request,"En az bir ürün fotoğrafı eklemeniz gerekmektedir.",extra_tags="danger")
                form = addProductForm(data=request.POST)
                return add_product_yonlendirme(request,form,ImageFormSet)

            try:
                form.save()  

            except Exception as e:
                messages.success(request,str(e),extra_tags="danger")
                form = addProductForm()
                return add_product_yonlendirme(request,form,ImageFormSet)

            add_image(formset,form_save)
            messages.info(request,"Ürün başarılı bir şekilde eklenmiştir. Bizi tercih ettiğiniz için teşekkür ederiz.",extra_tags="info")
            return redirect('add_product')

        else:
            form = addProductForm(request.POST or None)
            return add_product_yonlendirme(request,form,ImageFormSet)
    else:
        form = addProductForm()
    return add_product_yonlendirme(request,form,ImageFormSet)

#Edit product
@login_required(login_url='home')
def edit_product(request,id):
    products_in_basket,products_count,total_price = basket_product_list(request)
    product = Product.objects.get(id=id)
    form = addProductForm(instance=product)
    if request.user == product.user:
        if request.method == 'POST':
            form = addProductForm(request.POST, instance=product)
            if form.is_valid():
                try:
                    form.save()
                except Exception as e:
                    messages.success(request,"Bir hata oluştu! Lütfen tekrar deneyin.",extra_tags="danger")
                    form = addProductForm(instance=product)
                    context = {
                        'total_price' : total_price,
                        'products_in_basket' : products_in_basket,
                        'products_count' : products_count,
                        'form' : form,
                    }
                    return render(request, "product/edit_product.html",context)
                messages.info(request,"Ürün başarılı bir şekilde güncellenmiştir.",extra_tags="info")
                return redirect('view_products')
            else:
                messages.success(request,"Bir hata oluştu! Lütfen tekrar deneyin.",extra_tags="danger")
                return redirect('view_products')
        context = {
            'total_price' : total_price,
            'products_in_basket' : products_in_basket,
            'products_count' : products_count,
            'form' : form,
        }
        return render(request, 'products/edit_product.html',context)
    else:
        messages.success(request,"Bu sayfaya erişim izniniz bulunmamaktadır!",extra_tags="danger")
        return redirect('home')

#Delete product
@login_required(login_url='home')
def delete_product(request,id):
    products_in_basket,products_count,total_price = basket_product_list(request)
    product = Product.objects.get(id=id)
    if request.user == product.user:
        if request.method == 'POST':
            product.delete()
            return redirect("view_products")
        context = {
            'total_price' : total_price,
            'products_in_basket' : products_in_basket,
            'products_count' : products_count,
            'product' : product
        }
        return render(request,'products/delete_product.html',context)
    else:
        messages.success(request,"Bu sayfaya erişim izniniz bulunmamaktadır!",extra_tags="danger")
        return redirect('home')

def context_al(request,reviews,product,images,categories,form,is_favorite,is_basket):
    products_in_basket,products_count,total_price = basket_product_list(request)
    avg_rate = reviews.aggregate(Avg('rate'))
    
    if avg_rate["rate__avg"] is not None:
        avg_rate= round(avg_rate["rate__avg"])
    else :
        avg_rate= 0

    ratelist=[]

    for i in range(5,0,-1):
        ratelist.append(reviews.filter(rate=i).count()*100)
    
    context = {
                'total_price' : total_price,
                'products_in_basket' : products_in_basket,
                'products_count' : products_count,
                'reviews' : reviews,
                'product' : product,
                'images' : images,
                'categories' : categories,
                'form' : form,
                'avg_rate': avg_rate,
                'ratelist' : ratelist,
                'is_favorite' : is_favorite,
                'is_basket' : is_basket,
            }
    return render(request,'products/single_product.html',context)

#Single product
def detail_product(request,id):
    product = Product.objects.get(id=id)
    images = ProductImages.objects.filter(product_id=id)
    categories = product.categories.all()
    form = CommentForm(data=request.POST or None)
    reviews = Comment.objects.filter(product_id=id)
    is_favorite = False
    is_basket = False
    if request.user.is_authenticated:
        if Favorites.objects.filter(product_id=product.id,user=request.user).exists():
            is_favorite= True
        if Basket.objects.filter(product_id=product.id,user=request.user).exists():
            is_basket = True
    if request.method == 'POST':
        if form.is_valid():
            form_save = form.save(commit=False)
            form_save.user=request.user
            form_save.product_id = id
            form.save()
            messages.success(request,'Yorumunuz başarılı bir şekilde alınmıştır. Teşekkür ederiz.')
            return redirect('detail_product',id)
        else:
            messages.success(request,'Puan vermeniz gerekmektedir.',extra_tags='danger')
            return context_al(request,reviews,product,images,categories,form,is_favorite,is_basket)
    else:
        form=CommentForm()
    return context_al(request,reviews,product,images,categories,form,is_favorite,is_basket)

def border_form_input(form):
    for field in form:
        if field.errors:
            form.fields[field.name].widget.attrs["class"]+=" is-invalid"
        else:
            form.fields[field.name].widget.attrs["class"]+=" is-valid"
    return form

def cat_page_prep(products):
    min_price = products.aggregate(Min('price'))['price__min']
    max_price = products.aggregate(Max('price'))['price__max']
    authors = products.values('author',).annotate(Count('id')).order_by().filter(id__count__gt=0)
    categories = Product.objects.values('categories__category_name','categories__slug').annotate(Count('id')).order_by().filter(id__count__gt=0)
    
    return min_price,max_price,authors,categories

def category_page(request,slug):
    products_in_basket,products_count,total_price = basket_product_list(request)
    products = Product.objects.filter(categories__slug = slug)
    name = products[0].categories.all()
    
    rate = Comment.objects.filter(product__categories__slug = slug)
    rate_list = []
    min_price,max_price,authors,categories = cat_page_prep(products)
    
    if request.method == "POST":
        min_p = request.POST["min_price"]
        max_p = request.POST["max_price"]
        if "author" in request.POST.keys():
            aut = request.POST.getlist('author')
            products = products.filter(price__gte = min_p, price__lte = max_p, author__in = aut)
        else:
            products = products.filter(price__gte = min_p,price__lte = max_p)

    for i in products:
        is_fav =  False
        is_basket =  False
        if request.user.is_authenticated:
            if Favorites.objects.filter(product_id=i.id,user=request.user).exists():
                is_fav= True
            if Basket.objects.filter(product_id=i.id,user=request.user).exists():
                is_basket = True
        reviews=rate.filter(product_id = i.id)
        avg_rate = reviews.aggregate(Avg('rate'))
        if avg_rate["rate__avg"]:
            pass
        else:
            avg_rate["rate__avg"] = 0
        rate_list.append({'product':i,'rate':avg_rate,'fav':is_fav,'basket':is_basket})
    context = {
        'total_price' : total_price,
        'products_in_basket' : products_in_basket,
        'products_count' : products_count,
        'authors' : authors,
        'min_price' : min_price,
        'max_price' : max_price,
        'categories' : categories,
        'rate_list' : rate_list,
        'name' : name[0]
    }
    return render(request,'products/categorypage.html',context)

## ş harfini kabul etmiyor!!
def search(request):
    products_in_basket,products_count,total_price = basket_product_list(request)
    rate_list = []
    if request.method == "POST":
        query = request.POST['search']
        if len(query)<3:
            messages.success(request,"En az 3 karakter girmeniz gerekmektedir.",extra_tags="danger")
            return redirect('home')
        else:
            products = Product.objects.filter(product_name__icontains = query) | Product.objects.filter(author__icontains = query)
            if products.count() < 1:
                messages.success(request,"Aradığınız ürün bulunmamaktadır.",extra_tags="danger")
                return redirect('home')
            rate = Comment.objects.filter(product__product_name__icontains = query)
            min_price,max_price,authors,categories = cat_page_prep(products)
        
            for i in products:
                is_fav =  False
                if request.user.is_authenticated:
                    if Favorites.objects.filter(product_id=i.id,user=request.user).exists():
                        is_fav= True
                reviews=rate.filter(product_id = i.id)
                avg_rate = reviews.aggregate(Avg('rate'))
                if avg_rate["rate__avg"]:
                    pass
                else:
                    avg_rate["rate__avg"] = 0
                rate_list.append({'product':i,'rate':avg_rate,'fav':is_fav})
            context ={
                'total_price' : total_price,
                'products_in_basket' : products_in_basket,
                'products_count' : products_count,
                'authors' : authors,
                'min_price' : min_price,
                'max_price' : max_price,
                'categories' : categories,
                'rate_list' : rate_list
            }
            return render(request,'products/categorypage.html',context)
    return redirect('home')

##yanlış yerde açılıyor
def auto_complete(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(product_name__icontains=q)
        results = []
        for p in products:
            products_json = {}
            products_json = p.product_name
            results.append(products_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
