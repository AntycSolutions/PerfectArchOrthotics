from datetime import date, timedelta
import collections

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

from utils import model_utils

'''
    Char/Text Field is always set to '', doesnt need null=True
    All others need a null=True if blank=True
'''


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

    # ModelInheritance
    # Client, Dependent
    # ManyToManyField
    # Insurance
    # ForeignKey
    # Client, Insurance, Coverage, Claim

    def full_name(self):
        if self.first_name or self.last_name:
            return "%s %s" % (self.first_name, self.last_name)
        return None

    def get_absolute_url(self):
        try:
            return Client.objects.get(id=self.id).get_absolute_url()
        except:
            pass
        try:
            return Dependent.objects.get(id=self.id).get_absolute_url()
        except:
            pass
        return None

    def get_client(self):
        try:
            return Client.objects.get(id=self.id)
        except:
            pass
        try:
            return Dependent.objects.get(id=self.id).client
        except:
            pass
        return None

    def __unicode__(self):
        return self.full_name()

    def __str__(self):
        return self.__unicode__()


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

    # ForeignKey
    # Client, Dependent

    def age(self):
        if self.birth_date.year:
            return date.today().year - self.birth_date.year
        return None

    def credit(self):
        total = 0
        claimed_credit = 0
        for order in self.order_set.all():
            claimed_credit += order.credit_value
            if order.shoe:
                claimed_credit += order.shoe.credit_value
        for dependent in self.dependent_set.all():
            for claim in dependent.claim_set.all():
                if not claim.insurance_paid_date:
                    continue
                total += claim.total_expected_back()
                # for invoice in claim.invoice_set.all():
                    # total += (invoice.payment_made + invoice.deposit)
            for order in dependent.order_set.all():
                claimed_credit += order.credit_value
                if order.shoe:
                    claimed_credit += order.shoe.credit_value
        for claim in self.claim_set.all():
            if not claim.insurance_paid_date:
                continue
            total += claim.total_expected_back()
            # for invoice in claim.invoice_set.all():
                # total += invoice.payment_made + invoice.deposit
        credit = (total / 150) - claimed_credit
        return round(credit)

    def get_absolute_url(self):
        return reverse('client', kwargs={'client_id': self.id})

    def __unicode__(self):
        return self.full_name()

    def __str__(self):
        return self.__unicode__()


class Dependent(Person):
    SPOUSE = 's'
    CHILD = 'c'
    RELATIONSHIPS = ((SPOUSE, 'Spouse'),
                     (CHILD, 'Child'))

    client = models.ForeignKey(
        Client, verbose_name="Client")
    relationship = models.CharField(
        "Relationship", max_length=4, choices=RELATIONSHIPS,
        blank=True)

    def get_absolute_url(self):
        return "%s#%s" % (reverse('client',
                                  kwargs={'client_id': self.client.id}),
                          self.id)

    def __unicode__(self):
        return self.full_name()

    def __str__(self):
        return self.__unicode__()


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
        "Contract Number", max_length=128,
        blank=True)
    benefits = models.CharField(
        "Benefits", max_length=4, choices=BENEFITS,
        blank=True)
    three_d_laser_scan = models.BooleanField(
        "3D Laser Scan", default=False)
    insurance_card = models.BooleanField(
        "Insurance Card", default=False)

    claimants = models.ManyToManyField(
        Person, verbose_name="claimants", through="Coverage",
        related_name="claimants")

    # ForeignKey
    # Coverage

    def __unicode__(self):
        try:
            main_claimant = self.main_claimant
        except:
            main_claimant = None
        return "%s - %s" % (self.provider, main_claimant)

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

    # ManyToManyField
    # Claim
    # ForeignKey
    # ClaimCoverage

    def total_amount_claimed(self):
        total_amount_claimed = 0
        for claim_coverage in self.claimcoverage_set.all():
            total_amount_claimed += claim_coverage.expected_back
        return total_amount_claimed

    def claim_amount_remaining(self):
        return self.max_claim_amount - self.total_amount_claimed()

    def total_quantity_claimed(self):
        total_quantity_claimed = 0
        for claim_coverage in self.claimcoverage_set.all():
            for claim_item in claim_coverage.claimitem_set.all():
                total_quantity_claimed += claim_item.quantity
        return total_quantity_claimed

    def quantity_remaining(self):
        return self.max_quantity - self.total_quantity_claimed()

    def __unicode__(self):
        try:
            insurance = self.insurance
        except:
            insurance = None
        try:
            claimant = self.claimant
        except:
            claimant = None
        return "%s %s - %s" % (
            self.get_coverage_type_display(), claimant, insurance)

    def __str__(self):
        return self.__unicode__()


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
    unit_price = models.IntegerField(
        "Unit Price", default=0)

    # ManyToManyField
    # Claim
    # ForeignKey
    # ClaimItem

    def get_absolute_url(self):
        return reverse('item_detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return "%s %s" % (self.product_code, self.description)

    def __str__(self):
        return self.__unicode__()


class Claim(models.Model):
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

    def total_max_expected_back_quantity(self):
        Totals = collections.namedtuple('Totals', ['total_max_expected_back',
                                                   'total_max_quantity'])
        total_max_expected_back = 0
        total_max_quantity = 0
        for claim_coverage in self.claimcoverage_set.all():
            maxes = claim_coverage.max_expected_back_quantity()
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

    def __unicode__(self):
        try:
            patient = self.patient
        except:
            patient = None
        try:
            insurance = self.insurance
        except:
            insurance = None
        return "Submitted Datetime: %s %s - %s" % (
            self.submitted_datetime.strftime("%Y-%m-%d %I:%M %p"),
            patient,
            insurance)

    def __str__(self):
        return self.__unicode__()


class ClaimCoverage(models.Model):
    claim = models.ForeignKey(
        Claim, verbose_name="Claim")
    coverage = models.ForeignKey(
        Coverage, verbose_name="Coverage")

    items = models.ManyToManyField(
        Item, verbose_name="Items", through="ClaimItem")

    expected_back = models.IntegerField(
        "Expected Back", default=0)

    # ManyToManyField
    # Claim

    def total_amount_quantity(self):
        Totals = collections.namedtuple('Totals', ['total_amount',
                                                   'total_quantity'])
        total_amount = 0
        total_quantity = 0
        for claim_item in self.claimitem_set.all():
            total_amount += claim_item.amount()
            total_quantity += claim_item.quantity
        return Totals(total_amount, total_quantity)

    def _coverage_total_amount_claimed(self):
        total_amount_claimed = 0
        claim_coverages = self.coverage.claimcoverage_set.exclude(pk=self.pk)
        for claim_coverage in claim_coverages:
            if (claim_coverage.claim.submitted_datetime
                    < self.claim.submitted_datetime):
                total_amount_claimed += claim_coverage.expected_back
        return total_amount_claimed

    def _coverage_claim_amount_remaining(self):
        return (self.coverage.max_claim_amount
                - self._coverage_total_amount_claimed())

    def max_expected_back_quantity(self):
        Maxes = collections.namedtuple('Maxes', ['max_expected_back',
                                                 'max_quantity'])

        totals = self.total_amount_quantity()
        max_expected_back = min(
            self._coverage_claim_amount_remaining(),
            (totals.total_amount * (self.coverage.coverage_percent / 100))
        )
        max_quantity = totals.total_quantity

        quantity_remaining = self.coverage.quantity_remaining()
        if totals.total_quantity <= quantity_remaining:
            return Maxes(max_expected_back, max_quantity)
        else:
            max_expected_back = 0
            max_quantity = 0

        claim_item_dict = collections.defaultdict(int)
        for claim_item in self.claimitem_set.all():
            claim_item_dict[claim_item.item.unit_price] += claim_item.quantity

        while (max_quantity < (quantity_remaining + totals.total_quantity)):
            values = list(claim_item_dict.values())
            keys = list(claim_item_dict.keys())
            max_unit_price = keys[values.index(max(values))]
            max_expected_back += max_unit_price
            claim_item_dict[max_unit_price] -= 1
            if claim_item_dict[max_unit_price] == 0:
                claim_item_dict.pop(max_unit_price)
            max_quantity += 1

        return Maxes(max_expected_back, max_quantity)

    def __unicode__(self):
        try:
            coverage = self.coverage
        except:
            coverage = None
        try:
            claim = self.claim
        except:
            claim = None
        return "%s - %s" % (coverage, claim)

    def __str__(self):
        return self.__unicode__()


class ClaimItem(models.Model):
    claim_coverage = models.ForeignKey(
        ClaimCoverage, verbose_name="Claim Coverage")
    item = models.ForeignKey(
        Item, verbose_name="Item")

    quantity = models.IntegerField(
        "Quantity", default=0)

    # ManyToManyField
    # ClaimCoverage

    def amount(self):
        return self.item.unit_price * self.quantity

    def __unicode__(self):
        return "%s - %s" % (self.item, self.claim_coverage)

    def __str__(self):
        return self.__unicode__()


class Invoice(models.Model):
    CASH = "ca"
    CHEQUE = "ch"
    CREDIT = "cr"
    PAYMENT_TYPES = ((CASH, "Cash"),
                     (CHEQUE, "Cheque"),
                     (CREDIT, "Credit"))
    DUE_ON_RECEIPT = 'dor'
    PAYMENT_TERMS = ((DUE_ON_RECEIPT, 'Due On Receipt'),)

    claim = models.ForeignKey(
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

    def balance(self):
        totals = self.claim.total_amount_quantity_claimed()
        return (totals.total_amount_claimed
                - self.deposit
                - self.payment_made)

    def __unicode__(self):
        return "Invoice Date: %s - %s" % (self.invoice_date, self.claim)

    def __str__(self):
        return self.__unicode__()


class InsuranceLetter(models.Model):
    claim = models.ForeignKey(
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
        for invoice in self.claim.invoice_set.all():
            return invoice.invoice_date
        return None

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

    def __unicode__(self):
        # Needs better choice than practitioner_name
        return "Dispense Date: %s - %s" % (self.dispense_date(), self.claim)

    def __str__(self):
        return self.__unicode__()


class ProofOfManufacturing(models.Model):
    claim = models.ForeignKey(
        Claim, verbose_name="Claim")

    bill_to = settings.BILL_TO[0][1]
    ship_to = settings.BILL_TO[0][1]

    # MOLL
    laboratory = settings.LABORATORIES[0][1]
    laboratory_information = laboratory.split('\n')[0]
    laboratory_supervisor = laboratory.split('\n')[6].replace(
        'Laboratory Supervisor:', '')
    laboratory_address = laboratory.replace(laboratory.split('\n')[6], '')

    proof_of_manufacturing_date_verbose_name = "Proof of Manufacturing Date"

    def proof_of_manufacturing_date(self):
        for invoice in self.claim.invoice_set.all():
            if invoice.invoice_date:
                return invoice.invoice_date - timedelta(weeks=1)
        return None

    def __unicode__(self):
        return "Proof of Manufacturing Date: %s - %s" % (
            self.proof_of_manufacturing_date(), self.claim)

    def __str__(self):
        return self.__unicode__()


class Laboratory(models.Model):
    # Dont set default on information, or itll mess up FormSets
    information = models.CharField(
        "Information", max_length=8, choices=settings.LABORATORIES)
    insurance_letter = models.ForeignKey(
        InsuranceLetter, verbose_name="Insurance Letter",
        null=True, blank=True)

    def __unicode__(self):
        return self.get_information_display().split('\n')[0]

    def __str__(self):
        return self.__unicode__()


class SiteStatistics(models.Model):

    def outstanding_fees(self):
        return 0

    def number_of_clients_with_outstanding_fees(self):
        return 0

    def revenue(self):
        revenue = 0
        for invoice in Invoice.objects.all():
            revenue += invoice.payment_made + invoice.deposit
        return revenue

    def __unicode__(self):
        # Shouldnt be called
        return "Site Statistics (%s)" % self.pk

    def __str__(self):
        return self.__unicode__()
