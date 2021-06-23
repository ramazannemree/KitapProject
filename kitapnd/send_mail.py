

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator 
from kitapnd.utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings


def mail_gonder(user,body,subject="Mail Onayı",url_name="activate"):
    current_site = "localhost:8000"
    message = render_to_string('kullanici/mail.html',{'user': user,'body':body,'domain':current_site,'uid': urlsafe_base64_encode(force_bytes(user.pk)),'token':generate_token.make_token(user),'url_name':url_name})
    email = EmailMessage(subject,message,settings.EMAIL_HOST_USER,[user.email])
    try:
        email.send()
    except Exception as e:
        print("Mail gönderilemedi",str(e))
    