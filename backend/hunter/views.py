from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets
from .serializers import ProductSerializer
from .serializers import WebsiteSerializer
from .serializers import TagDataSerializer
from .models import Product
from .models import Website
from .models import TagData
from .scraper import Scraper
# Create your views here.

class ProductView(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

class WebsiteView(viewsets.ModelViewSet):
    serializer_class = WebsiteSerializer
    queryset = Website.objects.all()

class TagDataView(viewsets.ModelViewSet):
    serializer_class = TagDataSerializer
    queryset = TagData.objects.all()

def run_scraper(request):
    # start scraper
    scraper = Scraper()
    if not scraper.check_inventory():
        return JsonResponse({'error': 'Something went wrong'}, status=500)
    
    response = {
        'status': 'success',
        'message': 'Scraper finished successfully!',
    }
    # return a success response
    return JsonResponse(response)

def getProducts(request):
    Scraper = Scraper()
    