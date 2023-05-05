from django.contrib import admin

from .models import Story, Friend, Comment, Like

# Register your models here.
admin.site.register(Friend)
admin.site.register(Story)
admin.site.register(Like)
admin.site.register(Comment)
