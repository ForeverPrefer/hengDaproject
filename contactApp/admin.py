from django.contrib import admin
from .models import Ad

admin.site.register(Ad)

from django.utils.safestring import mark_safe
from .models import Resume

class ResumeAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'personID', 'birth', 'edu', 'school', 
                   'major', 'position', 'image_data')
    
    def image_data(self, obj):
        return mark_safe(f'<img src="{obj.photo.url}" width="120px"/>')
    image_data.short_description = '个人照片'

admin.site.register(Resume, ResumeAdmin)