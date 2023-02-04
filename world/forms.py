from django import forms
from core.convert_geometry import ConvertGeometry
from .models import Location, Category, Poi


class DynamicForm:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = ['CheckboxInput', 'ClearableFileInput', 'FileInput']
        for field in self.fields:
            widget_name = self.fields[field].widget.__class__.__name__
            if widget_name not in fields:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })


class PlaceForm(DynamicForm, forms.ModelForm):
    lat = forms.FloatField(widget=forms.HiddenInput())
    lng = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Poi
        fields = ('category', 'name')


class SearchForm(DynamicForm, forms.Form):
    term = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Example : Hotel'}), label='')
    model = forms.CharField(widget=forms.HiddenInput())
    pk = forms.CharField(widget=forms.HiddenInput())
    model_pk = forms.CharField(widget=forms.HiddenInput())


class PolygonSearchForm(DynamicForm, forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), required=False,
        empty_label="Select category")
    polygon = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        polygon = self.initial.get('polygon')
        pnt = ConvertGeometry(polygon, 'polygon').convert_geometry()
        poi_list = []
        if pnt:
            poi_list = Poi.objects.select_related('category').filter(geom__within=pnt)
            categories = Category.objects.filter(
                    pk__in=[poi.category_id for poi in poi_list])
            self.fields['category'].queryset = categories


class RouteSearchForm(DynamicForm, forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), required=False,
        empty_label="Select category")
    polygon = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        route = self.initial.get('route')
        pnt = ConvertGeometry(route, 'linestring').convert_geometry()
        poi_list = []
        if pnt:
            poi_list = Poi.objects.select_related('category').filter(
                geom__within=pnt.buffer(width=0.001))
            categories = Category.objects.filter(
                pk__in=[poi.category_id for poi in poi_list])
            self.fields['category'].queryset = categories



class PoiForm(DynamicForm, forms.ModelForm):
    lat = forms.FloatField(widget=forms.HiddenInput(), required=False)
    lng = forms.FloatField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Poi
        fields = ('name', 'category')