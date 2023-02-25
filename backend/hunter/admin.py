from django.contrib import admin
from .models import Product
from .models import Website
from .models import TagData
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'availability', 'url', 'price', 'dateCreated', 'dateUpdated', 'website')
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'url', 'relatedTagData')
class TagDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'productTag', 'nameTag', 'priceTag', 'availabilityTag', 'urlTag', 'relatedWebsite')

# Register your models here.

admin.site.register(Product, ProductAdmin)
admin.site.register(Website, WebsiteAdmin)
admin.site.register(TagData, TagDataAdmin)