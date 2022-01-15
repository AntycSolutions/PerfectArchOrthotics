from django.db import models
from django.core import urlresolvers, exceptions
from django.utils import timezone

from datetime import time

from .clients import Person


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

    def get_additional_data(self):
        # track client_id so we can look it up via auditlog
        # update api_helpers.HistoryMixin if this changes
        return {
            'client_id': self.main_claimant_id,
        }

    def get_absolute_url(self):
        url = '{}?toggle=insurances#insurance_{}'.format(
            urlresolvers.reverse(
                'client',
                kwargs={'client_id': self.main_claimant.get_client().pk}
            ),
            self.pk
        )

        return url

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
    KNEE_BRACE = 'kb'
    WRIST_BRACE = 'wb'
    ANKLE_BRACE = 'ab'
    TENS_MACHINE = 'tm'
    SHOULDER_BRACE = 'sb'
    NECK_BRACE = 'nb'
    OTHER_MEDICAL_EQUIPMENT = 'om'
    COVERAGE_TYPES = (
        (ORTHOTICS, "Orthotics"),
        (COMPRESSION_STOCKINGS, "Compression Stockings"),
        (ORTHOPEDIC_SHOES, "Orthopedic Shoes"),
        (BACK_SUPPORT, "Back Support"),
        (KNEE_BRACE, "Knee Brace"),
        (WRIST_BRACE, "Wrist Brace"),
        (ANKLE_BRACE, "Ankle Brace"),
        (TENS_MACHINE, 'TENS Machine'),
        (SHOULDER_BRACE, 'Shoulder Brace'),
        (NECK_BRACE, 'Neck Brace'),
        (OTHER_MEDICAL_EQUIPMENT, 'Other Medical Equipment'),
    )
    BENEFIT_YEAR = 1
    CALENDAR_YEAR = 2
    TWELVE_ROLLING_MONTHS = 12
    TWENTY_FOUR_ROLLING_MONTHS = 24
    THIRTY_SIX_ROLLING_MONTHS = 36
    PERIODS = (
        (TWELVE_ROLLING_MONTHS, "12 Rolling Months"),
        (TWENTY_FOUR_ROLLING_MONTHS, "24 Rolling Months"),
        (THIRTY_SIX_ROLLING_MONTHS, "36 Rolling Months"),
        (BENEFIT_YEAR, "Benefit Year"),
        (CALENDAR_YEAR, "Calendar Year"),
    )

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
        "Period", choices=PERIODS)
    period_date = models.DateField(
        "Period Date",
        blank=True, null=True)

    money_fields = ['max_claim_amount']

    # ManyToManyField
    # Claim
    # ForeignKey
    # ClaimCoverage

    def get_additional_data(self):
        # track client_id so we can look it up via auditlog
        # update api_helpers.HistoryMixin if this changes
        return {
            'client_id': self.claimant_id,
        }

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
        else:
            raise Exception("unknown period _get_start_end_period_dates")

        return period_start_date, period_end_date

    def total_amount_claimed_period(self):
        period_start_date, period_end_date = self._get_start_end_period_dates()

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
        return self.max_claim_amount - self.total_amount_claimed_period()

    def total_quantity_claimed_period(self):
        period_start_date, period_end_date = self._get_start_end_period_dates()

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
        return self.max_quantity - self.total_quantity_claimed_period()

    MISSING_PERIOD_DATE = "Benefit Year requires Period Date to be set"

    def clean(self):
        if self.period == self.BENEFIT_YEAR and self.period_date is None:
            msg = self.MISSING_PERIOD_DATE
            raise exceptions.ValidationError({
                'period': msg,
                'period_date': msg,
            })

    def get_absolute_url(self):
        url = '{}?toggle=insurances#insurance_{}'.format(
            urlresolvers.reverse(
                'client',
                kwargs={'client_id': self.claimant.get_client().pk}
            ),
            self.insurance.pk
        )

        return url

    def __str__(self):
        return "[{}] {} - Insurance ID: {} - Person ID: {}".format(
            self.pk,
            self.get_coverage_type_display(),
            self.insurance_id,
            self.claimant_id
        )
