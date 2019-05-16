from django.core.management import base

from ... import utils


class Command(base.BaseCommand):
    help = 'Find all Reminders'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        utils._find_unpaid_claims()
        utils._find_arrived_orders()
        utils._find_claims_without_orders()
        utils.find_benefits_clients()
