from django.db import models
from django.utils import timezone

# Create your models here.


class State(models.Model):
    slug = models.CharField(max_length=4, blank=False)
    created = models.DateTimeField(default=timezone.now)


class City(models.Model):
    name = models.CharField(max_length=153, blank=False)
    created = models.DateTimeField(default=timezone.now)
    state = models.ForeignKey(State, blank=False)


class Address(models.Model):
    address = models.TextField(max_length=200, blank=False)
    complement = models.TextField(max_length=200, blank=True)
    district = models.CharField(max_length=50, blank=False)
    cep = models.CharField(max_length=9, blank=False)
    city = models.ForeignKey(City, blank=False)