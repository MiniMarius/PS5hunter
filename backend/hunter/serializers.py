from rest_framework import serializers
from .models import Product
from .models import Website
from .models import TagData

class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = ('id','name', 'url', 'relatedTagData')
class ProductSerializer(serializers.ModelSerializer):
    website = WebsiteSerializer()
    class Meta:
        model = Product
        fields = ('id', 'name', 'availability', 'url', 'price', 'dateCreated', 'dateUpdated', 'website')
class TagDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagData
        fields = ('id', 'productTag', 'productFilter', 'nameTag', 'nameFilter', 'priceTag', 'priceFilter', 'availabilityTag', 'availabilityFilter', 'urlTag', 'urlFilter', 'relatedWebsite')