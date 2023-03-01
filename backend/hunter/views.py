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
    scraper = Scraper()

    try:
        products_added = scraper.run_scraper()
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=500)
    except Exception:
        return JsonResponse({'error': 'Something went wrong'}, status=500)

    if products_added:
        response = {
            'status': 'success',
            'message': 'Products added successfully!',
        }
    else:
        response = {
        'status': 'success',
        'message': 'Products were updated successfully!',
        }
    
    return JsonResponse(response)

def create_scraping_object(request):
    scraper = Scraper()
    scraper.create_scraping_object
    response = {
        'status': 'success',
        'message': 'Scraping object created successfully!',
    }

    return JsonResponse(response)

    
    