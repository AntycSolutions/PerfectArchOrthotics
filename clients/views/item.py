import collections

from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView

from django.core.urlresolvers import reverse_lazy

from search import get_query
from clients.models import Item
# from clients.forms.forms import ItemForm


class CreateItemView(CreateView):
    template_name = 'clients/generics/create.html'
    model = Item
    # form_class = ItemForm
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(CreateItemView, self).get_context_data(**kwargs)
        context['model_name_plural'] = self.model._meta.verbose_name_plural
        context['model_name'] = self.model._meta.verbose_name
        context['indefinite_article'] = 'an'
        return context

    def get_success_url(self):
        self.success_url = reverse_lazy('item_detail',
                                        kwargs={'pk': self.object.pk})
        return self.success_url


class ListItemView(ListView):
    template_name = "clients/generics/list.html"
    model = Item
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(ListItemView, self).get_context_data(**kwargs)
        context['model_name_plural'] = self.model._meta.verbose_name_plural
        context['model_name'] = self.model._meta.verbose_name
        context['indefinite_article'] = 'an'

        Option = collections.namedtuple('Option', ['value',
                                                   'value_display'])
        options = []
        for coverage_type in Item.COVERAGE_TYPES:
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
        queryset = super(ListItemView, self).get_queryset()

        if ('q' in self.request.GET) and self.request.GET['q'].strip():
            fields = ['gender', 'product_code', 'description']
            query_string = self.request.GET['q']
            item_query = get_query(query_string, fields)
            if queryset:
                queryset = queryset.filter(item_query)
            else:
                queryset = Item.objects.filter(item_query)

        if ('d' in self.request.GET) and self.request.GET['d'].strip():
            fields = ['coverage_type']
            query_string = self.request.GET['d']
            item_query = get_query(query_string, fields)
            if queryset:
                queryset = queryset.filter(item_query)
            else:
                queryset = Item.objects.filter(item_query)

        return queryset


class DetailItemView(DetailView):
    template_name = "clients/generics/detail.html"
    model = Item

    def get_context_data(self, **kwargs):
        context = super(DetailItemView, self).get_context_data(**kwargs)
        context['model_name'] = self.model._meta.verbose_name
        return context


class UpdateItemView(UpdateView):
    template_name = 'clients/generics/update.html'
    model = Item
    # form_class = ItemForm
    fields = '__all__'

    def get_success_url(self):
        self.success_url = reverse_lazy('item_detail',
                                        kwargs={'pk': self.object.pk})
        return self.success_url


class DeleteItemView(DeleteView):
    template_name = 'clients/generics/delete.html'
    model = Item

    def get_context_data(self, **kwargs):
        context = super(DeleteItemView, self).get_context_data(**kwargs)
        context['model_name'] = self.model._meta.verbose_name
        return context

    def get_success_url(self):
        self.success_url = reverse_lazy('item_list')
        return self.success_url
