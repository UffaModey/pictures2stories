# Register your models here.
from django.contrib import admin
from .models import Image, Story

admin.site.register(Image)
admin.site.register(Story)