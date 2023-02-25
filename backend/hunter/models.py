from django.db import models
from django.utils import timezone

class Website(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)
    url = models.URLField()
    related_tag_data = models.OneToOneField('TagData', on_delete=models.CASCADE, related_name='website', null=True, blank=True)

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)
    availability = models.BooleanField()
    url = models.URLField()
    price = models.FloatField(default=0)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='product')

class TagData(models.Model):
    id = models.AutoField(primary_key=True)
    name_tag = models.TextField()
    price_tag = models.TextField()
    availability_tag = models.TextField()
    url_tag = models.TextField()
    related_website = models.OneToOneField('Website', on_delete=models.CASCADE, related_name='tagData')