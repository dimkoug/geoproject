from django.urls import path

from .views import(
    LocationDetailView,
    CategoryDetailView,
    PolygonView,
    RouteView,
    PoiListView,
    PoiCreateView,
    PoiUpdateView,
    PoiDeleteView,
    get_polygon,
    get_route,
    get_radius,
    get_location_geojson,
    get_poi_geojson,
    polygon_create,
    route_create,
)

app_name="world"

urlpatterns = [
    path('<int:pk>/', LocationDetailView.as_view(),name="location-detail"),
    path('category/<int:pk>/', CategoryDetailView.as_view(),name="category-detail"),
    path('poi/', PoiListView.as_view(),name="poi-list"),
    path('poi/create/', PoiCreateView.as_view(),name="poi-create"),
    path('poi/update/<int:pk>/', PoiUpdateView.as_view(),name="poi-update"),
    path('poi/delete/<int:pk>/', PoiDeleteView.as_view(),name="poi-delete"),
    path('polygon/', PolygonView.as_view(), name='polygon'),
    path('route/', RouteView.as_view(), name='route'),
    path('get_polygon/', get_polygon,name="get-polygon"),
    path('get_route/', get_route,name="get-route"),
    path('get_radius/', get_radius,name="get-radius"),
    path('get_location_geojson/', get_location_geojson,name="get-location-geojson"),
    path('get_poi_geojson/', get_poi_geojson,name="get-poi-geojson"),
    path('polygon_create/', polygon_create, name='polygon_create'),
    path('route_create/', route_create, name='route_create'),

] 