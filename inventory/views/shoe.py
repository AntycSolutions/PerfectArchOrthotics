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
        context['form_type'] = 'multipart/form-data'
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

        if ('q' in self.request.GET) and self.request.GET['q'].strip():
            query_string = self.request.GET['q']
            context['q'] = query_string

        Option = collections.namedtuple('Option', ['value',
                                                   'value_display',
                                                   'selected'])
        categories = []
        for category in Shoe.CATEGORIES:
            if ("category" in self.request.GET
                    and self.request.GET["category"].strip()
                    and self.request.GET["category"] == category[0]):
                categories.append(Option(category[0], category[1], True))
            else:
                categories.append(Option(category[0], category[1], False))
        sizes = []
        for size in Shoe.SIZES:
            if ("size" in self.request.GET
                    and self.request.GET["size"].strip()
                    and self.request.GET["size"] == size[0]):
                sizes.append(Option(size[0], size[1], True))
            else:
                sizes.append(Option(size[0], size[1], False))
        selects = {"category": categories, "size": sizes}
        context['selects'] = selects

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

        if ('category' in self.request.GET
                and self.request.GET['category'].strip()):
            fields = ['category']
            query_string = self.request.GET['category']
            shoe_query = get_query(query_string, fields)
            if queryset:
                queryset = queryset.filter(shoe_query)
            else:
                queryset = Shoe.objects.filter(shoe_query)

        if ('size' in self.request.GET
                and self.request.GET['size'].strip()):
            fields = ['size']
            query_string = self.request.GET['size']
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

    def get_context_data(self, **kwargs):
        context = super(UpdateShoeView, self).get_context_data(**kwargs)
        context['model_name_plural'] = self.model._meta.verbose_name_plural
        context['model_name'] = self.model._meta.verbose_name
        context['indefinite_article'] = 'a'
        context['form_type'] = 'multipart/form-data'
        return context

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
