from django.contrib import admin
from .models import Product
from .models import Website
from .models import TagData
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'availability', 'url', 'price', 'date_created', 'date_updated', 'website')
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'url', 'related_tag_data')
class TagDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_tag', 'price_tag', 'availability_tag', 'url_tag', 'related_website')

# Register your models here.

admin.site.register(Product, ProductAdmin)
admin.site.register(Website, WebsiteAdmin)
admin.site.register(TagData, TagDataAdmin)