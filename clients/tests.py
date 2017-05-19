from django import test
from django.utils import timezone

from clients import models as clients_models
from inventory import models as inventory_models


class CreditTestCase(test.TestCase):

    def setUp(self):
        self.now = timezone.now()

        client = clients_models.Client.objects.create(
            first_name='Test Client',
        )
        insurance = clients_models.Insurance.objects.create(
            main_claimant=client,
            provider='Test Insurance',
        )
        clients_models.Coverage.objects.create(
            insurance=insurance,
            claimant=client,
            period=clients_models.Coverage.CALENDAR_YEAR,
        )
        clients_models.Claim.objects.create(
            patient=client,
            insurance=insurance,
            submitted_datetime=self.now,
        )

        clients_models.CreditDivisor.objects.create(
            value=150,
            # Must be before actual_paid_date
            created=self.now - timezone.timedelta(1),
        )

    def test_claimcoverage_none(self):
        client = clients_models.Client.objects.get(first_name='Test Client')
        self.assertEqual(client.credit2, 0)

    def test_claimcoverage_create(self):
        client = clients_models.Client.objects.get(first_name='Test Client')
        self.assertEqual(client.credit2, 0)

        clients_models.ClaimCoverage.objects.create(
            claim=clients_models.Claim.objects.get(patient=client),
            coverage=clients_models.Coverage.objects.get(claimant=client),
            actual_paid_date=self.now,
            expected_back=150,
        )
        client = clients_models.Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, 1)

    def test_claimcoverage_unset_actual_paid_date(self):
        client = clients_models.Client.objects.get(first_name='Test Client')
        self.assertEqual(client.credit2, 0)

        claimcoverage = clients_models.ClaimCoverage.objects.create(
            claim=clients_models.Claim.objects.get(patient=client),
            coverage=clients_models.Coverage.objects.get(claimant=client),
            actual_paid_date=self.now,
            expected_back=150,
        )
        client = clients_models.Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, 1)

        # TODO: why is actual_paid_date stored as just date in db
        claimcoverage.actual_paid_date = None
        claimcoverage.save()
        client = clients_models.Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, 0)

    def test_claimcoverage_set_actual_paid_date(self):
        client = clients_models.Client.objects.get(first_name='Test Client')
        self.assertEqual(client.credit2, 0)

        claimcoverage = clients_models.ClaimCoverage.objects.create(
            claim=clients_models.Claim.objects.get(patient=client),
            coverage=clients_models.Coverage.objects.get(claimant=client),
            expected_back=150,
        )
        client = clients_models.Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, 0)

        claimcoverage.actual_paid_date = self.now
        claimcoverage.save()
        client = clients_models.Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, 1)

    def test_claimcoverage_change_expected_back(self):
        client = clients_models.Client.objects.get(first_name='Test Client')
        self.assertEqual(client.credit2, 0)

        claimcoverage = clients_models.ClaimCoverage.objects.create(
            claim=clients_models.Claim.objects.get(patient=client),
            coverage=clients_models.Coverage.objects.get(claimant=client),
            actual_paid_date=self.now,
            expected_back=150,
        )
        client = clients_models.Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, 1)

        claimcoverage.expected_back = 300
        claimcoverage.save()
        client = clients_models.Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, 2)

    def test_claimcoverage_delete(self):
        client = clients_models.Client.objects.get(first_name='Test Client')
        self.assertEqual(client.credit2, 0)

        claimcoverage = clients_models.ClaimCoverage.objects.create(
            claim=clients_models.Claim.objects.get(patient=client),
            coverage=clients_models.Coverage.objects.get(claimant=client),
            actual_paid_date=self.now,
            expected_back=150,
        )
        client = clients_models.Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, 1)

        claimcoverage.delete()
        client = clients_models.Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, 0)

    def test_shoeorder_create(self):
        client = clients_models.Client.objects.get(first_name='Test Client')
        self.assertEqual(client.credit2, 0)

        shoe = inventory_models.Shoe.objects.create(
            name='Test Shoe',
            credit_value=1,
        )
        shoeattributes = inventory_models.ShoeAttributes.objects.create(
            shoe=shoe,
        )
        inventory_models.ShoeOrder.objects.create(
            claimant=client,
            shoe_attributes=shoeattributes,
        )
        client = clients_models.Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, -1)

    def test_shoe_change_credit_value(self):
        client = clients_models.Client.objects.get(first_name='Test Client')
        self.assertEqual(client.credit2, 0)

        shoe = inventory_models.Shoe.objects.create(
            name='Test Shoe',
            credit_value=1,
        )
        shoeattributes = inventory_models.ShoeAttributes.objects.create(
            shoe=shoe,
        )
        inventory_models.ShoeOrder.objects.create(
            claimant=client,
            shoe_attributes=shoeattributes,
        )
        client = clients_models.Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, -1)

        shoe.credit_value = 2
        shoe.save()
        client = clients_models.Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, -2)

    def test_shoeorder_shoe_delete(self):
        client = clients_models.Client.objects.get(first_name='Test Client')
        self.assertEqual(client.credit2, 0)

        shoe = inventory_models.Shoe.objects.create(
            name='Test Shoe',
            credit_value=1,
        )
        shoeattributes = inventory_models.ShoeAttributes.objects.create(
            shoe=shoe,
        )
        inventory_models.ShoeOrder.objects.create(
            claimant=client,
            shoe_attributes=shoeattributes,
        )
        client = clients_models.Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, -1)

        shoe.delete()
        client = clients_models.Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, 0)

    def test_shoeorder_delete(self):
        client = clients_models.Client.objects.get(first_name='Test Client')
        self.assertEqual(client.credit2, 0)

        shoe = inventory_models.Shoe.objects.create(
            name='Test Shoe',
            credit_value=1,
        )
        shoeattributes = inventory_models.ShoeAttributes.objects.create(
            shoe=shoe,
        )
        shoeorder = inventory_models.ShoeOrder.objects.create(
            claimant=client,
            shoe_attributes=shoeattributes,
        )
        client = clients_models.Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, -1)

        shoeorder.delete()
        client = clients_models.Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, 0)

    def test_coverageorder_create(self):
        client = clients_models.Client.objects.get(first_name='Test Client')
        self.assertEqual(client.credit2, 0)

        inventory_models.CoverageOrder.objects.create(
            claimant=client,
            credit_value=1,
        )
        client = clients_models.Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, -1)

    def test_coverageorder_change_credit_value(self):
        client = clients_models.Client.objects.get(first_name='Test Client')
        self.assertEqual(client.credit2, 0)

        coverageorder = inventory_models.CoverageOrder.objects.create(
            claimant=client,
            credit_value=1,
        )
        client = clients_models.Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, -1)

        coverageorder.credit_value = 2
        coverageorder.save()
        client = clients_models.Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, -2)

    def test_coverageorder_delete(self):
        client = clients_models.Client.objects.get(first_name='Test Client')
        self.assertEqual(client.credit2, 0)

        coverageorder = inventory_models.CoverageOrder.objects.create(
            order_type=clients_models.Coverage.ORTHOTICS,
            claimant=client,
            credit_value=1,
        )
        client = clients_models.Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, -1)

        coverageorder.delete()
        client = clients_models.Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, 0)

    def test_referral_create(self):
        client = clients_models.Client.objects.get(first_name='Test Client')
        self.assertEqual(client.credit2, 0)

        clients_models.Referral.objects.create(
            client=client,
            credit_value=1,
        )
        client = clients_models.Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, 1)

    def test_referral_change_credit_value(self):
        client = clients_models.Client.objects.get(first_name='Test Client')
        self.assertEqual(client.credit2, 0)

        referral = clients_models.Referral.objects.create(
            client=client,
            credit_value=1,
        )
        client = clients_models.Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, 1)

        referral.credit_value = 2
        referral.save()
        client = clients_models.Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, 2)

    def test_referral_delete(self):
        client = clients_models.Client.objects.get(first_name='Test Client')
        self.assertEqual(client.credit2, 0)

        referral = clients_models.Referral.objects.create(
            client=client,
            credit_value=1,
        )
        client = clients_models.Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, 1)

        referral.delete()
        client = clients_models.Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, 0)

    def test_shoeorder_create_returned_date(self):
        client = clients_models.Client.objects.get(first_name='Test Client')
        self.assertEqual(client.credit2, 0)

        shoe = inventory_models.Shoe.objects.create(
            name='Test Shoe',
            credit_value=1,
        )
        shoeattributes = inventory_models.ShoeAttributes.objects.create(
            shoe=shoe,
        )
        inventory_models.ShoeOrder.objects.create(
            claimant=client,
            shoe_attributes=shoeattributes,
            returned_date=self.now,
        )
        client = clients_models.Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, 0)

    def test_shoe_change_credit_value_returned_date(self):
        client = clients_models.Client.objects.get(first_name='Test Client')
        self.assertEqual(client.credit2, 0)

        shoe = inventory_models.Shoe.objects.create(
            name='Test Shoe',
            credit_value=1,
        )
        shoeattributes = inventory_models.ShoeAttributes.objects.create(
            shoe=shoe,
        )
        inventory_models.ShoeOrder.objects.create(
            claimant=client,
            shoe_attributes=shoeattributes,
            returned_date=self.now,
        )
        client = clients_models.Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, 0)

        shoe.credit_value = 2
        shoe.save()
        client = clients_models.Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, 0)

    def test_shoeorder_shoe_delete_returned_date(self):
        client = clients_models.Client.objects.get(first_name='Test Client')
        self.assertEqual(client.credit2, 0)

        shoe = inventory_models.Shoe.objects.create(
            name='Test Shoe',
            credit_value=1,
        )
        shoeattributes = inventory_models.ShoeAttributes.objects.create(
            shoe=shoe,
        )
        inventory_models.ShoeOrder.objects.create(
            claimant=client,
            shoe_attributes=shoeattributes,
            returned_date=self.now,
        )
        client = clients_models.Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, 0)

        shoe.delete()
        client = clients_models.Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, 0)

    def test_shoeorder_update_returned_date(self):
        client = clients_models.Client.objects.get(first_name='Test Client')
        self.assertEqual(client.credit2, 0)

        shoe = inventory_models.Shoe.objects.create(
            name='Test Shoe',
            credit_value=1,
        )
        shoeattributes = inventory_models.ShoeAttributes.objects.create(
            shoe=shoe,
        )
        shoeorder = inventory_models.ShoeOrder.objects.create(
            claimant=client,
            shoe_attributes=shoeattributes,
        )
        client = clients_models.Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, -1)

        shoeorder.returned_date = self.now
        shoeorder.save()

        client = clients_models.Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, 0)

        shoeorder.returned_date = None
        shoeorder.save()

        client = clients_models.Client.objects.get(first_name='Test Client')

        self.assertEqual(client.credit2, -1)
