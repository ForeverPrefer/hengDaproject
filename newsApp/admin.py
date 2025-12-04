from django.contrib import admin
from .models import MyNew

class MyNewAdmin(admin.ModelAdmin):
    list_display = ['title', 'newType', 'publishDate', 'views']
    list_filter = ['newType', 'publishDate']
    search_fields = ['title']

admin.site.register(MyNew, MyNewAdmin)