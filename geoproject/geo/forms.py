from django import forms
from .models import Place, Area, Route


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
        model = Place
        fields = ('name',)


class AreaForm(DynamicForm, forms.ModelForm):

    class Meta:
        model = Area
        fields = ('name',)


class RouteForm(DynamicForm, forms.ModelForm):

    class Meta:
        model = Route
        fields = ('name',)
