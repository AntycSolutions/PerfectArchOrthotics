import collections

from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView

from django.core.urlresolvers import reverse_lazy

from search import get_query
from inventory.models import Shoe


class CreateShoeView(CreateView):
    template_name = 'clients/generics/create.html'
    model = Shoe
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(CreateShoeView, self).get_context_data(**kwargs)
        context['model_name_plural'] = self.model._meta.verbose_name_plural
        context['model_name'] = self.model._meta.verbose_name
        context['indefinite_article'] = 'a'
        return context

    def get_success_url(self):
        self.success_url = reverse_lazy('shoe_detail',
                                        kwargs={'pk': self.object.pk})
        return self.success_url


class ListShoeView(ListView):
    template_name = "clients/generics/list.html"
    model = Shoe
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(ListShoeView, self).get_context_data(**kwargs)
        context['model_name_plural'] = self.model._meta.verbose_name_plural
        context['model_name'] = self.model._meta.verbose_name
        context['indefinite_article'] = 'a'

        Option = collections.namedtuple('Option', ['value',
                                                   'value_display'])
        options = []
        for coverage_type in Shoe.COVERAGE_TYPES:
            options.append(Option(coverage_type[0], coverage_type[1]))
        context['options'] = options

        if ('q' in self.request.GET) and self.request.GET['q'].strip():
            query_string = self.request.GET['q']
            context['q'] = query_string

        if ('d' in self.request.GET) and self.request.GET['d'].strip():
            query_string = self.request.GET['d']
            context['d'] = query_string
        return context

    def get_queryset(self):
        # Start from all, drilldown to q
        queryset = super(ListShoeView, self).get_queryset()

        if ('q' in self.request.GET) and self.request.GET['q'].strip():
            fields = ['brand', 'style', 'name', 'sku', 'colour', 'description']
            query_string = self.request.GET['q']
            shoe_query = get_query(query_string, fields)
            if queryset:
                queryset = queryset.filter(shoe_query)
            else:
                queryset = Shoe.objects.filter(shoe_query)

        if ('d' in self.request.GET) and self.request.GET['d'].strip():
            fields = ['coverage_type']
            query_string = self.request.GET['d']
            shoe_query = get_query(query_string, fields)
            if queryset:
                queryset = queryset.filter(shoe_query)
            else:
                queryset = Shoe.objects.filter(shoe_query)

        return queryset


class DetailShoeView(DetailView):
    template_name = "clients/generics/detail.html"
    model = Shoe

    def get_context_data(self, **kwargs):
        context = super(DetailShoeView, self).get_context_data(**kwargs)
        context['model_name'] = self.model._meta.verbose_name
        return context


class UpdateShoeView(UpdateView):
    template_name = 'clients/generics/update.html'
    model = Shoe
    fields = '__all__'

    def get_success_url(self):
        self.success_url = reverse_lazy('shoe_detail',
                                        kwargs={'pk': self.object.pk})
        return self.success_url


class DeleteShoeView(DeleteView):
    template_name = 'clients/generics/delete.html'
    model = Shoe

    def get_context_data(self, **kwargs):
        context = super(DeleteShoeView, self).get_context_data(**kwargs)
        context['model_name'] = self.model._meta.verbose_name
        return context

    def get_success_url(self):
        self.success_url = reverse_lazy('shoe_list')
        return self.success_url
