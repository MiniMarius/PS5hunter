from django.shortcuts import render
from rest_framework import viewsets
from .serializers import ProductSerializer
from .serializers import WebsiteSerializer
from .models import Product
from .models import Website
# Create your views here.

class ProductView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

class WebsiteView(viewsets.ModelViewSet):
    serializer_class = WebsiteSerializer
    queryset = Website.objects.all()
