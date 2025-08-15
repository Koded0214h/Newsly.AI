from django.contrib import admin
from .models import Topic, CustomUser, Article

# Register your models here.

admin.site.register(Topic)
admin.site.register(CustomUser)
admin.site.register(Article)