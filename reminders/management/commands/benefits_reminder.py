import datetime

from django.utils import timezone
from django.core.management import base

from clients import models as clients_models
from ... import models as reminders_models


class Command(base.BaseCommand):
    help = 'Check for clients we want to remind to come back'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        now = timezone.now()
        jan_1 = datetime.datetime(
            year=now.year, month=1, day=1, tzinfo=now.tzinfo
        )
        client_ids = {}

        all_benefit_coverages = (
            clients_models.Coverage.objects.select_related(
                'claimant__client'
            ).prefetch_related(
                'claimcoverage_set__claim'
            ).filter(
                period=clients_models.Coverage.BENEFIT_YEAR,
                period_date__isnull=False
            )
        )
        # TODO in django 2.2+ we can use ExtractFunction to get month/day
        benefit_coverages = []
        for coverage in all_benefit_coverages:
            add = True
            for claimcoverage in coverage.claimcoverage_set.all():
                submitted_datetime = claimcoverage.claim.submitted_datetime
                year = submitted_datetime.year
                month = submitted_datetime.month
                day = submitted_datetime.day
                period_date = coverage.period_date
                if (
                    year >= now.year and
                    month >= period_date.month and
                    day > period_date.day
                ):
                    add = False
                    break
            if add:
                benefit_coverages.append(coverage)

        calendar_coverages = clients_models.Coverage.objects.select_related(
            'claimant__client'
        ).filter(
            period=clients_models.Coverage.CALENDAR_YEAR
        ).exclude(
            claimcoverage__claim__submitted_datetime__gt=jan_1
        )

        twelve_months_ago = now - datetime.timedelta(days=365)
        twelve_coverages = clients_models.Coverage.objects.select_related(
            'claimant__client'
        ).filter(
            period=clients_models.Coverage.TWELVE_ROLLING_MONTHS
        ).exclude(
            claimcoverage__claim__submitted_datetime__gt=twelve_months_ago
        )

        twenty_four_months_ago = now - datetime.timedelta(days=730)
        twenty_four_coverages = clients_models.Coverage.objects.select_related(
            'claimant__client'
        ).filter(
            period=clients_models.Coverage.TWENTY_FOUR_ROLLING_MONTHS
        ).exclude(
            claimcoverage__claim__submitted_datetime__gt=twenty_four_months_ago
        )

        thirty_six_months_ago = now - datetime.timedelta(days=1095)
        thirty_six_coverages = clients_models.Coverage.objects.select_related(
            'claimant__client'
        ).filter(
            period=clients_models.Coverage.THIRTY_SIX_ROLLING_MONTHS
        ).exclude(
            claimcoverage__claim__submitted_datetime__gt=thirty_six_months_ago
        )

        coverages = benefit_coverages + list(
            calendar_coverages |
            twelve_coverages |
            twenty_four_coverages |
            thirty_six_coverages
        )
        for coverage in coverages:
            client_id = coverage.claimant.get_client().pk
            client_coverage_ids = client_ids.get(client_id, set())
            client_coverage_ids.add(coverage.pk)
            client_ids[client_id] = client_coverage_ids

        reminders = reminders_models.BenefitsReminder.objects.select_related(
            'client'
        ).exclude(
            follow_up__contains=reminders_models.Reminder.DELETED
        )
        three_weeks = datetime.timedelta(weeks=3)
        three_weeks_ago = now.date() - three_weeks
        for reminder in reminders:
            coverage_ids = client_ids.pop(reminder.client.pk, None)
            if coverage_ids is None:
                reminder.follow_up = reminders_models.Reminder.COMPLETED
                reminder.result = ''
                reminder.created = now
                reminder.save()
                reminder.coverages.clear()
                continue

            if reminders_models.Reminder.REQUIRED not in reminder.follow_up:
                if reminder.created <= three_weeks_ago:
                    reminder.follow_up = reminders_models.Reminder.REQUIRED
                    reminder.result = ''
                    reminder.created = now
                    reminder.save()
            reminder.coverages.set(coverage_ids)
        for client_id, coverage_ids in client_ids.items():
            reminder = reminders_models.BenefitsReminder.objects.create(
                client_id=client_id,
                created=now.date()
            )
            reminder.coverages.set(coverage_ids)
