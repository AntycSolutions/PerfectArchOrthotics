import decimal

from django.db import models
from django.core import urlresolvers
from datetime import date


class Person(models.Model):
    MALE = 'm'
    FEMALE = 'f'
    GENDERS = ((MALE, 'Male'),
               (FEMALE, 'Female'))

    first_name = models.CharField(
        "First Name", max_length=128)
    last_name = models.CharField(
        "Last Name", max_length=128,
        blank=True)
    gender = models.CharField(
        "Gender", max_length=4, choices=GENDERS,
        blank=True)
    birth_date = models.DateField(
        "Birth Date",
        blank=True, null=True)
    health_care_number = models.CharField(
        "Health Care Number", max_length=20,
        blank=True)
    employer = models.CharField(
        "Employer", max_length=128,
        blank=True)

    created = models.DateTimeField(
        "Created", auto_now_add=True)

    class Meta:
        permissions = (
            ('view_statistics', 'Can see statistics'),
        )

    # ModelInheritance
    # Client, Dependent
    # ManyToManyField
    # Insurance
    # ForeignKey
    # Client, Insurance, Coverage, Claim

    def age(self):
        if self.birth_date:
            today = date.today()

            return (
                today.year
                - self.birth_date.year
                - ((today.month, today.day)
                    < (self.birth_date.month, self.birth_date.day))
            )

    def full_name(self):
        full_name = self.first_name
        if self.last_name:
            full_name += " {0}".format(self.last_name)

        return full_name

    def get_absolute_url(self):
        try:
            return self.client.get_absolute_url()
        except Client.DoesNotExist:
            pass
        try:
            return self.dependent.get_absolute_url()
        except Dependent.DoesNotExist:
            pass

        raise Exception('Person is not a Client nor a Dependent.')

    def get_client(self):
        try:
            return self.client
        except Client.DoesNotExist:
            pass
        try:
            return self.dependent.primary
        except Dependent.DoesNotExist:
            pass

        raise Exception('Person is not tied to a Client: {}'.format(self.id))

    def __str__(self):
        return self.full_name()


class Client(Person):
    address = models.CharField(
        "Address", max_length=128,
        blank=True)
    city = models.CharField(
        "City", max_length=128,
        blank=True)
    province = models.CharField(
        "Province", max_length=128,
        blank=True)
    postal_code = models.CharField(
        "Postal Code", max_length=7,
        blank=True)
    # TODO Write validators for the phone numbers below
    # In the form of (780)-937-1514
    phone_number = models.CharField(
        "Phone Number", max_length=14,
        blank=True)
    # In the form of (780)-937-1514
    cell_number = models.CharField(
        "Cell Number", max_length=14,
        blank=True)
    email = models.EmailField(
        "Email", max_length=254,
        blank=True, null=True)
    referred_by = models.ForeignKey(
        Person, related_name="referred_set",
        blank=True, null=True
    )
    notes = models.TextField(
        "Notes",
        blank=True)

    # TODO: remove credit() and rename credit2 to credit
    credit2 = models.DecimalField(
        max_digits=5, decimal_places=2,
        default=decimal.Decimal(0)
    )

    # ForeignKey
    # Client, Dependent

    def _claimed_credit(self, person):
        claimed_credit = 0
        for order in person.order_set.all():
            claimed_credit += order.get_credit_value()

        return claimed_credit

    # TODO: remove credit() and rename credit2 to credit
    def credit(self):
        total = 0
        claimed_credit = 0
        claimed_credit += self._claimed_credit(self)
        for dependent in self.dependent_set.all():
            for claim in dependent.claim_set.all():
                for claim_coverage in claim.claimcoverage_set.all():
                    if not claim_coverage.actual_paid_date:
                        continue
                    total += claim_coverage.expected_back
            claimed_credit += self._claimed_credit(dependent)
        for claim in self.claim_set.all():
            for claim_coverage in claim.claimcoverage_set.all():
                if not claim_coverage.actual_paid_date:
                    continue
                total += claim_coverage.expected_back

        referral_credit = self.referral_set.all().aggregate(
            models.Sum('credit_value')
        )['credit_value__sum'] or 0

        credit = (
            (total / decimal.Decimal(150)) -
            decimal.Decimal(claimed_credit) +
            decimal.Decimal(referral_credit)
        )

        return round(credit, 2)

    def get_absolute_url(self):
        return urlresolvers.reverse_lazy(
            'client', kwargs={'client_id': self.id}
        )

    def __str__(self):
        return self.full_name()


class Note(models.Model):
    client = models.ForeignKey(Client)

    notes = models.TextField()

    created = models.DateTimeField(auto_now_add=True)

    def get_additional_data(self):
        # track client_id so we can look it up via auditlog
        # update api_helpers.HistoryMixin if this changes
        return {
            'client_id': self.client_id,
        }

    def __str__(self):
        return '{} - {} - Client ID: {}'.format(
            self.notes, self.created, self.client_id
        )


class Dependent(Person):
    SPOUSE = 's'
    CHILD = 'c'
    RELATIONSHIPS = ((SPOUSE, 'Spouse'),
                     (CHILD, 'Child'))

    primary = models.ForeignKey(Client)
    relationship = models.CharField(
        "Relationship", max_length=4, choices=RELATIONSHIPS)

    def get_additional_data(self):
        # track client_id so we can look it up via auditlog
        # update api_helpers.HistoryMixin if this changes
        return {
            'client_id': self.primary_id,
        }

    def get_absolute_url(self):
        url = '{}?toggle=dependents#dependent_{}'.format(
            urlresolvers.reverse(
                'client', kwargs={'client_id': self.primary_id}
            ),
            self.pk
        )

        return url

    def __str__(self):
        return self.full_name()
