from django.contrib import admin
from .models import Product
from .models import Website

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'website', 'availability', 'url', 'price')
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'url', 'html', 'date')

# Register your models here.

admin.site.register(Product, ProductAdmin)
admin.site.register(Website, WebsiteAdmin)