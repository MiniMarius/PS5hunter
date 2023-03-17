from django.shortcuts import render
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.throttling import UserRateThrottle
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer, WebsiteSerializer, TagDataSerializer
from .models import Product, Website, TagData
from .scraper import Scraper
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

@permission_classes([AllowAny])
@api_view(['POST'])
def create_user(request):
    # get the user data from the request
    username = request.data.get('username')
    password = request.data.get('password')

    # create the user
    user = User.objects.create_user(username=username, password=password)

    # return a response indicating success or failure
    if user:
        return Response({
            'success': True,
            'message': 'User created successfully.',
            'user_id': user.id,
            'username': user.username,
        }, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Failed to create user.'}, status=status.HTTP_400_BAD_REQUEST)

class ProductView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

class WebsiteView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
    serializer_class = TagDataSerializer
    queryset = TagData.objects.all()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
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