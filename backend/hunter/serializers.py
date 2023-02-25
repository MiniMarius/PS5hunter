from rest_framework import serializers
from .models import Product
from .models import Website
from .models import TagData
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'availability', 'url', 'price', 'date_created', 'date_updated', 'website')
class WebsiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Website
        fields = ('id','name', 'url', 'related_tag_data')
class TagDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagData
        fields = ('id', 'name_tag', 'price_tag', 'availability_tag', 'url_tag', 'related_website')