import collections
import operator
import decimal
from os import path
from datetime import date, timedelta, time

from django.db import models
from django.conf import settings
from django.core import urlresolvers
from django.utils import timezone
from django.db.models import Sum, Case, When
from django.template import defaultfilters

from auditlog.registry import auditlog
from utils import model_utils


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
            return self.dependent.client
        except Dependent.DoesNotExist:
            pass

        raise Exception('Person is not tied to a Client.')

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
        Person, verbose_name="Referred By", related_name="referred_by",
        blank=True, null=True)
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

    def __str__(self):
        return '{} - {} - Client ID: {}'.format(
            self.notes, self.created, self.client_id
        )


class Dependent(Person):
    SPOUSE = 's'
    CHILD = 'c'
    RELATIONSHIPS = ((SPOUSE, 'Spouse'),
                     (CHILD, 'Child'))

    client = models.ForeignKey(
        Client, verbose_name="Client")
    relationship = models.CharField(
        "Relationship", max_length=4, choices=RELATIONSHIPS)

    def get_absolute_url(self):
        return "{0}#dependent_{1}".format(
            urlresolvers.reverse_lazy(
                'client', kwargs={'client_id': self.client.id}
            ),
            self.id
        )

    def __str__(self):
        return self.full_name()


class Insurance(models.Model):
    ASSIGNMENT = "a"
    NON_ASSIGNMENT = "na"
    BENEFITS = ((ASSIGNMENT, "Assignment"),
                (NON_ASSIGNMENT, "Non-assignment"))

    main_claimant = models.ForeignKey(
        Person, verbose_name="Claimant")
    provider = models.CharField(
        "Provider", max_length=128)
    policy_number = models.CharField(
        "Policy Number", max_length=128,
        blank=True)
    contract_number = models.CharField(
        "ID Number", max_length=128,
        blank=True)
    benefits = models.CharField(
        "Benefits", max_length=4, choices=BENEFITS)
    three_d_laser_scan = models.BooleanField(
        "3D Laser Scan", default=False)
    insurance_card = models.BooleanField(
        "Insurance Card", default=False)

    claimants = models.ManyToManyField(
        Person, verbose_name="claimants", through="Coverage",
        related_name="claimants")

    # ForeignKey
    # Coverage

    def get_absolute_url(self):
        return "{0}#insurance_{1}".format(
            urlresolvers.reverse_lazy(
                'client',
                kwargs={'client_id': self.main_claimant.get_client().id}
            ),
            self.id
        )

    def __unicode__(self):
        return "{} - Person ID: {}".format(
            self.provider, self.main_claimant_id
        )

    def __str__(self):
        return self.__unicode__()


class Coverage(models.Model):
    ORTHOTICS = "o"
    COMPRESSION_STOCKINGS = "cs"
    ORTHOPEDIC_SHOES = "os"
    BACK_SUPPORT = "bs"
    COVERAGE_TYPES = ((ORTHOTICS, "Orthotics"),
                      (COMPRESSION_STOCKINGS, "Compression Stockings"),
                      (ORTHOPEDIC_SHOES, "Orthopedic Shoes"),
                      (BACK_SUPPORT, "Back Support"))
    BENEFIT_YEAR = 1
    CALENDAR_YEAR = 2
    TWELVE_ROLLING_MONTHS = 12
    TWENTY_FOUR_ROLLING_MONTHS = 24
    THIRTY_SIX_ROLLING_MONTHS = 36
    PERIODS = ((TWELVE_ROLLING_MONTHS, "12 Rolling Months"),
               (TWENTY_FOUR_ROLLING_MONTHS, "24 Rolling Months"),
               (THIRTY_SIX_ROLLING_MONTHS, "36 Rolling Months"),
               (BENEFIT_YEAR, "Benefit Year"),
               (CALENDAR_YEAR, "Calendar Year"))

    insurance = models.ForeignKey(
        Insurance, verbose_name="Insurance")
    claimant = models.ForeignKey(
        Person, verbose_name="Claimant")

    coverage_type = models.CharField(
        "Coverage Type", max_length=4, choices=COVERAGE_TYPES,
        blank=True)
    coverage_percent = models.IntegerField(
        "Coverage Percent", default=0)
    max_claim_amount = models.IntegerField(
        "Max Claim Amount", default=0)
    max_quantity = models.IntegerField(
        "Max Quantity", default=0)
    period = models.IntegerField(
        "Period", choices=PERIODS,
        blank=True, null=True)
    period_date = models.DateField(
        "Period Date",
        blank=True, null=True)

    money_fields = ['max_claim_amount']

    # ManyToManyField
    # Claim
    # ForeignKey
    # ClaimCoverage

    # def total_amount_claimed(self):
    #     total_amount_claimed = 0
    #     # TODO: aggregate?
    #     for claim_coverage in self.claimcoverage_set.all():
    #         total_amount_claimed += claim_coverage.expected_back

    #     return total_amount_claimed

    # def claim_amount_remaining(self):
    #     return self.max_claim_amount - self.total_amount_claimed()

    def _get_start_end_period_dates(self, submitted_datetime=None):
        if not submitted_datetime:
            submitted_datetime = timezone.now()

        period = self.period
        if period == self.TWELVE_ROLLING_MONTHS:
            period_start_date = \
                submitted_datetime.replace(year=submitted_datetime.year - 1)
            period_end_date = submitted_datetime
        elif period == self.TWENTY_FOUR_ROLLING_MONTHS:
            period_start_date = \
                submitted_datetime.replace(year=submitted_datetime.year - 2)
            period_end_date = submitted_datetime
        elif period == self.THIRTY_SIX_ROLLING_MONTHS:
            period_start_date = \
                submitted_datetime.replace(year=submitted_datetime.year - 3)
            period_end_date = submitted_datetime
        elif period == self.BENEFIT_YEAR:
            period_date = self.period_date

            if not period_date:
                return None, None

            period_date = timezone.datetime.combine(period_date, time.min)
            period_date = timezone.make_aware(period_date)

            period_start_date = \
                period_date.replace(year=submitted_datetime.year)
            period_end_date = \
                period_start_date.replace(year=period_start_date.year + 1)
        elif period == self.CALENDAR_YEAR:
            period_start_date = \
                submitted_datetime.replace(month=1, day=1, hour=0)
            period_end_date = \
                period_start_date.replace(year=period_start_date.year + 1)
        elif not period:
            return None, None
        else:
            raise Exception("unknown period _get_start_end_period_dates")

        return period_start_date, period_end_date

    class PeriodException(BaseException):
        pass

    def total_amount_claimed_period(self):
        period_start_date, period_end_date = self._get_start_end_period_dates()

        if not period_start_date or not period_end_date:
            raise self.PeriodException()

        total_amount_claimed = 0
        claim_coverages = self.claimcoverage_set.filter(
            claim__submitted_datetime__range=[
                period_start_date, period_end_date
            ]
        )
        # TODO: aggregate?
        for claim_coverage in claim_coverages:
            total_amount_claimed += claim_coverage.expected_back

        return total_amount_claimed

    def claim_amount_remaining_period(self):
        try:
            return self.max_claim_amount - self.total_amount_claimed_period()
        except self.PeriodException:
            return 'Period and/or Period Date not set'

    # def total_quantity_claimed(self):
    #     total_quantity_claimed = 0
    #     claim_coverages = self.claimcoverage_set.all()
    #     # self.claimcoverage_set.prefetch_related('claimitem_set').all()
    #     # TODO: aggregate?
    #     for claim_coverage in claim_coverages:
    #         for claim_item in claim_coverage.claimitem_set.all():
    #             total_quantity_claimed += claim_item.quantity

    #     return total_quantity_claimed

    # def quantity_remaining(self):
    #     return self.max_quantity - self.total_quantity_claimed()

    def total_quantity_claimed_period(self):
        period_start_date, period_end_date = self._get_start_end_period_dates()

        if not period_start_date or not period_end_date:
            raise self.PeriodException

        total_quantity_claimed = 0
        claim_coverages = self.claimcoverage_set.prefetch_related(
            'claimitem_set'
        ).filter(
            claim__submitted_datetime__range=[
                period_start_date, period_end_date
            ]
        )
        # TODO: aggregate?
        for claim_coverage in claim_coverages:
            for claim_item in claim_coverage.claimitem_set.all():
                total_quantity_claimed += claim_item.quantity

        return total_quantity_claimed

    def quantity_remaining_period(self):
        try:
            return self.max_quantity - self.total_quantity_claimed_period()
        except self.PeriodException:
            return 'Period and/or Period Date not set'

    def __str__(self):
        return "{} - Insurance ID: {} - Person ID: {}".format(
            self.get_coverage_type_display(),
            self.insurance_id,
            self.claimant_id
        )


class Item(models.Model, model_utils.FieldList):
    COVERAGE_TYPES = Coverage.COVERAGE_TYPES
    WOMENS = 'wo'
    MENS = 'me'
    GENDERS = ((WOMENS, "Women's"),
               (MENS, "Men's"))

    coverage_type = models.CharField(
        "Coverage Type", max_length=4, choices=COVERAGE_TYPES)
    gender = models.CharField(
        "Gender", max_length=4, choices=GENDERS,
        blank=True)
    product_code = models.CharField(
        "Product Code", max_length=12, unique=True)
    # Should be name or changed to TextField
    description = models.CharField(
        "Description", max_length=128)
    cost = models.IntegerField(
        "Cost", default=0)
    unit_price = models.IntegerField(
        "Retail", default=0)

    money_fields = ['cost', 'unit_price']

    # ManyToManyField
    # Claim
    # ForeignKey
    # ClaimItem

    def get_values(self, datetime):
        # support prefetch_related with python level filtering instead of
        #  db filtering (to reduce queries) as this can be called many times
        item_histories = self.itemhistory_set.all()

        if item_histories:
            if timezone.is_naive(datetime):
                datetime = timezone.make_aware(datetime)

            item_histories_before = []
            item_histories_after = []
            for item_history in item_histories:
                if item_history.created <= datetime:
                    item_histories_before.append(item_history)
                else:
                    item_histories_after.append(item_history)

            if item_histories_before:
                item_history = max(
                    item_histories_before, key=operator.attrgetter('created')
                )
            else:
                item_history = min(
                    item_histories_after, key=operator.attrgetter('created')
                )

            unit_price = item_history.unit_price
            cost = item_history.cost
        else:
            unit_price = self.unit_price
            cost = self.cost

        return {'unit_price': unit_price, 'cost': cost}

    def get_absolute_url(self):
        return urlresolvers.reverse_lazy('item_detail', kwargs={'pk': self.pk})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # store cost/unit_price in case it changes
        self._initial_cost = self.cost
        self._initial_unit_price = self.unit_price

    def save(self, *args, **kwargs):
        initial_cost = self._initial_cost
        initial_unit_price = self._initial_unit_price
        new_cost = self.cost != initial_cost
        new_unit_price = self.unit_price != initial_unit_price
        if new_cost or new_unit_price:
            ItemHistory.objects.create(
                item=self, cost=initial_cost, unit_price=initial_unit_price
            )

        super().save(*args, **kwargs)

        self._initial_cost = self.cost
        self._initial_unit_price = self.unit_price

    def __str__(self):
        return "{} - {}".format(self.product_code, self.description)


class ItemHistory(models.Model):
    item = models.ForeignKey(Item)

    cost = models.IntegerField()

    unit_price = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Cost: ${} - Unit Price: ${} - {} - Item ID: {}'.format(
            self.cost, self.unit_price, self.created, self.item_id
        )


class Claim(models.Model, model_utils.FieldList):
    patient = models.ForeignKey(
        Person, verbose_name="Patient")
    insurance = models.ForeignKey(
        Insurance, verbose_name="Insurance")

    coverages = models.ManyToManyField(
        Coverage, verbose_name="Coverages",
        through="ClaimCoverage")

    submitted_datetime = models.DateTimeField(
        "Submitted Datetime", unique=True)
    insurance_paid_date = models.DateField(
        "Insurance Paid Date",
        blank=True, null=True)

    # ForeignKey
    # Invoice, InsuranceLetter, ProofOfManufacturing, ClaimCoverage

    def total_expected_back(self):
        total_expected_back = 0
        for claim_coverage in self.claimcoverage_set.all():
            total_expected_back += claim_coverage.expected_back

        return total_expected_back

    # def total_max_expected_back_quantity(self):
    #     Totals = collections.namedtuple('Totals', ['total_max_expected_back',
    #                                                'total_max_quantity'])
    #     total_max_expected_back = 0
    #     total_max_quantity = 0
    #     for claim_coverage in self.claimcoverage_set.all():
    #         maxes = claim_coverage.max_expected_back_quantity()
    #         total_max_expected_back += maxes.max_expected_back
    #         total_max_quantity += maxes.max_quantity

    #     return Totals(total_max_expected_back, total_max_quantity)

    def total_max_expected_back_quantity_period(self):
        Totals = collections.namedtuple('Totals', ['total_max_expected_back',
                                                   'total_max_quantity'])
        total_max_expected_back = 0
        total_max_quantity = 0
        for claim_coverage in self.claimcoverage_set.all():
            maxes = claim_coverage.max_expected_back_quantity_period()
            total_max_expected_back += maxes.max_expected_back
            total_max_quantity += maxes.max_quantity

        return Totals(total_max_expected_back, total_max_quantity)

    def total_amount_quantity_claimed(self):
        Totals = collections.namedtuple('Totals', ['total_amount_claimed',
                                                   'total_quantity_claimed'])
        total_amount_claimed = 0
        total_quantity_claimed = 0
        for claim_coverage in self.claimcoverage_set.all():
            totals = claim_coverage.total_amount_quantity()
            total_amount_claimed += totals.total_amount
            total_quantity_claimed += totals.total_quantity

        return Totals(total_amount_claimed, total_quantity_claimed)

    def expected_back_revenue(self):
        if self.insurance.benefits == 'a':
            claimcoverages = self.claimcoverage_set.aggregate(
                expected_back=Sum(Case(
                    When(
                        actual_paid_date__isnull=False,
                        then='expected_back',
                    ),
                    default=0,
                )),
            )

            return (claimcoverages['expected_back'] or 0)

        return 0

    def get_all_fields(self):
        fields = super().get_all_fields()

        fileset = self.Field(
            model_utils.FieldList.PseudoFileSet("Claim Packages"),
            self.claimattachment_set
        )
        fields.update(
            {"fileset": fileset}
        )

        return fields

    def get_absolute_url(self):
        return urlresolvers.reverse_lazy('claim', kwargs={'claim_id': self.id})

    def __str__(self):
        try:
            submitted_datetime = timezone.localtime(self.submitted_datetime)
            submitted_datetime = submitted_datetime.strftime(
                "%Y-%m-%d %I:%M %p")
        except AttributeError:
            submitted_datetime = None

        return "{} - Person ID: {} - Insurance ID: {}".format(
            submitted_datetime, self.patient_id, self.insurance_id
        )


class ClaimAttachment(models.Model):
    claim = models.ForeignKey(Claim)
    attachment = models.FileField(
        "Attachment",
        upload_to='clients/claim_packages/%Y/%m/%d'
    )

    def attachment_filename(self):
        if self.attachment:
            return path.basename(self.attachment.name)

    def __str__(self):
        return "{} - Claim ID: {}".format(
            self.attachment_filename(), self.claim_id
        )


class ClaimCoverage(models.Model):
    claim = models.ForeignKey(
        Claim, verbose_name="Claim")
    coverage = models.ForeignKey(
        Coverage, verbose_name="Coverage")

    CASH = "cas"
    CHEQUE = "che"
    VISA = "vis"
    MASTERCARD = "mas"
    DEBIT = "deb"
    PAYMENT_TYPES = (
        (CASH, "Cash"),
        (CHEQUE, "Cheque"),
        (VISA, "VISA"),
        (MASTERCARD, "MasterCard"),
        (DEBIT, "Interac Debit"),
    )
    payment_type = models.CharField(
        max_length=3, choices=PAYMENT_TYPES,
        blank=True,
    )

    items = models.ManyToManyField(
        Item, verbose_name="Items", through="ClaimItem")

    expected_back = models.IntegerField(
        "Expected Back", default=0)

    actual_paid_date = models.DateField(
        "Actual Paid Date",
        blank=True, null=True)

    money_fields = ['expected_back']

    # ManyToManyField
    # Claim

    def total_amount_quantity(self):
        Totals = collections.namedtuple('Totals', ['total_amount',
                                                   'total_quantity'])
        total_amount = 0
        total_quantity = 0
        for claim_item in self.claimitem_set.all():
            total_amount += claim_item.unit_price_amount()
            total_quantity += claim_item.quantity

        return Totals(total_amount, total_quantity)

    # def _coverage_total_amount_claimed(self):
    #     total_amount_claimed = 0
    #     claim_coverages = self.coverage.claimcoverage_set.exclude(pk=self.pk)
    #     for claim_coverage in claim_coverages:
    #         if (
    #             claim_coverage.claim.submitted_datetime <
    #             self.claim.submitted_datetime
    #                 ):
    #             total_amount_claimed += claim_coverage.expected_back

    #     return total_amount_claimed

    def _coverage_total_amount_claimed_period(self):
        period_start_date, period_end_date = \
            self.coverage._get_start_end_period_dates(
                self.claim.submitted_datetime
            )

        if not period_start_date or not period_end_date:
            return self._coverage_total_amount_claimed()

        total_amount_claimed = 0
        claim_coverages = self.coverage.claimcoverage_set.exclude(
            pk=self.pk
        ).filter(
            claim__submitted_datetime__range=[
                period_start_date, period_end_date
            ]
        )
        # TODO: aggregate?
        for claim_coverage in claim_coverages:
            total_amount_claimed += claim_coverage.expected_back

        return total_amount_claimed

    # def _coverage_claim_amount_remaining(self):
    #     return (
    #         self.coverage.max_claim_amount -
    #         self._coverage_total_amount_claimed()
    #     )

    def _coverage_claim_amount_remaining_period(self):
        return (
            self.coverage.max_claim_amount -
            self._coverage_total_amount_claimed_period()
        )

    # def max_expected_back_quantity(self):
    #     Maxes = collections.namedtuple('Maxes', ['max_expected_back',
    #                                              'max_quantity'])

    #     totals = self.total_amount_quantity()
    #     max_expected_back = min(
    #         self._coverage_claim_amount_remaining(),
    #         (totals.total_amount * (self.coverage.coverage_percent / 100))
    #     )
    #     max_quantity = totals.total_quantity

    #     quantity_remaining = self.coverage.quantity_remaining()
    #     if totals.total_quantity <= quantity_remaining:
    #         return Maxes(max_expected_back, max_quantity)
    #     else:
    #         max_expected_back = 0
    #         max_quantity = 0

    #     claim_item_dict = collections.defaultdict(int)
    #     for claim_item in self.claimitem_set.all():
    #         claim_item_dict[claim_item.get_unit_price()] += claim_item.quantity

    #     while (max_quantity < (quantity_remaining + totals.total_quantity)):
    #         if not claim_item_dict:
    #             break
    #         values = list(claim_item_dict.values())
    #         keys = list(claim_item_dict.keys())
    #         max_unit_price = keys[values.index(max(values))]
    #         max_expected_back += max_unit_price
    #         claim_item_dict[max_unit_price] -= 1
    #         if claim_item_dict[max_unit_price] == 0:
    #             claim_item_dict.pop(max_unit_price)
    #         max_quantity += 1

    #     # Should be min'd against coverage remaining
    #     return Maxes(max_expected_back, max_quantity)

    def max_expected_back_quantity_period(self):
        Maxes = collections.namedtuple('Maxes', ['max_expected_back',
                                                 'max_quantity'])

        totals = self.total_amount_quantity()
        max_expected_back = min(
            self._coverage_claim_amount_remaining_period(),
            (totals.total_amount * (self.coverage.coverage_percent / 100))
        )
        max_quantity = totals.total_quantity

        quantity_remaining = self.coverage.quantity_remaining_period()
        if totals.total_quantity <= quantity_remaining:
            return Maxes(max_expected_back, max_quantity)
        else:
            max_expected_back = 0
            max_quantity = 0

        claim_item_dict = collections.defaultdict(int)
        for claim_item in self.claimitem_set.all():
            claim_item_dict[claim_item.get_unit_price()] += claim_item.quantity

        while (max_quantity < (quantity_remaining + totals.total_quantity)):
            if not claim_item_dict:
                break
            values = list(claim_item_dict.values())
            keys = list(claim_item_dict.keys())
            max_unit_price = keys[values.index(max(values))]
            max_expected_back += max_unit_price
            claim_item_dict[max_unit_price] -= 1
            if claim_item_dict[max_unit_price] == 0:
                claim_item_dict.pop(max_unit_price)
            max_quantity += 1

        # Should be min'd against coverage remaining
        return Maxes(max_expected_back, max_quantity)

    def __str__(self):
        return "Expected Back: ${} - Claim ID: {} Coverage ID: {}".format(
            self.expected_back, self.claim_id, self.coverage_id
        )


class ClaimItem(models.Model):
    claim_coverage = models.ForeignKey(
        ClaimCoverage, verbose_name="Claim Coverage")
    item = models.ForeignKey(
        Item, verbose_name="Item")

    quantity = models.IntegerField(
        "Quantity", default=0)

    # ManyToManyField
    # ClaimCoverage

    def get_values(self):
        return self.item.get_values(
            self.claim_coverage.claim.submitted_datetime
        )

    def get_unit_price(self):
        return self.get_values()['unit_price']

    def unit_price_amount(self):
        return self.get_values()['unit_price'] * self.quantity

    def get_cost(self):
        return self.get_values()['cost']

    def cost_amount(self):
        return self.get_values()['cost'] * self.quantity

    def get_amount(self):
        values = self.get_values()

        quantity = self.quantity

        return {
            'unit_price': values['unit_price'] * quantity,
            'cost': values['cost'] * quantity,
        }

    def __str__(self):
        return "Quantity: {} - Claim Coverage ID: {} - Item ID: {}".format(
            self.quantity, self.claim_coverage_id, self.item_id
        )


class Invoice(models.Model):
    CASH = "ca"
    CHEQUE = "ch"
    CREDIT = "cr"
    PAYMENT_TYPES = ((CASH, "Cash"),
                     (CHEQUE, "Cheque"),
                     (CREDIT, "Credit"))
    DUE_ON_RECEIPT = 'dor'
    PAYMENT_TERMS = ((DUE_ON_RECEIPT, 'Due On Receipt'),)

    claim = models.OneToOneField(
        Claim, verbose_name="Claim")

    invoice_date = models.DateField(
        "Invoice Date",
        blank=True, null=True)
    dispensed_by = models.CharField(
        "Dispensed By", max_length=4, choices=settings.PRACTITIONERS,
        blank=True)
    payment_type = models.CharField(
        "Payment Type", max_length=4, choices=PAYMENT_TYPES,
        blank=True)
    payment_terms = models.CharField(
        "Payment Terms", max_length=4, choices=PAYMENT_TERMS,
        default=DUE_ON_RECEIPT,
        blank=True)
    payment_made = models.IntegerField(
        "Payment Made", default=0)
    payment_date = models.DateField(
        "Payment Date",
        blank=True, null=True)
    deposit = models.IntegerField(
        "Deposit", default=0)
    deposit_date = models.DateField(
        "Deposite Date",
        blank=True, null=True)
    estimate = models.BooleanField(
        "Estimate", default=False)

    money_fields = ['payment_made', 'deposit']

    def balance(self):
        totals = self.claim.total_amount_quantity_claimed()

        return (totals.total_amount_claimed
                - self.deposit
                - self.payment_made
                - self.claim.expected_back_revenue())

    def get_absolute_url(self):
        return urlresolvers.reverse_lazy(
            'fillOutInvoice', kwargs={'claim_id': self.claim.id}
        )

    def __str__(self):
        return "{} - Claim ID: {}".format(self.invoice_date, self.claim_id)


class InsuranceLetter(models.Model):
    claim = models.OneToOneField(
        Claim, verbose_name="Claim")

    practitioner_name = models.CharField(
        "Practitioner Name", max_length=4, choices=settings.PRACTITIONERS,
        default=settings.DM,
        blank=True)
    biomedical_and_gait_analysis_date = models.DateField(
        "Biomedical and Gait Analysis Date",
        blank=True, null=True)
    examiner = models.CharField(
        "Examiner", max_length=4, choices=settings.PRACTITIONERS,
        default=settings.DM,
        blank=True)
    dispensing_practitioner = models.CharField(
        "Dispensing Practitioner", max_length=4,
        choices=settings.PRACTITIONERS, default=settings.DM,
        blank=True)

    orthopedic_shoes = models.BooleanField(
        "Orthopedic Shoes", default=False)
    foot_orthotics_orthosis = models.BooleanField(
        "Foot Orthotics Orthosis", default=False)
    internally_modified_footwear = models.BooleanField(
        "Internally Modified Orthosis", default=False)

    foam_plaster = models.BooleanField(
        "Foam / Plaster", default=False)

    plantar_fasciitis = models.BooleanField(
        "Plantar Fasciitis", default=False)
    hammer_toes = models.BooleanField(
        "Hammer Toes", default=False)
    ligament_tear = models.BooleanField(
        "Ligament Tear / Sprain", default=False)
    knee_arthritis = models.BooleanField(
        "Knee Arthritis", default=False)
    metatarsalgia = models.BooleanField(
        "Metatarsalgia", default=False)
    drop_foot = models.BooleanField(
        "Drop Foot", default=False)
    scoliosis_with_pelvic_tilt = models.BooleanField(
        "Scoliosis With Pelvic Tilt", default=False)
    hip_arthritis = models.BooleanField(
        "Hip Arthritis", default=False)
    pes_cavus = models.BooleanField(
        "Pes Cavus", default=False)
    heel_spur = models.BooleanField(
        "Heel Spur", default=False)
    lumbar_spine_dysfunction = models.BooleanField(
        "Lumbar Spine Dysfunction", default=False)
    lumbar_arthritis = models.BooleanField(
        "Lumbar Arthritis", default=False)
    pes_planus = models.BooleanField(
        "Pes Planus", default=False)
    ankle_abnormal_rom = models.BooleanField(
        "Ankle: Abnormal ROM", default=False)
    leg_length_discrepency = models.BooleanField(
        "Leg Length Discrepancy", default=False)
    si_arthritis = models.BooleanField(
        "SI Arthritis", default=False)
    diabetes = models.BooleanField(
        "Diabetes", default=False)
    foot_abnormal_ROM = models.BooleanField(
        "Foot: Abnormal ROM", default=False)
    si_joint_dysfunction = models.BooleanField(
        "SI Joint Dysfunction", default=False)
    ankle_arthritis = models.BooleanField(
        "Ankle Arthritis", default=False)
    neuropathy = models.BooleanField(
        "Neuropathy", default=False)
    peroneal_dysfunction = models.BooleanField(
        "Peroneal Dysfunction", default=False)
    genu_valgum = models.BooleanField(
        "Genu Valgum", default=False)
    foot_arthritis = models.BooleanField(
        "Foot Arthritis", default=False)
    mtp_drop = models.BooleanField(
        "MTP Drop", default=False)
    interdigital_neuroma = models.BooleanField(
        "Interdigital Neuroma", default=False)
    genu_varum = models.BooleanField(
        "Genu Varum", default=False)
    first_mtp_arthritis = models.BooleanField(
        "1st MTP Arthritis", default=False)
    forefoot_varus = models.BooleanField(
        "Forefoot Varus", default=False)
    bunions_hallux_valgus = models.BooleanField(
        "Bunions / Hallux Valgus", default=False)
    abnormal_patellar_tracking = models.BooleanField(
        "Abnormal Patellar Tracking", default=False)
    rheumatoid_arthritis = models.BooleanField(
        "Rheumatoid Arthritis", default=False)
    forefoot_valgus = models.BooleanField(
        "Forefoot Valgus", default=False)
    abnormal_gait_tracking = models.BooleanField(
        "Abnormal Gait Timing", default=False)
    abnormal_gait_pressures = models.BooleanField(
        "Abnormal Gait Pressures", default=False)
    gout = models.BooleanField(
        "Gout", default=False)
    shin_splints = models.BooleanField(
        "Shin Splints", default=False)
    over_supination = models.BooleanField(
        "Over Supination", default=False)
    achilles_tendinitis = models.BooleanField(
        "Achilles Tendinitis", default=False)
    ulcers = models.BooleanField(
        "Ulcers", default=False)
    over_pronation = models.BooleanField(
        "Over Pronation", default=False)

    other = models.CharField(
        "Other", max_length=64,
        blank=True)

    # ForeignKey
    # Laboratory

    def dispense_date(self):
        try:
            invoice = self.claim.invoice
            if invoice.invoice_date:
                return invoice.invoice_date
        except (Claim.DoesNotExist, Invoice.DoesNotExist):
            pass

    def _verbose_name(self, field):
        return InsuranceLetter._meta.get_field(field).verbose_name

    def diagnosis(self):
        diagnosis = []

        if self.plantar_fasciitis:
            diagnosis.append(self._verbose_name('plantar_fasciitis'))
        if self.hammer_toes:
            diagnosis.append(self._verbose_name('hammer_toes'))
        if self.ligament_tear:
            diagnosis.append(self._verbose_name('ligament_tear'))
        if self.knee_arthritis:
            diagnosis.append(self._verbose_name('knee_arthritis'))
        if self.metatarsalgia:
            diagnosis.append(self._verbose_name('metatarsalgia'))
        if self.drop_foot:
            diagnosis.append(self._verbose_name('drop_foot'))
        if self.scoliosis_with_pelvic_tilt:
            diagnosis.append(self._verbose_name('scoliosis_with_pelvic_tilt'))
        if self.hip_arthritis:
            diagnosis.append(self._verbose_name('hip_arthritis'))
        if self.pes_cavus:
            diagnosis.append(self._verbose_name('pes_cavus'))
        if self.heel_spur:
            diagnosis.append(self._verbose_name('heel_spur'))
        if self.lumbar_spine_dysfunction:
            diagnosis.append(self._verbose_name('lumbar_spine_dysfunction'))
        if self.lumbar_arthritis:
            diagnosis.append(self._verbose_name('lumbar_arthritis'))
        if self.pes_planus:
            diagnosis.append(self._verbose_name('pes_planus'))
        if self.ankle_abnormal_rom:
            diagnosis.append(self._verbose_name('ankle_abnormal_rom'))
        if self.leg_length_discrepency:
            diagnosis.append(self._verbose_name('leg_length_discrepency'))
        if self.si_arthritis:
            diagnosis.append(self._verbose_name('si_arthritis'))
        if self.diabetes:
            diagnosis.append(self._verbose_name('diabetes'))
        if self.foot_abnormal_ROM:
            diagnosis.append(self._verbose_name('foot_abnormal_ROM'))
        if self.si_joint_dysfunction:
            diagnosis.append(self._verbose_name('si_joint_dysfunction'))
        if self.ankle_arthritis:
            diagnosis.append(self._verbose_name('ankle_arthritis'))
        if self.neuropathy:
            diagnosis.append(self._verbose_name('neuropathy'))
        if self.peroneal_dysfunction:
            diagnosis.append(self._verbose_name('peroneal_dysfunction'))
        if self.genu_valgum:
            diagnosis.append(self._verbose_name('genu_valgum'))
        if self.foot_arthritis:
            diagnosis.append(self._verbose_name('foot_arthritis'))
        if self.mtp_drop:
            diagnosis.append(self._verbose_name('mtp_drop'))
        if self.interdigital_neuroma:
            diagnosis.append(self._verbose_name('interdigital_neuroma'))
        if self.genu_varum:
            diagnosis.append(self._verbose_name('genu_varum'))
        if self.first_mtp_arthritis:
            diagnosis.append(self._verbose_name('first_mtp_arthritis'))
        if self.forefoot_varus:
            diagnosis.append(self._verbose_name('forefoot_varus'))
        if self.bunions_hallux_valgus:
            diagnosis.append(self._verbose_name('bunions_hallux_valgus'))
        if self.abnormal_patellar_tracking:
            diagnosis.append(self._verbose_name('abnormal_patellar_tracking'))
        if self.rheumatoid_arthritis:
            diagnosis.append(self._verbose_name('rheumatoid_arthritis'))
        if self.forefoot_valgus:
            diagnosis.append(self._verbose_name('forefoot_valgus'))
        if self.abnormal_gait_tracking:
            diagnosis.append(self._verbose_name('abnormal_gait_tracking'))
        if self.abnormal_gait_pressures:
            diagnosis.append(self._verbose_name('abnormal_gait_pressures'))
        if self.gout:
            diagnosis.append(self._verbose_name('gout'))
        if self.shin_splints:
            diagnosis.append(self._verbose_name('shin_splints'))
        if self.over_supination:
            diagnosis.append(self._verbose_name('over_supination'))
        if self.achilles_tendinitis:
            diagnosis.append(self._verbose_name('achilles_tendinitis'))
        if self.ulcers:
            diagnosis.append(self._verbose_name('ulcers'))
        if self.over_pronation:
            diagnosis.append(self._verbose_name('over_pronation'))
        if self.other:
            diagnosis.append(self.other)

        if diagnosis:
            diagnosis.append("as per prescription.")

        # Remove list characters
        return str(diagnosis).strip("[]").replace("'", "")

    def get_absolute_url(self):
        return urlresolvers.reverse_lazy(
            'fillOutInsurance', kwargs={'claim_id': self.claim.id}
        )

    def __str__(self):
        return "{} - Claim ID: {}".format(self.dispense_date(), self.claim_id)


class ProofOfManufacturing(models.Model):
    claim = models.OneToOneField(
        Claim, verbose_name="Claim")

    laboratory = models.CharField(max_length=4, choices=settings.LABORATORIES)

    proof_of_manufacturing_date_verbose_name = "Manufacturing Date"

    class Meta:
        verbose_name_plural = "Proofs of manufacturing"

    def bill_to(self):
        if self.laboratory != settings.PAOI:
            bill_to = settings.BILL_TO[0][1]
        else:
            bill_to = None

        return bill_to

    def ship_to(self):
        if self.laboratory != settings.PAOI:
            ship_to = settings.BILL_TO[0][1]
        else:
            ship_to = None

        return ship_to

    def laboratory_information(self):
        laboratory_information = \
            self.get_laboratory_display().split('\n')[0]

        return laboratory_information

    def laboratory_supervisor(self):
        laboratory_supervisor = \
            self.get_laboratory_display().split('\n')[7].replace(
                'Laboratory Supervisor:', ''
            )

        return laboratory_supervisor

    def laboratory_address(self):
        laboratory = self.get_laboratory_display()
        laboratory_address = laboratory.replace(
            laboratory.split('\n')[7], ''
        )

        return laboratory_address

    def proof_of_manufacturing_date(self):
        try:
            invoice = self.claim.invoice
            if invoice.invoice_date:
                return invoice.invoice_date - timedelta(weeks=1)
        except Claim.DoesNotExist:
            pass

    def get_absolute_url(self):
        return urlresolvers.reverse_lazy(
            'fillOutProof', kwargs={'claim_id': self.claim.id}
        )

    def __str__(self):
        return "{} - Claim ID: {}".format(
            self.proof_of_manufacturing_date(), self.claim_id
        )


class Laboratory(models.Model):
    # Dont set default on information, or itll mess up FormSets
    information = models.CharField(
        "Information", max_length=8, choices=settings.LABORATORIES)
    insurance_letter = models.ForeignKey(
        InsuranceLetter, verbose_name="Insurance Letter",
        null=True, blank=True)

    class Meta:
        verbose_name_plural = "Laboratories"

    def __str__(self):
        return self.get_information_display().split('\n')[0]


class Referral(models.Model):
    client = models.ForeignKey(Client)
    claims = models.ManyToManyField(Claim)
    credit_value = models.DecimalField(
        "Credit Value",
        max_digits=3,
        decimal_places=2,
        default=decimal.Decimal(0.00)
    )

    def __str__(self):
        return "Credit Value: {} - Client ID: {}".format(
            self.credit_value, self.client_id
        )


class Receipt(models.Model, model_utils.FieldList):
    claim = models.ForeignKey(Claim)

    DEBIT = 'd'
    CREDIT = 'c'
    CARD_TYPE_CHOICES = (
        (DEBIT, 'Debit'),
        (CREDIT, 'Credit'),
    )
    card_type = models.CharField(
        max_length=1, choices=CARD_TYPE_CHOICES,
        default=CREDIT,
    )

    VISA = 'v'
    MASTERCARD = 'm'
    INTERAC = 'i'
    CARD_COMPANY_CHOICES = (
        (VISA, 'VISA'),
        (MASTERCARD, 'MASTERCARD'),
        (INTERAC, 'INTERAC'),
    )
    card_company = models.CharField(
        max_length=1, choices=CARD_COMPANY_CHOICES,
        default=VISA,
    )

    CHIP = 'c'
    MANUAL = 'm'
    CARD_METHOD_CHOICES = (
        (CHIP, 'Chip'),
        (MANUAL, 'Manual CP'),
    )
    card_method = models.CharField(
        max_length=1, choices=CARD_METHOD_CHOICES,
        default=CHIP,
    )

    MID = models.CharField(max_length=11)
    TID = models.CharField(max_length=22)
    REF = models.CharField(max_length=8)
    batch = models.CharField(max_length=3)
    RRN = models.CharField(max_length=12, blank=True)
    APPR = models.CharField(max_length=6)
    trace = models.CharField(max_length=1)

    card_number = models.CharField(max_length=4)

    amount = models.DecimalField(max_digits=6, decimal_places=2,
                                 default=decimal.Decimal(0.00))

    AID = models.CharField(max_length=14, blank=True)
    TVR = models.CharField(max_length=14, blank=True)
    TSI = models.CharField(max_length=5, blank=True)

    money_fields = ['amount']

    def get_absolute_url(self):
        url = urlresolvers.reverse_lazy(
            'receipt_detail', kwargs={'pk': self.pk}
        )

        return url

    def __str__(self):
        return 'Amount ${} - Claim ID: {}'.format(self.amount, self.claim_id)


class CreditDivisor(models.Model):
    value = models.DecimalField(
        max_digits=5, decimal_places=2,
        default=decimal.Decimal(0.00)
    )
    created = models.DateTimeField()

    def __str__(self):
        created = defaultfilters.date(self.created, "N j, Y, P")

        return 'Value: {} - {}'.format(self.value, created)


auditlog.register(Person)
auditlog.register(Client)
auditlog.register(Note)
auditlog.register(Dependent)
auditlog.register(Insurance)
auditlog.register(Coverage)
auditlog.register(Item)
auditlog.register(ItemHistory)
auditlog.register(Claim)
auditlog.register(ClaimAttachment)
auditlog.register(ClaimCoverage)
auditlog.register(ClaimItem)
auditlog.register(Invoice)
auditlog.register(InsuranceLetter)
auditlog.register(ProofOfManufacturing)
auditlog.register(Laboratory)
auditlog.register(Referral)
auditlog.register(Receipt)
auditlog.register(CreditDivisor)
