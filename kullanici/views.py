
from basket.views import basket_product_list
from .models import User
from django.views.generic import TemplateView,FormView
from .forms import RegisterForm,LoginForm,ProfilUpdateForm
from direct.forms import CreateChatForm
from time import time
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from kitapnd.send_mail import mail_gonder
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from kitapnd.utils import generate_token
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages
from django.urls import reverse_lazy,reverse
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect,HttpResponse,HttpResponseForbidden
from django.views.generic.edit import FormView
from direct.models import ChatModel,Message
from django.urls import reverse,reverse_lazy
from django.contrib.auth.decorators import login_required

# form invalid design
def border_form_input(form):
        for field in form:
            if field.errors:
                form.fields[field.name].widget.attrs["class"]+=" is-invalid"
                #form.fields[field.name].widget.attrs["style"]+="border:10px solid green"
            else:
                form.fields[field.name].widget.attrs["class"]+=" is-valid"
        return form

def KayitView(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/")
    form = RegisterForm(data=request.POST or None)
    if request.method == 'POST':
      
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            try:
                user.set_password(form.cleaned_data['password'])
                user.save()
            except Exception as e:
                messages.success(request,
                              "Bu mail adresi sistemimizde Kayıtlı",
                              extra_tags="danger")
                return render(request, "kullanici/register.html", context={'form': form})


            messages.info(request,"Mail Adresinize Aktivasyon Linki Gönderilmiştir. Üyeliğinizin Tamamlanması İçin Lütfen Onaylayınız",extra_tags="info")
            form = RegisterForm()

        else:

            form = border_form_input(form)     

    return render(request,"kullanici/register.html",context={'form':form})



class ActivateView(TemplateView):
    def get(self,request,uidb64,token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as e:
            user = None
        if user is not None and generate_token.check_token(user,token):
            user.is_active = True
            user.save()
            #success message
            # home ekranına yönlendirme !!!
            messages.success(request,"Üyelik Aktivasyonu Başarıyla Sağlandı",extra_tags="success")
            return redirect('register')

        return render(request,'kullanici/activate_failed.html',status=401)


def LoginView(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = None
            #messages.success(request,"Başarıyla Giriş Yaptınız. Anasayfaya Yönlendiriliyorsunuz.")
            email = form.cleaned_data.get("email")
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
            if not user:
                messages.success(request, "Bu Bilgilerde Kullanıcı Bulunamadı",
                                 extra_tags="danger")
                return render(request, "kullanici/login.html", context={'form': form})
            if not user.is_active:
                messages.success(request,"Mail adresinizi lütfen aktifleştiirin",extra_tags="warning")
                return render(request, "kullanici/login.html", context={'form': form})

            else:
                password = form.cleaned_data.get("password")
                kullanici = authenticate(username=user.username, password=password,
                                         backend='django.contrib.auth.backends.ModelBackend')
                if not kullanici:
                    messages.success(request, "Bu bilgilerde kullanıcıX bulunamadı", extra_tags="danger")
                    return render(request, "kullanici/login.html", context={'form': form})
                login(request,user,backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request,"Giriş Yaptığınız İçin Teşekkürler %s"%(user.first_name),extra_tags="success")
                return redirect('home')

        messages.success(request, "Kullanıcı Adı veya Parola Hatalı.", extra_tags="danger")
        return render(request, "kullanici/login.html", context={'form': form})
    else:

        form = LoginForm()
        return render(request,"kullanici/login.html",context={'form':form})

@login_required(login_url=reverse_lazy('login'))
def LogoutView(request):

    logout(request)
    messages.success(request,"Başarıyla Çıkış Yapıldı",extra_tags="success")
    return HttpResponseRedirect(reverse('login'))


def password_reset_request(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/")
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            
            data = password_reset_form.cleaned_data["email"]
            user = None
            try:
                user = User.objects.get(email=data)
            except:
                messages.success(request, "Bu mail adresi sistemimizde kayıtlı değil", extra_tags="danger")

            #print("DATA",data)
            if user:
                mail_gonder(user,body="Şifrenizi aşağıdaki bağlantıdan sıfırlayabilirsiniz.",url_name="password_reset_confirm")
                messages.success(request,"Şifre Sıfırlama Bağlantısı Mail Adresinize Gönderildi.",extra_tags="success")

            return render(request=request, template_name="kullanici/recovery_password_mail.html", context={"password_reset_form":password_reset_form})


    password_reset_form = PasswordResetForm()
           

    return render(request=request, template_name="kullanici/recovery_password_mail.html", context={"password_reset_form":password_reset_form})

@login_required(login_url=reverse_lazy('login'))
def ProfileView(request):
    if request.method == "GET":#update view

        user = User.objects.get(username=request.user.username)
        print("PROFİL IMAGE",user.profile.image)
        initial = {'first_name': user.first_name, 'last_name': user.last_name,
                   'email': user.email, 'phone': user.phone,'il':user.il.replace("i","İ").upper(),'ilce':user.ilce.replace("i","İ").upper(),'adres':user.adres,'resim':user.profile.image}
        form = ProfilUpdateForm(initial=initial)
        print("Burada")
        return render(request, "kullanici/profile/profile.html", {'form': form})


    if request.method == "POST":
        print(request.POST)
        form = ProfilUpdateForm(data=request.POST or None, files=request.FILES or None,instance=request.user)
        if form.is_valid():
            user = form.save(commit=True)
            image = form.cleaned_data.get("resim")
            if image:
                user.profile.image = image
                user.profile.save()

            messages.success(request,"Profiliniz Başarılı Bir Şekilde Güncellendi",extra_tags="success")
        else:
            messages.success(request,"Lütfen Aşağıdaki Hataları Düzeltin.",extra_tags="danger")
            form = border_form_input(form)

    return render(request,"kullanici/profile/profile.html",{"form":form})
#



@login_required(login_url=reverse_lazy('login'))
def CreateChatView(request):
    form = CreateChatForm(request.POST or None)
    try:
        chat = ChatModel.objects.filter(user=request.user)
    except Exception as e:
        chat = None
    if request.method == "POST":

        if form.is_valid():
            created_chat = form.save(commit=False)
            created_chat.user = request.user
            created_chat.save()
            form = CreateChatForm()
        else:
            messages.success(request,"Formunuz oluşturulamadı. Lütfen Hataları Düzeltin",extra_tags="danger")
            form = border_form_input(form)
    return render(request,"kullanici/profile/tickets.html",context={"form":form,"chats":chat})
from direct.forms import CreateMessageForm

@login_required(login_url=reverse_lazy('login'))
def SingleTicketView(request,id):

    try:
        chat = ChatModel.objects.get(id=id)
        mesajlar = Message.objects.filter(chat=chat)
    except:
        messages.success(request,"Destek Talebi Bulunamıyor. Yeni Bir Talep Oluşturabilirsiniz.",extra_tags="danger")
        return HttpResponseRedirect(reverse_lazy("destek"))
    if chat.user != request.user:
        return HttpResponseForbidden()
    mesaj_form = CreateMessageForm(request.POST or None)
    if request.method == "POST":
        if mesaj_form.is_valid():
            form = mesaj_form.save(commit=False)
            form.chat = chat
            form.is_staff = request.user.is_staff
            form.save()
            mesaj_form = CreateMessageForm()
    return render(request,"kullanici/profile/single-ticket.html",context={
        "chat":chat,"mesajlar":mesajlar,"mesaj_form":mesaj_form
    })
