from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Item, Message, UserRanking

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Item)
admin.site.register(Message)
admin.site.register(UserRanking)