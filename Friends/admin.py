from django.contrib import admin
from rest_framework.authtoken.models import TokenProxy

from .models import Story,  Friend

# Register your models here.
# admin.site.register(TokenProxy)
admin.site.register(Story)
# admin.site.register(Like)
# admin.site.register(Comment)
# admin.site.register(Reply)
admin.site.register(Friend)