from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .mixins import SuccessUrlMixin


class BaseListView(ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'model': self.model
        })
        return context


class BaseCreateView(SuccessUrlMixin, CreateView):
    pass


class BaseUpdateView(SuccessUrlMixin, UpdateView):
    pass


class BaseDeleteView(SuccessUrlMixin, DeleteView):
    pass
