"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from hunter import views

router = routers.DefaultRouter()
router.register(r'product', views.ProductView, 'product')
router.register(r'website', views.WebsiteView, 'website')
router.register(r"tagdata", views.TagDataView, "tagdata")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('run_scraper/', views.run_scraper, name='run_scraper'),
    path('create_scraping_object/', views.create_scraping_object, name='create_scraping_object')
]