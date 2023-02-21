from django.db import models


class Website(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)
    url = models.URLField()
    html = models.TextField()
    date = models.DateField()


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120)
    website = models.CharField(max_length=120)
    availability = models.BooleanField()
    url = models.URLField()
    price = models.FloatField(default=0)
