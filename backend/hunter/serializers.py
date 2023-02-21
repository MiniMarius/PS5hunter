from rest_framework import serializers
from .models import Product
from .models import Website
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'website', 'availability', 'url', 'price')
class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = ('id','name', 'url', 'html', 'date')
