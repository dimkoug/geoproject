import json
from django.urls import reverse
from django.core.serializers import serialize
from django.contrib.gis import geos
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.serializers import geojson
from django.contrib.gis.measure import Distance
from django.contrib import messages
from django.utils.safestring import SafeString
from django.http import HttpResponse, JsonResponse, Http404
from django.template.loader import render_to_string
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView

# Create your views here.

from core.mixins import GoogleApiMixin, PaginationMixin
from core.functions import get_pagination, is_ajax
from core.convert_geometry import ConvertGeometry

from core.views import (
    BaseListView, BaseCreateView, BaseUpdateView, BaseDeleteView
)


from .models import Poi, Location, Category

from .forms import RouteSearchForm, PolygonSearchForm, PoiForm


class LocationDetailView(DetailView):
    model = Location
    queryset = Location.objects.select_related('parent').prefetch_related('children', 'poi')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        data = self.get_object().children.values("id","name")
        if not data:
            context["poi"] = True
            data = self.get_object().poi.values("id", "name")
        paginator, num_pages, items_page = get_pagination(self.request,data,12)
        current_page = items_page
        page_no = current_page.number

        if num_pages <= 11 or page_no <= 6:  # case 1 and 2
            pages = [x for x in range(1, min(num_pages + 1, 12))]
        elif page_no > num_pages - 6:  # case 4
            pages = [x for x in range(num_pages - 10, num_pages + 1)]
        else:  # case 3
            pages = [x for x in range(page_no - 5, page_no + 6)]

        context['pages'] = pages
        context['data'] = items_page
        return context


class CategoryDetailView(DetailView):
    model = Category
    queryset = Category.objects.prefetch_related('poi')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["poi"] = True
        data = self.get_object().poi.values("id", "name")
        paginator, num_pages, items_page = get_pagination(self.request,data,12)
        current_page = items_page
        page_no = current_page.number

        if num_pages <= 11 or page_no <= 6:  # case 1 and 2
            pages = [x for x in range(1, min(num_pages + 1, 12))]
        elif page_no > num_pages - 6:  # case 4
            pages = [x for x in range(num_pages - 10, num_pages + 1)]
        else:  # case 3
            pages = [x for x in range(page_no - 5, page_no + 6)]

        context['pages'] = pages
        context['data'] = items_page
        return context


class PolygonView(TemplateView):
    template_name = "world/polygon.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class RouteView(TemplateView):
    template_name = "world/route.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class PoiListView(PaginationMixin,GoogleApiMixin, BaseListView):
    model = Poi
    paginate_by = 100  # if pagination is desired
    queryset = Poi.objects.select_related('category').order_by("-id")


class PoiCreateView(GoogleApiMixin, BaseCreateView):
    model = Poi
    form_class = PoiForm
    template_name = 'world/poi_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['geo_type'] = self.request.GET.get("geo_type")
        return context

    def form_valid(self, form):
        geo_type = self.request.POST["geo_type"]
        if geo_type == "point":
            lat = form.cleaned_data.get('lat')
            lng = form.cleaned_data.get('lng')
            wkt = "POINT({} {})".format(lng, lat)
            point = GEOSGeometry(wkt)
            point.srid = 4326
            form.instance.geom = point
            form.instance.raw_geom = point
            form.instance.center = point
        elif geo_type == "polygon":
            print("polygon")
            form.instance.name = self.request.POST['name']
            form.instance.category_id = self.request.POST['category']
            polygon = self.request.POST.getlist('polygon[]')
            pnt = ConvertGeometry(polygon, 'polygon').convert_geometry()
            pnt.srid = 4326
            form.instance.geom = pnt
            form.instance.raw_geom = pnt
            form.instance.center = pnt
        elif geo_type == 'linestring':
            route = self.request.POST.getlist('route[]')
            pnt = ConvertGeometry(route, 'linestring').convert_geometry()
            pnt.srid = 4326
            form.instance.geom = pnt
            form.instance.raw_geom = pnt
            form.instance.center = pnt
            form.instance.category_id = self.request.POST['category']
            if is_ajax(self.request):
                form.save()
                return JsonResponse({
                    'success': True,
                    'url': reverse('world:poi-list'),
                })
        if is_ajax(self.request):
                form.save()
                return JsonResponse({
                    'success': True,
                    'url': reverse('world:poi-list'),
                })
        else:
            form.save()
        print("hi")
        messages.success(self.request, f'Your {geo_type} was  saved successfully!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        if is_ajax(self.request):
            return JsonResponse(form.errors, safe=False, status=400)
        return super().form_invalid(form)


class PoiUpdateView(GoogleApiMixin, BaseUpdateView):
    model = Poi
    form_class = PoiForm
    template_name = 'world/poi_form.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        g = geojson.Serializer()
        data = g.serialize(
            [self.get_object()], geometry_field='geom', fields=('name',))
        context['geom'] = SafeString(json.loads(data))
        print(self.get_object().geom.__class__.__name__)
        context['geo_type'] = self.get_object().geom.__class__.__name__.lower()

        return context



    def form_valid(self, form):
        geo_type = self.request.POST["geo_type"]
        if geo_type == "point":

            lat = form.cleaned_data.get('lat')
            lng = form.cleaned_data.get('lng')
            wkt = "POINT({} {})".format(lng, lat)
            point = GEOSGeometry(wkt)
            point.srid = 4326
            form.instance.name = self.request.POST['name']
            form.instance.category_id = self.request.POST['category']
            form.instance.geom = point
            form.instance.raw_geom = point
            form.instance.center = point
        elif geo_type == "polygon":
            form.instance.name = self.request.POST['name']
            form.instance.category_id = self.request.POST['category']
            polygon = self.request.POST.getlist('polygon[]')
            pnt = ConvertGeometry(polygon, 'polygon').convert_geometry()
            pnt.srid = 4326
            form.instance.geom = pnt
            form.instance.raw_geom = pnt
            form.instance.center = pnt
        elif geo_type == 'linestring':
            route = self.request.POST.getlist('route[]')
            form.instance.name = self.request.POST['name']
            form.instance.category_id = self.request.POST['category']
            pnt = ConvertGeometry(route, 'linestring').convert_geometry()
            pnt.srid = 4326
            form.instance.geom = pnt
            form.instance.raw_geom = pnt
            form.instance.center = pnt
        
        if is_ajax(self.request):
            form.save()
            return JsonResponse({
                'success': True,
                'url': reverse('world:poi-list'),
            })
        else:
            form.save()
        messages.success(self.request, f'Your {geo_type} was  saved successfully!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        if is_ajax(self.request):
            return JsonResponse(form.errors, safe=False, status=400)
        return super().form_invalid(form)


class PoiDeleteView(GoogleApiMixin, BaseDeleteView):
    model = Poi


def get_polygon(request):
    g = geojson.Serializer()
    try:
        data = request.GET.getlist('polygon[]')
        pnt = ConvertGeometry(data, 'polygon').convert_geometry()
        if all([pnt, request.GET.get('category')]):
            poi_list = Poi.objects.select_related('category').filter(
                geom__within=pnt, category_id=request.GET.get('category')).values('id')

            poi = Poi.objects.filter(pk__in=poi_list, category_id=request.GET.get('category'))
            data = g.serialize(poi, geometry_field='geom',
            use_natural_foreign_keys=True, use_natural_primary_keys=True)
            return HttpResponse(data, content_type='application/json')
        else:
            raise Http404
    except IndexError:
        raise Http404


def get_route(request):
    g = geojson.Serializer()
    try:
        data = request.GET.getlist('route[]')
        pnt = ConvertGeometry(data, 'linestring').convert_geometry()
        if all([pnt, request.GET.get('category')]):
            poi_list = Poi.objects.select_related('category').filter(
                    geom__within=pnt.buffer(width=0.001),
                    category_id=request.GET.get('category')).values('id')
            poi = Poi.objects.filter(pk__in=poi_list, category_id=request.GET.get('category'))
            data = g.serialize(
                poi, geometry_field='geom',
                use_natural_foreign_keys=True, use_natural_primary_keys=True)
            return HttpResponse(data, content_type='application/json')
        else:
            raise Http404
    except IndexError:
        raise Http404


def get_radius(request):

    #  Get the point from the  array
    #  Convert the point in Point object
    #  Add a bounding box to the Point
    #  Check if tour points intersects with the bounding box
    #  the return the result query as geojson
    #  to display it in the map
    g = geojson.Serializer()
    lat = request.GET.get('lat', None)
    lng = request.GET.get('lng', None)
    radius = request.GET.get('radius', None)
    if(all([lat, lng, radius])):
        circle = geos.Point(float(lng), float(lat), srid=4326)
        poi = Poi.objects.select_related('category').filter(
            geom__distance_lt=(circle, Distance(km=int(radius)/1000)))
        data = g.serialize(
            poi, geometry_field='geom',
            use_natural_foreign_keys=True, use_natural_primary_keys=True)
        return HttpResponse(data, content_type='application/json')
    msg = {}
    msg['0'] = 'Error'
    return JsonResponse(msg, safe=False)


def save_category_form(request, form, template_name=None):
    data = dict()
    context = {'form': form}
    # if request.method == 'GET':
    #     if form.is_valid():
    #         obj = form.save()
    #     else:
    #         data['form_is_valid'] = False
    #         for key, error in form.errors.items():
    #             print(error)

    data['html_form'] = render_to_string(template_name, context, request)
    return JsonResponse(data)


def polygon_create(request):
    polygon = request.GET.getlist('x[]')
    data = {'polygon': polygon}
    form = PolygonSearchForm(initial=data)
    template = 'partials/category_search.html'
    return save_category_form(request, form, template)


def route_create(request):
    route = request.GET.getlist('x[]')
    data = {'route': route}
    form = RouteSearchForm(initial=data)
    template = 'partials/category_search.html'
    return save_category_form(request, form, template)


def get_location_geojson(request):
    id = request.GET.get("id")
    if not id:
        return JsonResponse({})
    g = geojson.Serializer()
    location = Location.objects.get(id=id)
    data = g.serialize([location], geometry_field='geom',
            use_natural_foreign_keys=True, use_natural_primary_keys=True)
    return JsonResponse(data, safe=False)


def get_poi_geojson(request):
    id = request.GET.get("id")
    if not id:
        return JsonResponse({})
    g = geojson.Serializer()
    poi = Poi.objects.get(id=id)
    data = g.serialize([poi], geometry_field='geom',
            use_natural_foreign_keys=True, use_natural_primary_keys=True)
    return JsonResponse(data, safe=False)