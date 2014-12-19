from django.views.generic import TemplateView

from ..models import SiteStatistics


class Statistics(TemplateView):
    template_name = "clients/statistics.html"
    context = dict()

    def get(self, request, *args, **kwargs):
        statistics = SiteStatistics.objects.get_or_create(pk=0)[0]

        self.context['statistics'] = statistics

        return self.render_to_response(self.context)
