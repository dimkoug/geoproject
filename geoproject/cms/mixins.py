from django.urls import reverse


class SuccessUrlMixin:
    def get_success_url(self):
        model = self.model.__name__.lower()
        return reverse('{}-list'.format(model))
