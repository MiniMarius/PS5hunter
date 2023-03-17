from rest_framework import serializers
from .models import Product
from .models import Website
from .models import TagData
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
class TagDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagData
        fields = ['productTag', 'productFilter', 'nameTag', 'nameFilter', 'priceTag', 'priceFilter', 'availabilityTag', 'availabilityFilter', 'urlTag', 'urlFilter']
class WebsiteSerializer(serializers.ModelSerializer):
    relatedTagData = TagDataSerializer()

    class Meta:
        model = Website
        fields = ('name', 'url', 'relatedTagData')

    def create(self, validated_data):
        tag_data_data = validated_data.pop('relatedTagData')
        tag_data = TagData.objects.create(**tag_data_data)

        website = Website.objects.create(relatedTagData=tag_data, **validated_data)
        return website

    def update(self, instance, validated_data):
        tag_data_data = validated_data.pop('relatedTagData', None)
        if tag_data_data:
            tag_data_serializer = TagDataSerializer(instance.relatedTagData, data=tag_data_data)
            if tag_data_serializer.is_valid():
                tag_data = tag_data_serializer.save()
                validated_data['relatedTagData'] = tag_data
            else:
                raise serializers.ValidationError(tag_data_serializer.errors)

        return super().update(instance, validated_data)
        
    def delete(self, instance):
        instance.relatedTagData.delete()
        instance.delete()

class ProductSerializer(serializers.ModelSerializer):
    website = WebsiteSerializer()
    class Meta:
        model = Product
        fields = ('id', 'name', 'availability', 'url', 'price', 'dateCreated', 'dateUpdated', 'website')