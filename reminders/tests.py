import datetime

from django import test
from django.utils import timezone
from django.core import management

from clients import models as clients_models
from . import models


class BenefitsReminderTestCase(test.TestCase):
    def setUp(self):
        self.client = clients_models.Client.objects.create(
            first_name='Client',
        )
        self.insurance = clients_models.Insurance.objects.create(
            main_claimant=self.client,
            provider='Insurance',
        )

    def _create_claim(self, coverage, submitted_datetime):
        claim = clients_models.Claim.objects.create(
            patient=self.client,
            submitted_datetime=submitted_datetime,
        )
        claim.insurances.add(self.insurance)
        clients_models.ClaimCoverage.objects.create(
            claim=claim, coverage=coverage
        )

        return claim

    def _create_coverage(self, period, period_date=None):
        coverage = clients_models.Coverage.objects.create(
            insurance=self.insurance,
            claimant=self.client,
            period=period,
            period_date=period_date
        )

        return coverage

    def test_calendar_none(self):
        coverage = self._create_coverage(clients_models.Coverage.CALENDAR_YEAR)
        self._create_claim(
            coverage,
            timezone.now()
        )

        reminders = models.BenefitsReminder.objects.count()
        self.assertEqual(reminders, 0)

        management.call_command('reminders')

        reminders = models.BenefitsReminder.objects.count()
        self.assertEqual(reminders, 0)

    def test_calendar(self):
        coverage = self._create_coverage(clients_models.Coverage.CALENDAR_YEAR)
        self._create_claim(
            coverage,
            timezone.now() - datetime.timedelta(days=365 + 5)
        )

        reminders = models.BenefitsReminder.objects.count()
        self.assertEqual(reminders, 0)

        management.call_command('reminders')

        reminders = models.BenefitsReminder.objects.count()
        self.assertEqual(reminders, 1)

    def test_calendar_complete(self):
        coverage = self._create_coverage(clients_models.Coverage.CALENDAR_YEAR)
        self._create_claim(
            coverage,
            timezone.now() - datetime.timedelta(days=365 + 5)
        )

        reminders = models.BenefitsReminder.objects.count()
        self.assertEqual(reminders, 0)

        management.call_command('reminders')

        reminders = models.BenefitsReminder.objects.count()
        self.assertEqual(reminders, 1)

        self._create_claim(
            coverage,
            timezone.now()
        )

        management.call_command('reminders')

        reminders = models.BenefitsReminder.objects.all()
        self.assertEqual(len(reminders), 1)
        self.assertIn(models.Reminder.COMPLETED, reminders[0].follow_up)

    def test_benefit_none(self):
        coverage = self._create_coverage(
            clients_models.Coverage.BENEFIT_YEAR, period_date=timezone.now()
        )
        self._create_claim(
            coverage,
            timezone.now() + datetime.timedelta(days=1)
        )

        reminders = models.BenefitsReminder.objects.count()
        self.assertEqual(reminders, 0)

        management.call_command('reminders')

        reminders = models.BenefitsReminder.objects.count()
        self.assertEqual(reminders, 0)

    def test_benefit(self):
        coverage = self._create_coverage(
            clients_models.Coverage.BENEFIT_YEAR, period_date=timezone.now()
        )
        self._create_claim(
            coverage,
            timezone.now() - datetime.timedelta(days=365 + 5)
        )

        reminders = models.BenefitsReminder.objects.count()
        self.assertEqual(reminders, 0)

        management.call_command('reminders')

        reminders = models.BenefitsReminder.objects.count()
        self.assertEqual(reminders, 1)

    def test_benefit_complete(self):
        coverage = self._create_coverage(
            clients_models.Coverage.BENEFIT_YEAR, period_date=timezone.now()
        )
        self._create_claim(
            coverage,
            timezone.now() - datetime.timedelta(days=365 + 5)
        )

        reminders = models.BenefitsReminder.objects.count()
        self.assertEqual(reminders, 0)

        management.call_command('reminders')

        reminders = models.BenefitsReminder.objects.count()
        self.assertEqual(reminders, 1)

        self._create_claim(
            coverage,
            timezone.now()
        )

        management.call_command('reminders')

        reminders = models.BenefitsReminder.objects.all()
        self.assertEqual(len(reminders), 1)
        self.assertIn(models.Reminder.COMPLETED, reminders[0].follow_up)

    def test_twelve_none(self):
        coverage = self._create_coverage(
            clients_models.Coverage.TWELVE_ROLLING_MONTHS
        )
        self._create_claim(
            coverage,
            timezone.now()
        )

        reminders = models.BenefitsReminder.objects.count()
        self.assertEqual(reminders, 0)

        management.call_command('reminders')

        reminders = models.BenefitsReminder.objects.count()
        self.assertEqual(reminders, 0)

    def test_twelve(self):
        coverage = self._create_coverage(
            clients_models.Coverage.TWELVE_ROLLING_MONTHS
        )
        self._create_claim(
            coverage,
            timezone.now() - datetime.timedelta(days=365 + 5)
        )

        reminders = models.BenefitsReminder.objects.count()
        self.assertEqual(reminders, 0)

        management.call_command('reminders')

        reminders = models.BenefitsReminder.objects.count()
        self.assertEqual(reminders, 1)

    def test_twelve_complete(self):
        coverage = self._create_coverage(
            clients_models.Coverage.TWELVE_ROLLING_MONTHS
        )
        self._create_claim(
            coverage,
            timezone.now() - datetime.timedelta(days=365 + 5)
        )

        reminders = models.BenefitsReminder.objects.count()
        self.assertEqual(reminders, 0)

        management.call_command('reminders')

        reminders = models.BenefitsReminder.objects.count()
        self.assertEqual(reminders, 1)

        self._create_claim(
            coverage,
            timezone.now()
        )

        management.call_command('reminders')

        reminders = models.BenefitsReminder.objects.all()
        self.assertEqual(len(reminders), 1)
        self.assertIn(models.Reminder.COMPLETED, reminders[0].follow_up)

    def test_twenty_four_none(self):
        coverage = self._create_coverage(
            clients_models.Coverage.TWENTY_FOUR_ROLLING_MONTHS
        )
        self._create_claim(
            coverage,
            timezone.now()
        )

        reminders = models.BenefitsReminder.objects.count()
        self.assertEqual(reminders, 0)

        management.call_command('reminders')

        reminders = models.BenefitsReminder.objects.count()
        self.assertEqual(reminders, 0)

    def test_twenty_four(self):
        coverage = self._create_coverage(
            clients_models.Coverage.TWENTY_FOUR_ROLLING_MONTHS
        )
        self._create_claim(
            coverage,
            timezone.now() - datetime.timedelta(days=730 + 5)
        )

        reminders = models.BenefitsReminder.objects.count()
        self.assertEqual(reminders, 0)

        management.call_command('reminders')

        reminders = models.BenefitsReminder.objects.count()
        self.assertEqual(reminders, 1)

    def test_twenty_four_complete(self):
        coverage = self._create_coverage(
            clients_models.Coverage.TWENTY_FOUR_ROLLING_MONTHS
        )
        self._create_claim(
            coverage,
            timezone.now() - datetime.timedelta(days=730 + 5)
        )

        reminders = models.BenefitsReminder.objects.count()
        self.assertEqual(reminders, 0)

        management.call_command('reminders')

        reminders = models.BenefitsReminder.objects.count()
        self.assertEqual(reminders, 1)

        self._create_claim(
            coverage,
            timezone.now() - datetime.timedelta(days=365 + 5)
        )

        management.call_command('reminders')

        reminders = models.BenefitsReminder.objects.all()
        self.assertEqual(len(reminders), 1)
        self.assertIn(models.Reminder.COMPLETED, reminders[0].follow_up)

    def test_thirty_six_none(self):
        coverage = self._create_coverage(
            clients_models.Coverage.THIRTY_SIX_ROLLING_MONTHS
        )
        self._create_claim(
            coverage,
            timezone.now()
        )

        reminders = models.BenefitsReminder.objects.count()
        self.assertEqual(reminders, 0)

        management.call_command('reminders')

        reminders = models.BenefitsReminder.objects.count()
        self.assertEqual(reminders, 0)

    def test_thirty_six(self):
        coverage = self._create_coverage(
            clients_models.Coverage.THIRTY_SIX_ROLLING_MONTHS
        )
        self._create_claim(
            coverage,
            timezone.now() - datetime.timedelta(days=1095 + 5)
        )

        reminders = models.BenefitsReminder.objects.count()
        self.assertEqual(reminders, 0)

        management.call_command('reminders')

        reminders = models.BenefitsReminder.objects.count()
        self.assertEqual(reminders, 1)

    def test_thirty_six_complete(self):
        coverage = self._create_coverage(
            clients_models.Coverage.THIRTY_SIX_ROLLING_MONTHS
        )
        self._create_claim(
            coverage,
            timezone.now() - datetime.timedelta(days=1095 + 5)
        )

        reminders = models.BenefitsReminder.objects.count()
        self.assertEqual(reminders, 0)

        management.call_command('reminders')

        reminders = models.BenefitsReminder.objects.count()
        self.assertEqual(reminders, 1)

        self._create_claim(
            coverage,
            timezone.now() - datetime.timedelta(days=730 + 5)
        )

        management.call_command('reminders')

        reminders = models.BenefitsReminder.objects.all()
        self.assertEqual(len(reminders), 1)
        self.assertIn(models.Reminder.COMPLETED, reminders[0].follow_up)

    def test_update(self):
        coverage = self._create_coverage(
            clients_models.Coverage.TWELVE_ROLLING_MONTHS
        )
        self._create_claim(
            coverage,
            timezone.now() - datetime.timedelta(days=365 + 5)
        )

        reminders = models.BenefitsReminder.objects.count()
        self.assertEqual(reminders, 0)

        management.call_command('reminders')

        reminders = models.BenefitsReminder.objects.count()
        self.assertEqual(reminders, 1)

        self._create_claim(
            coverage,
            timezone.now() - datetime.timedelta(days=365 + 5)
        )

        management.call_command('reminders')

        reminders = models.BenefitsReminder.objects.all()
        self.assertEqual(len(reminders), 1)
        self.assertIn(models.Reminder.REQUIRED, reminders[0].follow_up)

        coverage2 = self._create_coverage(
            clients_models.Coverage.TWELVE_ROLLING_MONTHS
        )
        self._create_claim(
            coverage2,
            timezone.now() - datetime.timedelta(days=365 + 5)
        )

        management.call_command('reminders')

        reminders = models.BenefitsReminder.objects.all()
        self.assertEqual(len(reminders), 1)
        self.assertIn(models.Reminder.REQUIRED, reminders[0].follow_up)
        self.assertEqual(len(reminders[0].coverages.all()), 2)

        self._create_claim(
            coverage,
            timezone.now()
        )
        self._create_claim(
            coverage2,
            timezone.now()
        )

        management.call_command('reminders')

        reminders = models.BenefitsReminder.objects.all()
        self.assertEqual(len(reminders), 1)
        self.assertIn(models.Reminder.COMPLETED, reminders[0].follow_up)
        self.assertEqual(len(reminders[0].coverages.all()), 0)

    def test_reset_required(self):
        coverage = self._create_coverage(
            clients_models.Coverage.TWELVE_ROLLING_MONTHS
        )
        self._create_claim(
            coverage,
            timezone.now() - datetime.timedelta(days=365 + 5)
        )

        reminders = models.BenefitsReminder.objects.count()
        self.assertEqual(reminders, 0)

        management.call_command('reminders')

        reminders = models.BenefitsReminder.objects.count()
        self.assertEqual(reminders, 1)

        self._create_claim(
            coverage,
            timezone.now() - datetime.timedelta(days=365 + 5)
        )

        management.call_command('reminders')

        reminders = models.BenefitsReminder.objects.all()
        self.assertEqual(len(reminders), 1)
        self.assertIn(models.Reminder.REQUIRED, reminders[0].follow_up)

        reminder = models.BenefitsReminder.objects.first()
        reminder.follow_up = models.Reminder.EMAIL
        reminder.created = (
            timezone.now() - datetime.timedelta(weeks=6 + 1)
        ).date()
        reminder.save()

        management.call_command('reminders')

        reminders = models.BenefitsReminder.objects.all()
        self.assertEqual(len(reminders), 1)
        self.assertIn(models.Reminder.REQUIRED, reminders[0].follow_up)
        self.assertEqual(len(reminders[0].coverages.all()), 1)

    def test_reset_complete(self):
        coverage = self._create_coverage(
            clients_models.Coverage.TWELVE_ROLLING_MONTHS
        )
        self._create_claim(
            coverage,
            timezone.now() - datetime.timedelta(days=365 + 5)
        )

        reminders = models.BenefitsReminder.objects.count()
        self.assertEqual(reminders, 0)

        management.call_command('reminders')

        reminders = models.BenefitsReminder.objects.count()
        self.assertEqual(reminders, 1)

        self._create_claim(
            coverage,
            timezone.now() - datetime.timedelta(days=365 + 5)
        )

        management.call_command('reminders')

        reminders = models.BenefitsReminder.objects.all()
        self.assertEqual(len(reminders), 1)
        self.assertIn(models.Reminder.REQUIRED, reminders[0].follow_up)

        claim = self._create_claim(
            coverage,
            timezone.now()
        )

        management.call_command('reminders')

        reminders = models.BenefitsReminder.objects.all()
        self.assertEqual(len(reminders), 1)
        self.assertIn(models.Reminder.COMPLETED, reminders[0].follow_up)
        self.assertEqual(len(reminders[0].coverages.all()), 0)

        claim.delete()
        reminders[0].created = timezone.now() - datetime.timedelta(weeks=6 + 1)
        reminders[0].save()

        management.call_command('reminders')

        reminders = models.BenefitsReminder.objects.all()
        self.assertEqual(len(reminders), 1)
        self.assertIn(models.Reminder.REQUIRED, reminders[0].follow_up)
        self.assertEqual(len(reminders[0].coverages.all()), 1)
