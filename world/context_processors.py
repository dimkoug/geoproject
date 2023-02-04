from django.conf import settings
from django.core.cache import cache
from django.db.models import Prefetch
from django.db.models import Count
from .models import Location, Category, Poi


def get_data(request):

    locations = Location.objects.select_related('parent').filter(parent__isnull=True).values("id", 'name')
    categories = Category.objects.all()
    return {
        'debug': settings.DEBUG,
        'GOOGLE_MAPS_KEY': settings.GOOGLE_MAPS_KEY,
        'locations': locations,
        'categories': categories
      }