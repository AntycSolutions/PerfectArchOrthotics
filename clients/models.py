from datetime import date
from django.db import models
from django.conf import settings

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

    # ForeignKey
    # Client, Dependent

    def full_name(self):
        if self.first_name or self.last_name:
            return "%s %s" % (self.first_name, self.last_name)
        return None

    def __unicode__(self):
        return "Person - %s" % (self.full_name())

    def __str__(self):
        return self.__unicode__()


class Dependent(Person):
    SPOUSE = 's'
    CHILD = 'c'
    RELATIONSHIPS = ((SPOUSE, 'Spouse'),
                     (CHILD, 'Child'))

    relationship = models.CharField(
        "Relationship", max_length=4, choices=RELATIONSHIPS,
        blank=True)

    # ManyToMany
    # Client

    def __unicode__(self):
        return "Dependent - %s" % (self.full_name())

    def __str__(self):
        return self.__unicode__()


class Client(Person):
    address = models.CharField(
        "Address", max_length=128,
        blank=True)
    city = models.CharField(
        "City", max_length=128,
        blank=True)
    postal_code = models.CharField(
        "Postal Code", max_length=6,
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
    health_care_number = models.CharField(
        "Health Care Number", max_length=20,
        blank=True)
    employer = models.CharField(
        "Employer", max_length=128,
        blank=True)
    credit = models.SmallIntegerField(
        "Credit", default=0)
    referred_by = models.CharField(
        "Referred By", max_length=128,
        blank=True)
    notes = models.TextField(
        "Notes",
        blank=True)
    dependents = models.ManyToManyField(
        Dependent, verbose_name="Dependents",
        blank=True, null=True)

    # Foreign keys
    # Insurance, Claim

    def age(self):
        if self.birth_date.year:
            return date.today().year - self.birth_date.year
        return None

    def __unicode__(self):
        return "Client - %s" % (self.full_name())

    def __str__(self):
        return self.__unicode__()


class Insurance(models.Model):
    DIRECT = "d"
    INDIRECT = "i"
    BILLINGS = ((DIRECT, "Direct"),
                (INDIRECT, "Indirect"))

    client = models.ForeignKey(
        Client, verbose_name="Client")
    # A spouse can have their own insurance
    spouse = models.ForeignKey(
        Dependent, verbose_name="Spouse",
        blank=True, null=True)
    provider = models.CharField(
        "Provider", max_length=128,
        blank=True)
    policy_number = models.CharField(
        "Policy Number", max_length=128,
        blank=True)
    contract_number = models.CharField(
        "Contract Number", max_length=128,
        blank=True)
    billing = models.CharField(
        "Billing", max_length=4, choices=BILLINGS,
        blank=True)
    gait_scan = models.BooleanField(
        "Gait Scan", default=False)
    insurance_card = models.BooleanField(
        "Insurance Card", default=False)

    # ForeignKey
    # CoverageType

    def __unicode__(self):
        return "Insurance - %s - %s" % (self.provider, self.client)

    def __str__(self):
        return self.__unicode__()


class CoverageType(models.Model):
    ORTHOTICS = "o"
    COMPRESSION_STOCKINGS = "cs"
    ORTHOPEDIC_SHOES = "os"
    COVERAGE_TYPES = ((ORTHOTICS, "Orthotics"),
                      (COMPRESSION_STOCKINGS, "Compression Stockings"),
                      (ORTHOPEDIC_SHOES, "Orthopedic Shoes"))
    BENEFIT_YEAR = 1
    CALENDAR_YEAR = 2
    TWELVE_ROLLING_MONTHS = 12
    TWENTY_FOUR_ROLLING_MONTHS = 24
    THIRTY_SIX_ROLLING_MONTHS = 36
    PERIODS = ((TWELVE_ROLLING_MONTHS, '12 Rolling Months'),
               (TWENTY_FOUR_ROLLING_MONTHS, '24 Rolling Months'),
               (THIRTY_SIX_ROLLING_MONTHS, '36 Rolling Months'),
               (BENEFIT_YEAR, 'Benefit Year'),
               (CALENDAR_YEAR, 'Calendar Year'))

    insurance = models.ForeignKey(
        Insurance, verbose_name="Insurance")
    coverage_type = models.CharField(
        "Coverage Type", max_length=4, choices=COVERAGE_TYPES,
        blank=True)
    coverage_percent = models.IntegerField(
        "Coverage Percent", default=0)
    max_claim_amount = models.IntegerField(
        "Max Claim Amount", default=0)
    total_claimed = models.IntegerField(
        "Total Claimed", default=0)
    quantity = models.IntegerField(
        "Quantity", default=0)
    period = models.IntegerField(
        "Period", choices=PERIODS,
        blank=True, null=True)

    # ForeignKey
    # Claim

    def coverage_remaining(self):
        return self.max_claim_amount - self.total_claimed

    def __unicode__(self):
        return "Coverage Type - %s - %s" % (self.get_coverage_type_display(),
                                            self.insurance)

    def __str__(self):
        return self.__unicode__()


class Claim(models.Model):
    CASH = "ca"
    CHEQUE = "ch"
    CREDIT = "cr"
    PAYMENTS = ((CASH, "Cash"),
                (CHEQUE, "Cheque"),
                (CREDIT, "Credit"))

    client = models.ForeignKey(
        Client, verbose_name="Client")
    patient = models.ForeignKey(
        Person, verbose_name="Patient", related_name="patient",
        blank=True, null=True)
    coverage_types = models.ManyToManyField(
        CoverageType, verbose_name="Coverage Types",
        blank=True, null=True)
    submitted_date = models.DateField(
        "Submitted Date", auto_now_add=True)
    paid_date = models.DateField(
        "Paid Date",
        blank=True, null=True)
    amount_claimed = models.IntegerField(
        "Amount Claimed", default=0)
    # TODO validate based on clients insurance, amount left in coverage
    #  and coverage percent
    expected_back = models.IntegerField(
        "Expected Back", default=0)
    payment_type = models.CharField(
        "Payment Type", max_length=4, choices=PAYMENTS,
        blank=True)

    # ForeignKey
    # Invoice, InsuranceLetter, ProofOfManufacturing

    def __unicode__(self):
        return "Claim - %s - %s" % (self.submitted_date, self.client)

    def __str__(self):
        return self.__unicode__()


class Invoice(models.Model):
    ASSIGNMENT = "a"
    NON_ASSIGNMENT = "na"
    PAYMENT_TYPES = ((ASSIGNMENT, "Assignment"),
                     (NON_ASSIGNMENT, "Non-assignment"))

    claim = models.ForeignKey(
        Claim, verbose_name="Claim")
    dispensed_by = models.CharField(
        "Dispensed By", max_length=128,
        blank=True)
    payment_type = models.CharField(
        "Payment Type", max_length=4, choices=PAYMENT_TYPES,
        blank=True)
    payment_terms = models.CharField(
        "Payment Terms", max_length=256,
        blank=True)
    payment_made = models.IntegerField(
        "Payment Made", default=0)

    # ForeignKey
    # Item

    def balance(self):
        if (self.total() != 0) and self.payment_made:
            return self.total() - self.payment_made
        return None

    def total(self):
        total = 0
        for item in self.item_set.all():
            total += item.total()
        return total

    def __unicode__(self):
        return "Invoice - %s - %s" % (self.dispensed_by, self.claim)

    def __str__(self):
        return self.__unicode__()


class Item(models.Model):
    invoice = models.ForeignKey(
        Invoice, verbose_name="Invoice")
    description = models.CharField(
        "Description", max_length=512,
        blank=True)
    unit_price = models.IntegerField(
        "Unit Price", default=0)
    quantity = models.IntegerField(
        "Quantity", default=0)

    def total(self):
        return self.unit_price * self.quantity

    def __unicode__(self):
        return "Item - %s - %s" % (self.description, self.invoice)


class InsuranceLetter(models.Model):
    claim = models.ForeignKey(
        Claim, verbose_name="Claim")

    practitioner_name = models.CharField(
        "Practitioner Name", max_length=128, choices=settings.PRACTITIONERS,
        default=settings.DM,
        blank=True)
    biomedical_and_gait_analysis_date = models.DateField(
        "Biomedical and Gait Analysis Date",
        blank=True, null=True)
    examiner = models.CharField(
        "Examiner", max_length=128,
        blank=True)
    dispensing_practitioner = models.CharField(
        "Dispensing Practitioner", max_length=128,
        blank=True)
    dispense_date = models.DateField(
        "Dispense Date",
        blank=True, null=True)

    orthopedic_shoes = models.BooleanField(
        "Orthopedic Shoes", default=False)
    foot_orthotics_orthosis = models.BooleanField(
        "Foot Orthotics Orthosis", default=False)
    internally_modified_footwear = models.BooleanField(
        "Internally Modified Orthosis", default=False)

    foam_plaster = models.BooleanField(
        "Foam / Plaster", default=False)
    gaitscan = models.BooleanField(
        "Gait Scan(TM)", default=False)

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

    # ForeignKey
    # Laboratory

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

        if diagnosis:
            diagnosis.append("as per prescription.")

        # Remove list characters
        return str(diagnosis).strip("[]").replace("'", "")

    def __unicode__(self):
        return "Insurance Letter - %s - %s" % (self.practitioner_name,
                                               self.claim)

    def __str__(self):
        return self.__unicode__()


class ProofOfManufacturing(models.Model):
    claim = models.ForeignKey(
        Claim, verbose_name="Claim")

    invoice_date = models.DateField(
        "Invoice Date",
        blank=True, null=True)

    product = models.CharField(
        "Product", max_length=256,
        blank=True)
    quantity = models.IntegerField(
        "Quantity", default=0)

    laboratory_supervisor = models.CharField(
        "Laboratory Supervisor", max_length=128,
        blank=True)
    raw_materials = models.TextField(
        "Raw Materials",
        blank=True)
    manufacturing = models.TextField(
        "Manufacturing",
        blank=True)
    casting_technique = models.TextField(
        "Casting Technique",
        blank=True)

    # ForeignKey
    # Laboratory

    def __unicode__(self):
        return "Proof of Manufacturing - %s - %s" % (self.product,
                                                     self.claim)

    def __str__(self):
        return self.__unicode__()


class Laboratory(models.Model):
    # Dont set default on information, or itll mess up FormSets
    information = models.CharField(
        "Information", max_length=8, choices=settings.LABORATORIES)
    insurance_letter = models.ForeignKey(
        InsuranceLetter, verbose_name="Insurance Letter",
        null=True, blank=True)
    proof_of_manufacturing = models.ForeignKey(
        ProofOfManufacturing, verbose_name="Proof of Manufacturing",
        null=True, blank=True)

    def __unicode__(self):
        return "Laboratory - %s - %s" % (self.name,
                                         self.insurance_letter)

    def __str__(self):
        return self.__unicode__()


class SiteStatistics(models.Model):
    home_page_views = models.IntegerField(default=0)

    def outstanding_fees(self):
        return 0

    def number_of_clients_with_outstanding_fees(self):
        return 0

    def revenue(self):
        revenue = 0
        for claim in Claim.objects.all():
            revenue += claim.amount_claimed - claim.expected_back
        return revenue
