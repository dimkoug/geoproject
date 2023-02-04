from django.core.serializers import serialize
from cached_property import cached_property_with_ttl
from django.contrib.gis.db import models
from django.urls import reverse_lazy


class Geo(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    raw_geom = models.GeometryField(srid=2100)
    geom = models.GeometryField(srid=4326)
    sgeom = models.GeometryField(srid=4326, null=True, blank=True)
    center = models.GeometryField(srid=4326)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Diamerismata(models.Model):
    objectid = models.IntegerField()
    code_diam = models.CharField(max_length=255)
    name_diam = models.CharField(max_length=255)
    code_gdiam = models.CharField(max_length=255)
    code_ota = models.CharField(max_length=255)
    code_nom = models.CharField(max_length=255)
    name_ota = models.CharField(max_length=255)
    name_nom = models.CharField(max_length=255)
    name_gdiam = models.CharField(max_length=255)
    type_land = models.IntegerField()
    type_ota = models.CharField(max_length=255)
    code_edra = models.CharField(max_length=255)
    name_edra = models.CharField(max_length=255, blank=True, null=True)
    area_diam = models.FloatField()
    shape_leng = models.FloatField()
    shape_area = models.FloatField()
    rowid = models.IntegerField()
    objectid_1 = models.IntegerField()
    code_dia_1 = models.CharField(max_length=255)
    frequency = models.IntegerField()
    sum_shape = models.FloatField()
    sum_shape1 = models.FloatField()
    raw_geom = models.MultiPolygonField(srid=2100)

    class Meta:
        verbose_name = 'Διαμέρισμα'
        verbose_name_plural = 'Διαμερίσματα'

    def __str__(self):
        return '{}-{}-{}'.format(self.name_gdiam, self.name_nom, self.name_ota)


class Category(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ['name']
        default_related_name = 'categories'
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.name



class Location(Geo):
    parent = models.ForeignKey("self", related_name='children',
                               on_delete=models.CASCADE, null=True, blank=True)
    poi = models.ManyToManyField("Poi", through="LocationPoi", null=True)

    class Meta:
        default_related_name = 'locations'
        verbose_name = 'location'
        verbose_name_plural = 'locations'

    def get_geojson(self):
        return serialize('geojson', [self],
                         geometry_field='sgeom',
                         fields=('name',))


class LocationPoi(models.Model):
    location = models.ForeignKey("Location", on_delete=models.CASCADE)
    poi = models.ForeignKey("Poi", on_delete=models.CASCADE)


    class Meta:
        default_related_name = 'locationpoi'
        constraints = [
            models.UniqueConstraint(fields=['location', 'poi'], name="locationpoi")
        ]
        indexes = [
            models.Index(fields=['location', 'poi']),
        ]

class Poi(Geo):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, db_index=True)

    class Meta:
        default_related_name = 'poi'
        verbose_name = 'Poi'
        verbose_name_plural = 'Poi'
        # indexes = [
        #     GistIndex(fields=['geom'])
        # ]

    def __str__(self):
        return self.name

    @cached_property_with_ttl(ttl=86400)
    def get_geojson(self):
        return serialize('geojson', [self],
                          geometry_field='geom',
                          fields=('name',))

