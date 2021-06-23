
from django.forms.fields import IntegerField
from django.forms.widgets import CheckboxInput
from products.models import Product,ProductImages,Category
from django import forms

class addProductForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),widget=forms.CheckboxSelectMultiple,required=True,label="Kategori")
    product_name = forms.CharField(max_length=100,label="Başlık")
    keywords = forms.CharField(max_length=100,label="Anahtar kelimeler")
    description = forms.CharField(max_length=100,label="Açıklama")
    price = forms.FloatField(label="Fiyat")
    amount = forms.IntegerField(label="Adet")
    detail = forms.CharField(widget=forms.Textarea(),label="Detay")

    class Meta:
        model = Product
        fields = ['categories','product_name','keywords','description','price','amount','detail']

    def __init__(self,*args,**kwargs):
        super(addProductForm, self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class':'form-control'}
            self.fields[field].required = True
        self.fields['detail'].widget.attrs['rows'] = 7
        self.fields['categories'].widget.attrs['class'] = ""

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label="Resim")
    class Meta:
        model = ProductImages
        fields = ['image',]

