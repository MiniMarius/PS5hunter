from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
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

    def create(self, request):
        try:
            website = Website.objects.get(url=request.data['url'])
            serializer = WebsiteSerializer(website)
            return Response(serializer.data, status=status.HTTP_409_CONFLICT)
        except Website.DoesNotExist:
            pass
        serializer = WebsiteSerializer(data=request.data)
        if serializer.is_valid():
            website = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def update(self, request, pk):
        try:
            website = Website.objects.get(url=request.data.get('url'))
        except Website.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = WebsiteSerializer(website, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, pk):
        url = request.data.get('url', None)
        if url is None:
            return Response({'error': 'url parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            websites = Website.objects.filter(url=url)
        except Website.DoesNotExist:
            return Response({'error': 'website does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        for website in websites:
            website.delete()
        
        return Response({'success': 'website deleted'}, status=status.HTTP_200_OK)

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