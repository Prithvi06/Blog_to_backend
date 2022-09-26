from django.contrib import admin

# from django_markdown.admin import MarkdownModelAdmin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(BlogPost)
admin.site.register(Comment)
admin.site.register(Reply)