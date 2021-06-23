
from django.db import models
from django import forms
from django.forms import ModelForm
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
import json
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.forms import ValidationError
from django.templatetags.static import static
import re,os
from .models import User
#from django.core.exceptions import ValidationError
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
#class LoginForm(forms.)
class IlIlceChoiceField(forms.ChoiceField):
    def validate(self, value):
        pass
    # def validate(self, value):
    #     p = static('js/kullanici/il-ilce.txt')
    #     #content = p.readlines()
    #     with open(p[1:],"r",encoding="utf-8") as f:
    #         data = f.read()
    #         if value in data:
    #             return value
    #         else:
    #             raise ValidationError("Lütfen Doğru Seçim Yapınız")
             
class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=20,label="İsim")
    last_name = forms.CharField(max_length=20,label="Soyisim")
    email = forms.EmailField(max_length=50,label="Email")
    il = IlIlceChoiceField(label="İl")
    ilce = IlIlceChoiceField(label="İlçe",widget=forms.Select())
    phone = forms.CharField( max_length=12,label="Telefon No")
    adres = forms.CharField(max_length=300,widget=forms.Textarea())
    password = forms.CharField(label="Parola", widget=forms.PasswordInput, help_text="Parolanızı girin")
    sifre2 = forms.CharField(label="Parola Tekrar",widget=forms.PasswordInput,help_text="Parolanızı tekrar girin")
    password2 = None
    
    class Meta:
        model = User
        fields = ('first_name','last_name','phone','email','il','ilce','password','sifre2','adres')
    
        # labels = {
        #     "first_name": "İsim",
        #     "last_name" : "Soyisim",
        #     "email": "E-mail",
        #     "phone": "Telefon",
        #
        #
        # }
    def __init__(self,*args,**kwargs):
        super(RegisterForm, self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class':'form-control'}
            self.fields[field].required = True


        self.fields["email"].widget.attrs["placeholder"] = "test@deneme.com"
        self.fields["first_name"].widget.attrs["placeholder"] = "Adınız"
        self.fields["last_name"].widget.attrs["placeholder"] = "Soyadınız"
        self.fields["sifre2"].widget.attrs["placeholder"] = "Şifreniz Tekrar"
        self.fields["il"].widget.attrs["placeholder"] = "İl Seçiniz"
        #self.fields["il"].widget.attrs["id"] = "il_select"
        #self.fields["ilce"].widget.attrs["id"] = "ilce_select"
        self.fields["ilce"].widget.attrs["placeholder"] = "İlçe Seçiniz"
        self.fields["adres"].widget.attrs["placeholder"] = "Adres Giriniz"
        self.fields["phone"].widget.attrs["placeholder"] = "(5__)-___-____"
        self.fields["phone"].widget.attrs["class"] += " input-mask"
        self.fields['adres'].widget.attrs['rows'] = 7
        self.fields["password1"].required = False

      





    def clean(self):
 
       
        cleaned = self.cleaned_data
        print("Cleaned",self.cleaned_data)
        sifre = cleaned.get("password")
        tekrar_sifre = cleaned.get("sifre2")
        if sifre is None or tekrar_sifre is None:
            #self.add_error("password1","Şifre Alanı Boş Bırakılamaz")
            #self.add_error("sifre2", "Şifre Alanı Boş Bırakılamaz")
            raise ValidationError("")
        if sifre != tekrar_sifre:
            self.add_error("password","Şifreler Uyuşmuyor")
            self.add_error("sifre2", "Şifreler Uyuşmuyor")
            raise ValidationError("")

    def clean_phone(self):
        
        phone = self.cleaned_data["phone"]

        return phone.replace("-","")

    # def clean_email(self):
    #
    #     email = self.cleaned_data["email"]
    #     email = value.lower()
    #     if User.objects.filter(email=email).exists():
    #
    #         raise forms.ValidationError("Email Sistemde Kayıtlı.")
    #     return email


class LoginForm(forms.Form):
    email = forms.CharField(required=True,max_length=40,label="Email",
                            widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email Adresini Giriniz'}))
    password = forms.CharField(required=True,max_length=40,label="Password",
                            widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Şifrenizi Giriniz'}))

    # def clean(self):
    #     email = self.cleaned_data.get("email")
    #     password = self.cleaned_data.get("password")
    #     validate_email(email)
    def clean_email(self):
        email = self.cleaned_data.get("email").strip()
       # validate_email(email)
        return email
    def clean_password(self):
        password = self.cleaned_data.get("password")
        #validate_password(password)
        return password












class ProfilUpdateForm(forms.ModelForm):
    #password = forms.CharField(required=False,max_length=40,label="Yeni Şifre",
     #                       widget=forms.PasswordInput())
    #password_again = forms.CharField(required=False,max_length=40,label="Şifre Tekrar",
    #                        widget=forms.PasswordInput())
    il = IlIlceChoiceField(label="İl")
    ilce = IlIlceChoiceField(label="İlçe",widget=forms.Select())
    resim = forms.ImageField()
    class Meta:
        model = User
        fields = ['resim','first_name','last_name','email','phone','il','ilce','adres']



    def __init__(self,*args,**kwargs):
        super(ProfilUpdateForm, self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class':'form-control'}
            #self.fields[field].required = False


        self.fields["resim"].required = False
        self.fields["first_name"].widget.attrs["placeholder"] = "Adınız"
        self.fields["last_name"].widget.attrs["placeholder"] = "Soyadınız"
        #self.fields["password"].widget.attrs["placeholder"] = "Yeni Şifre"
        #self.fields["password_again"].widget.attrs["placeholder"] = "Şifre Tekrar"
        self.fields["email"].widget.attrs["readonly"] = True
        self.fields["phone"].widget.attrs["placeholder"] = "(5__)-___-____"
        self.fields["phone"].widget.attrs["class"] += " input-mask"
        self.fields['adres'].widget.attrs['rows'] = 7

    # def clean(self):
    #
    #     cleaned = self.cleaned_data
    #     print("Cleaned", self.cleaned_data)
    #     sifre = cleaned.get("password")
    #     tekrar_sifre = cleaned.get("password_again")
    #     if sifre is None or tekrar_sifre is None:
    #         self.add_error("password","Şifre Alanı Boş Bırakılamaz")
    #         self.add_error("password_again", "Şifre Alanı Boş Bırakılamaz")
    #         raise ValidationError("")
    #     if sifre != tekrar_sifre:
    #         self.add_error("password", "Şifreler Uyuşmuyor")
    #         self.add_error("password_again", "Şifreler Uyuşmuyor")
    #         raise ValidationError("")