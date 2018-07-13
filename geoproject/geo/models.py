from django.db import models
from django.contrib import gis


class Timestamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Place(Timestamped):
    '''
    Save Points
    '''
    name = models.CharField(max_length=100)
    geom = gis.db.models.GeometryField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Area(Timestamped):
    '''
    Save Polygons
    '''
    name = models.CharField(max_length=100)
    geom = gis.db.models.GeometryField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Route(Timestamped):
    '''
    Save LineStrings
    '''
    name = models.CharField(max_length=100)
    geom = gis.db.models.GeometryField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
