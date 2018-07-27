from django.test import TestCase
from django.utils import timezone
from clients.models import Client, Referral, Claim, Insurance, Coverage
from clients.forms.forms import ReferralForm


class ReferralCreditsTestCase(TestCase):

    def setUp(self):
        self.client = Client.objects.create(first_name='Test Client')

    def test_referral_create(self):
        self.assertEqual(self.client.credit2, 0)

        Referral.objects.create(
            client=self.client,
            credit_value=1,
        )
        client = Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, 1)

    def test_referral_change_credit_value(self):
        self.assertEqual(self.client.credit2, 0)

        referral = Referral.objects.create(
            client=self.client,
            credit_value=1,
        )
        client = Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, 1)

        referral.credit_value = 2
        referral.save()
        client = Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, 2)

    def test_referral_delete(self):
        self.assertEqual(self.client.credit2, 0)

        referral = Referral.objects.create(
            client=self.client,
            credit_value=1,
        )
        client = Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, 1)

        referral.delete()
        client = Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, 0)

    def _setup_test_data(self):
        referred_client = Client.objects.create(
            first_name="Referred Man",
            referred_by=self.client
            )
        insurance = Insurance.objects.create(
            main_claimant=self.client,
            provider='Test Insurance',
        )
        Coverage.objects.create(
            insurance=insurance,
            claimant=self.client,
            period=Coverage.CALENDAR_YEAR,
        )
        Claim.objects.create(
            patient=referred_client,
            insurance=insurance,
            submitted_datetime=timezone.now())
        Referral.objects.create(
            client=self.client,
            credit_value=1)

    def test_cannot_receive_credit_for_duplicate_referral(self):
        self._setup_test_data()

        claims_queryset = Claim.objects.none()
        claims_queryset = ReferralForm._get_referred_claims(
            ReferralForm,
            self.client.person_ptr,
            claims_queryset)

        self.assertFalse(
            ReferralForm._remove_credited_claims(
                ReferralForm,
                claims_queryset,
                self.client).exists())
