from django.db import models
from django.utils import timezone
class Website(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)
    url = models.URLField()
    relatedTagData = models.OneToOneField('TagData', on_delete=models.CASCADE, related_name='website', null=True, blank=True)

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)
    availability = models.BooleanField()
    url = models.URLField()
    price = models.FloatField(default=0)
    dateCreated = models.DateTimeField(default=timezone.now)
    dateUpdated = models.DateTimeField(auto_now=True)
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='product')

class TagData(models.Model):
    id = models.AutoField(primary_key=True)
    relatedWebsite = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='tagData', null=True)
    
    nameTag = models.CharField(max_length=100, null=True)
    nameFilter = models.JSONField(null=True)
    
    priceTag = models.CharField(max_length=100, null=True)
    priceFilter = models.JSONField(null=True)
    
    availabilityTag = models.CharField(max_length=100, null=True)
    availabilityFilter = models.JSONField(null=True)
    
    urlTag = models.CharField(max_length=100, null=True)
    urlFilter = models.JSONField(null=True)