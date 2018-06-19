from django.test import TestCase
from clients.models import Client, Referral


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
