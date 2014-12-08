from django.views.generic import TemplateView

from ..models import Client, Claim, SiteStatistics


class Statistics(TemplateView):
    template_name = "statistics.html"
    context = dict()

    def get(self, request, *args, **kwargs):
        #number of mechanics, number of inspection videos and views,
        #number of sellers, etc.
        clients_total = Client.objects.all().count()
        claims_total = Claim.objects.all().count()
        statistics = SiteStatistics.objects.get_or_create(pk=0)[0]

        self.context['clients_total'] = clients_total
        self.context['claims_total'] = claims_total
        self.context['statistics'] = statistics

        return self.render_to_response(self.context)
