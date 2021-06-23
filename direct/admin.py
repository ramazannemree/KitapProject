from django.contrib import admin
from .models import ChatModel,Message
class MessageAdmin(admin.ModelAdmin):
    list_filter = ['is_staff',]
admin.site.register(ChatModel)
admin.site.register(Message,MessageAdmin)

# Register your models here.
