import json
from django.conf import settings
from django.utils.safestring import SafeString
from django.contrib.gis.geos import GEOSGeometry
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from django.contrib.gis.serializers import geojson

from django.urls import reverse

from cms.views import (
    BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView
)


from .models import Place, Area, Route
from .forms import PlaceForm, AreaForm, RouteForm
from .convert_geometry import ConvertGeometry


class GoogleApiMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['google_key'] = settings.GOOGLE_API_KEY
        return context


class PlaceListView(GoogleApiMixin, BaseListView):
    model = Place
    paginate_by = 100  # if pagination is desired


class PlaceCreate(GoogleApiMixin, BaseCreateView):
    model = Place
    form_class = PlaceForm

    def form_valid(self, form):
        lat = form.cleaned_data.get('lat')
        lng = form.cleaned_data.get('lng')
        wkt = "POINT({} {})".format(lng, lat)
        point = GEOSGeometry(wkt)
        point.srid = 4326
        form.instance.geom = point
        form.save()
        return super().form_valid(form)


class PlaceUpdate(GoogleApiMixin, BaseUpdateView):
    model = Place
    form_class = PlaceForm
    template_name = 'geo/place_form.html'

    def form_valid(self, form):
        lat = form.cleaned_data.get('lat')
        lng = form.cleaned_data.get('lng')
        wkt = "POINT({} {})".format(lng, lat)
        point = GEOSGeometry(wkt)
        point.srid = 4326
        form.instance.geom = point
        form.save()
        return super().form_valid(form)


class PlaceDelete(GoogleApiMixin, BaseDeleteView):
    model = Place


class AreaListView(GoogleApiMixin, BaseListView):

    model = Area
    paginate_by = 100  # if pagination is desired


class AreaCreate(GoogleApiMixin, BaseCreateView):
    model = Area
    form_class = AreaForm

    def form_valid(self, form):
        form.instance.name = self.request.POST['name']
        if self.request.is_ajax():
            polygon = self.request.POST.getlist('polygon[]')
            pnt = ConvertGeometry(polygon, 'polygon').convert_geometry()
            pnt.srid = 4326
            form.instance.geom = pnt
            form.save()
            return JsonResponse({
                'success': True,
                'url': reverse('area-list'),
            })
        return super().form_valid(form)


class AreaUpdate(GoogleApiMixin, BaseUpdateView):
    model = Area
    form_class = AreaForm
    template_name = 'geo/area_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        g = geojson.Serializer()
        geo_data = Area.objects.filter(pk=self.kwargs['pk'])
        data = g.serialize(
            geo_data, geometry_field='geom', fields=('name',))
        context['geom'] = SafeString(json.loads(data))
        return context

    def form_valid(self, form):
        form.instance.name = self.request.POST['name']
        if self.request.is_ajax():
            polygon = self.request.POST.getlist('polygon[]')
            pnt = ConvertGeometry(polygon, 'polygon').convert_geometry()
            pnt.srid = 4326
            form.instance.geom = pnt
            form.save()
            return JsonResponse({
                'success': True,
                'url': reverse('area-list'),
            })
        return super().form_valid(form)


class AreaDelete(GoogleApiMixin, BaseDeleteView):
    model = Area


class RouteListView(GoogleApiMixin, BaseListView):

    model = Route
    paginate_by = 100  # if pagination is desired


class RouteCreate(GoogleApiMixin, BaseCreateView):
    model = Route
    form_class = RouteForm

    def form_valid(self, form):
        form.instance.name = self.request.POST['name']
        if self.request.is_ajax():
            route = self.request.POST.getlist('route[]')
            pnt = ConvertGeometry(route, 'linestring').convert_geometry()
            pnt.srid = 4326
            form.instance.geom = pnt
            form.save()
            return JsonResponse({
                'success': True,
                'url': reverse('route-list'),
            })
        return super().form_valid(form)


class RouteUpdate(GoogleApiMixin, BaseUpdateView):
    model = Route
    form_class = RouteForm
    template_name = 'geo/route_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        g = geojson.Serializer()
        geo_data = Route.objects.filter(pk=self.kwargs['pk'])
        data = g.serialize(
            geo_data, geometry_field='geom', fields=('name',))
        context['geom'] = SafeString(json.loads(data))
        return context

    def form_valid(self, form):
        form.instance.name = self.request.POST['name']
        if self.request.is_ajax():
            route = self.request.POST.getlist('route[]')
            pnt = ConvertGeometry(route, 'linestring').convert_geometry()
            pnt.srid = 4326
            form.instance.geom = pnt
            form.save()
            return JsonResponse({
                'success': True,
                'url': reverse('route-list'),
            })
        return super().form_valid(form)


class RouteDelete(GoogleApiMixin, BaseDeleteView):
    model = Route


class HomeView(GoogleApiMixin, TemplateView):
    template_name = "place.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['places'] = Place.objects.all()
        context['form'] = PlaceForm()
        return context
