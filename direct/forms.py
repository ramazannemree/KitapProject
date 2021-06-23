from kullanici.models import User
from django.forms import ValidationError
from django import forms
from .models import ChatModel,Message

class CreateMessageForm(forms.ModelForm):
    msg_text = forms.CharField(label="Mesajınız", widget=forms.Textarea())
    class Meta:
        model = Message
        fields = ('msg_text',)
    def __init__(self,*args,**kwargs):
        super(CreateMessageForm,self).__init__(*args,**kwargs)
        self.fields["msg_text"].widget.attrs["rows"] = 7
        self.fields["msg_text"].widget.attrs["class"] = "form-control"
        self.fields["msg_text"].widget.attrs["placeholder"] = "Mesajınızı Yazın"

class CreateChatForm(forms.ModelForm):
    PRIORITY_SELECTIONS = [
        ("danger","Acil"),
        ("warning","Yüksek"),
        ("info","Orta"),
        ("success","Düşük")
    ]
    MESSAGE_TYPE_SELECTIONS = [
        ("Siteyle Alakalı Teknik Problem","Siteyle Alakalı Teknik Problem"),
        ("İşbirliği Talebi","İşbirliği Talebi"),
        ("Şikayet","Şikayet")
    ]
    priority = forms.CharField(label='Mesaj Öncelik Durumu',widget=forms.Select(choices=PRIORITY_SELECTIONS))
    message_type = forms.CharField(label='Mesaj Türü',widget=forms.Select(choices=MESSAGE_TYPE_SELECTIONS))
    first_message = forms.CharField(label="Mesajınız",widget=forms.Textarea())
    class Meta:
        model = ChatModel
        fields = ('subject', 'message_type', 'priority', 'first_message')
        labels = {
            'subject':'Mesajın Konusu',
            'message_type':'Mesaj Türü',
            'priority':'Mesaj Öncelik Durumu',
            'first_message':'Mesajınız'
        }


    def __init__(self,*args,**kwargs):
        super(CreateChatForm, self).__init__(*args,**kwargs)
        for field in self.fields :
            self.fields[field].widget.attrs = {'class':'form-control'}
            self.fields[field].required = True
        self.fields["first_message"].widget.attrs["rows"] = 7

