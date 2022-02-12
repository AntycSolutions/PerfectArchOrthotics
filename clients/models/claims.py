import collections
import decimal

from django.conf import settings
from django.core import urlresolvers
from django.db import models
from django.db.models import Sum, Case, When
from django.template import defaultfilters
from django.utils import timezone
from datetime import timedelta
from os import path
from utils import model_utils

from .clients import Person
from .insurance_info import Coverage, Insurance
from .items import Item


class Claim(models.Model, model_utils.FieldList):
    patient = models.ForeignKey(
        Person, verbose_name="Patient")
    insurances = models.ManyToManyField(Insurance)

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

    def get_additional_data(self):
        # track client_id so we can look it up via auditlog
        # update api_helpers.HistoryMixin if this changes
        return {
            'client_id': self.patient_id,
        }

    def has_orthotics(self):
        # check if prefetch_related has been called to avoid extra db queries
        if 'claimcoverage' in self._prefetched_objects_cache:
            for claimcoverage in self.claimcoverage_set.all():
                if 'items' in claimcoverage._prefetched_objects_cache:
                    for item in claimcoverage.items.all():
                        if item.coverage_type == Coverage.ORTHOTICS:
                            return True
        if 'coverages' in self._prefetched_objects_cache:
            for coverage in self.coverages.all():
                if coverage.coverage_type == Coverage.ORTHOTICS:
                    return True

        # prefetch_related wasn't used, query db
        has_orthotics = (
            self.coverages.filter(
                coverage_type=Coverage.ORTHOTICS
            ).exists() or
            self.claimcoverage_set.filter(
                items__coverage_type=Coverage.ORTHOTICS
            ).exists()
        )

        return has_orthotics

    def total_expected_back(self):
        total_expected_back = 0
        for claim_coverage in self.claimcoverage_set.all():
            total_expected_back += claim_coverage.expected_back

        return total_expected_back

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
        expected_back = 0
        for insurance in self.insurances.all():
            if insurance.benefits == 'a':
                claimcoverages = self.claimcoverage_set.filter(
                    coverage__insurance_id=insurance.pk
                ).aggregate(
                    expected_back=Sum(Case(
                        When(
                            actual_paid_date__isnull=False,
                            then='expected_back',
                        ),
                        default=0,
                    )),
                )

                expected_back += claimcoverages['expected_back'] or 0

        return expected_back

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

    def get_str(self):
        try:
            submitted_datetime = timezone.localtime(self.submitted_datetime)
            submitted_datetime = defaultfilters.date(
                submitted_datetime, "N j, Y, P"
            )
        except AttributeError:
            submitted_datetime = None

        return "{} - {}".format(submitted_datetime, self.patient)

    def __str__(self):
        try:
            submitted_datetime = timezone.localtime(self.submitted_datetime)
            submitted_datetime = defaultfilters.date(
                submitted_datetime, "N j, Y, P"
            )
        except AttributeError:
            submitted_datetime = None

        return "{} - Person ID: {} - Insurance IDs: {}".format(
            submitted_datetime,
            self.patient_id,
            self.insurances.values_list('pk', flat=True)
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
    DELINQUENT = 'del'
    NO_COVERAGE = 'noc'
    E_TRANSFER = 'etr'
    PAYMENT_TYPES = (
        ('Paid', (
            (CASH, "Cash"),
            (CHEQUE, "Cheque"),
            (VISA, "VISA"),
            (MASTERCARD, "MasterCard"),
            (DEBIT, "Interac Debit"),
            (E_TRANSFER, "e-Transfer"),
        )),
        ('Not paid', (
            (DELINQUENT, "Delinquent"),
            (NO_COVERAGE, "No coverage"),
        )),
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

    def _coverage_total_amount_claimed_period(self):
        period_start_date, period_end_date = \
            self.coverage._get_start_end_period_dates(
                self.claim.submitted_datetime
            )

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

    def _coverage_claim_amount_remaining_period(self):
        return (
            self.coverage.max_claim_amount -
            self._coverage_total_amount_claimed_period()
        )

    def max_expected_back_quantity_period(self):
        Maxes = collections.namedtuple('Maxes', ['max_expected_back',
                                                 'max_quantity'])

        totals = self.total_amount_quantity()
        max_expected_back = min(
            self._coverage_claim_amount_remaining_period(),
            (totals.total_amount * (
                decimal.Decimal(self.coverage.coverage_percent) / 100
            ))
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

    PERFECT_ARCH = 'pa'
    PC_MEDICAL = 'pc'
    BRACE_AND_BODY = 'bb'
    COMPANIES = (
        (PERFECT_ARCH, 'Perfect Arch'),
        (PC_MEDICAL, 'PC Medical'),
        (BRACE_AND_BODY, 'Brace and Body'),
    )
    company = models.CharField(
        max_length=2, choices=COMPANIES, default=PERFECT_ARCH
    )

    invoice_number = models.PositiveIntegerField(
        'Invoice Number', blank=True, null=True
    )
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
    payment_made = models.DecimalField(
        'Payment Made', max_digits=6, decimal_places=2,
        default=decimal.Decimal(0.00)
    )
    payment_date = models.DateField(
        "Payment Date",
        blank=True, null=True)
    deposit = models.DecimalField(
        'Deposit', max_digits=6, decimal_places=2,
        default=decimal.Decimal(0.00)
    )
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

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            # this used to just be the claim.id field
            self.invoice_number = (Invoice.objects.filter(
                company=self.company
            ).aggregate(
                max=models.Max('invoice_number')
            )['max'] or 0) + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return "{} - Claim ID: {}".format(self.invoice_date, self.claim_id)


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
            self.get_laboratory_display().split('\n')[8].replace(
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
        except (Claim.DoesNotExist, Invoice.DoesNotExist):
            pass

    def get_absolute_url(self):
        return urlresolvers.reverse_lazy(
            'fillOutProof', kwargs={'claim_id': self.claim.id}
        )

    def __str__(self):
        return "{} - Claim ID: {}".format(
            self.proof_of_manufacturing_date(), self.claim_id
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

    datetime = models.DateTimeField()

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
