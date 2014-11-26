"""Models for the clients app.

The following tables will be contained within:
- Dependent
- Client
- Insurance
- Claim
- Prescription

"""
from django.db import models


class Person(models.Model):
    firstName = models.CharField(max_length=128, blank=True, default="")
    lastName = models.CharField(max_length=128, blank=True, default="")

    def __unicode__(self):
        return "%s %s" % (self.firstName, self.lastName)

    def __str__(self):
        return self.__unicode__()


class Dependent(Person):

    """Model of a clients dependents.

    Fields:
    Relationship (spouse, son, daughter)
    Birthdate
    Sex

    * Each client will have a list of dependents that they are associate with.

    """
    SPOUSE = 'Spouse'
    CHILD = 'Child'
    RELATIONSHIP_CHOICES = ((SPOUSE, 'Spouse'),
                            (CHILD, 'Child'))

    MALE = 'Male'
    FEMALE = 'Female'
    GENDER_CHOICES = ((MALE, 'Male'),
                      (FEMALE, 'Female'))

    relationship = models.CharField(max_length=6, choices=RELATIONSHIP_CHOICES,
                                    blank=True, default="")
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES,
                              blank=True, default="")
    birthdate = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return "%s %s" % (self.firstName, self.lastName)

    def __str__(self):
        return self.__unicode__()


class Client(Person):

    """Model of a client.

    A client will have the following fields:
    First Name
    Last Name
    Address
    City of residence
    Postal code
    Phone #
    Cell #
    Email
    Birthdate
    Gender
    Employer
    Albeta Healthcare number
    Credit (current credit from insurance company)
    Notes (for log of communication)
    Dependents - another table
    Prescriptions - another table
    Insurance - another table

    """

    MALE = 'Male'
    FEMALE = 'Female'
    GENDER_CHOICES = ((MALE, 'Male'),
                      (FEMALE, 'Female'))

    address = models.CharField(max_length=128, blank=True, default="")
    city = models.CharField(max_length=128, blank=True, default="")
    postalCode = models.CharField(max_length=6, blank=True, default="")
    # TODO Write validators for the phone numbers below
    # In the form of (780)-937-1514
    phoneNumber = models.CharField(max_length=14, blank=True, default="")
    # In the form of (780)-937-1514
    cellNumber = models.CharField(max_length=14, blank=True, default="")
    # will cover all RFC3696/5321-compliant email addresses
    email = models.EmailField(max_length=254, blank=True, null=True)
    healthcareNumber = models.CharField(max_length=20, blank=True, default="")
    birthdate = models.DateField(blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES,
                              blank=True, default="")
    employer = models.CharField(max_length=128, blank=True, default="")
    credit = models.SmallIntegerField(blank=True, default=0)
    referredBy = models.CharField(max_length=128, blank=True, default="")
    notes = models.TextField(blank=True, default="")
    dependents = models.ManyToManyField(Dependent, blank=True, null=True)
    # Foreign key relationships
    # insurance (foreign key on other table)
    # prescriptions (foreign key on other table)
    # invoices (foreign key on other table)
    # claims (foreign key on other table)

    def __unicode__(self):
        return "%s %s" % (self.firstName, self.lastName)

    def __str__(self):
        return self.__unicode__()

    def getAge(self):
        """Calculate clients age in years."""
        pass


class Insurance(models.Model):

    """Model of a clients insurance coverage.

    This is meant to cover most of the cases of how coverage would work.
    Following are some examples:

    1) Some plans have a pool for coverage, say $10,000 for everything per
    year per person under the insurance plan. This includes primaries
    and dependents.

    EX. $10,000 can be used for eveything, dental, orthotics, hospital etc.
    Once you go over that $10,000 nothing else is covered

    Modeling:
    Have the total coverage amount, amount remaining of that total, amount
    we have claimed against it. Coverage % would likely be 100% until that
    limit is reached and then the coverage % won't be considered. Billing
    can still be of certain types and the roll-over timeframe can be set
    as normal

    2) More common are plans as follows. The client has a max for each expense,
    normally covering themselves and dependents.

    EX. Dental will have $500 per year, orthotics will have $300 max
        every three years.

    Modeling:
    Have the total coverage amount, amount remaining and amount claimed. The
    calc for amount remaining should be as easy as taking the total and minus
    the amount claimed. However this may change if they go elsewhere for
    something that is covered elsewhere and then comes back to us. The amount
    remaining then should be dynamic and calculated separately from our
    numbers. (Have to ask Danny) Coverage % may be different for each plan,
    say some will be 50%, others 100% and will obviously drop to 0% once the
    coverage is used during the roll-over timeframe.

    Insurance will have the following fields:
    Provider
    Policy #
    Contract #
    coverage %
    Benefit year (when the insurers benefit period renews):
    1) Calendar Year (Jan 1)
    2) could be a specific month in the year
    Example: April 1

    Direct/indirect billing

    Notes:
    coverage conditions
    Husband and Wifes coverage (there could be multiple policies)
    Reporting:

    """
    BILLING_CHOICES = (("Direct", "Direct"),
                       ("Indirect", "Indirect"))

    client = models.ForeignKey(Client)
    spouse = models.ForeignKey(Dependent, blank=True, null=True)
    provider = models.CharField(max_length=128, blank=True, default="")
    policyNumber = models.CharField(max_length=128, blank=True, default="")
    contractNumber = models.CharField(max_length=128, blank=True, default="")
    billing = models.CharField(max_length=8, choices=BILLING_CHOICES,
                               blank=True, default="")
    gaitScan = models.BooleanField(default=False)
    insuranceCard = models.BooleanField(default=False)

    def __unicode__(self):
        clientName = self.client.firstName + " " + self.client.lastName
        return "Insurance - %s - %s" % (clientName, self.provider)

    def __str__(self):
        return self.__unicode__()


class CoverageType(models.Model):

    """This class will represent coverage types.

    There are three types:
    COVERAGE_TYPE = (("Orthotics", "Orthotics"),
                 ("Compression_stockings", "Compression Stockings"),
                 ("Orthopedic_shoes", "Orthopedic Shoes"))

    Other fields will include:
    - Covergae %
    - Max claim amount
    - Quantitiy in pair(s)
    - Period

    """
    COVERAGE_TYPE = (("Orthotics", "Orthotics"),
                     ("Compression_stockings", "Compression Stockings"),
                     ("Orthopedic_shoes", "Orthopedic Shoes"))

    insurance = models.ForeignKey(Insurance)
    coverageType = models.CharField(max_length=21, choices=COVERAGE_TYPE,
                                    blank=True, default="")
    coveragePercent = models.IntegerField(blank=True, null=True)
    maxClaimAmount = models.IntegerField(default=0, blank=True)
    totalClaimed = models.IntegerField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    period = models.IntegerField(default=1)

    def __unicode__(self):
        return "%s - Coverage percent: %s" % (self.coverageType,
                                              self.coveragePercent)


class Claim(models.Model):

    """Model of a claim submitted for a clients.

    Claims will have the following fields:
    Submitted date
    invoice date
    paid date
    client/dependent
    insurance
    amount claimed
    expected back
    payment type (cash, cheque, credit)
    Look up report types from google docs

    """

    PAYMENT_CHOICES = (("CASH", "Cash"),
                       ("CHEQUE", "Cheque"),
                       ("CREDIT", "Credit"))
    CLAIM_TYPE = (("Orthotics", "Orthotics"),
                  ("Compression_stockings", "Compression Stockings"),
                  ("Orthopedic_shoes", "Orthopedic Shoes"))

    client = models.ForeignKey(Client, blank=True, null=True,
                               related_name="uses_coverage_of")
    patient = models.ForeignKey(Person, blank=True, null=True)
    # TODO figure out how to get the insurance from the client to calidate this
    # TODO remove this, coveraged the the insurance claim model now
    insurance = models.ForeignKey(Insurance, blank=True, null=True)
    submittedDate = models.DateTimeField(auto_now_add=True)
    invoiceDate = models.DateTimeField(blank=True, null=True)
    paidDate = models.DateTimeField(blank=True, null=True)
    amountClaimed = models.IntegerField(blank=True, default=0)
    # TODO validate based on clients insurance, amount left in coverage
    #  and coverage percent
    expectedBack = models.IntegerField(blank=True, default=0)
    paymentType = models.CharField(max_length=6, choices=PAYMENT_CHOICES,
                                   blank=True, default="")
    claimType = models.CharField(max_length=21, choices=CLAIM_TYPE,
                                 blank=True, default="")

    def __unicode__(self):
        return "Claim - %s %s" % (self.client.firstName, self.client.lastName)

    def __str__(self):
        return self.__unicode__()


class InsuranceClaim(models.Model):

    """Model to represent an amount claimed against a coverage."""

    claim = models.ForeignKey(Claim)
    coverageType = models.ForeignKey(CoverageType)
    amountClaimed = models.IntegerField(blank=True, default=0)

    def __unicode__(self):
        return "%s - %s - Amount claimed: %s" % (self.claim, self.coverageType,
                                                 self.amountClaimed)


class Prescription(models.Model):

    """Model of a saved prescription file.

    A prescription will have the following fields:
    Client
    Date added
    Prescription image

    Notes:
    Reporting:

    """

    client = models.ForeignKey(Client)
    dateAdded = models.DateTimeField(auto_now_add=True)
    # TODO file field for uploading and saving the prescription, optional for
    #  now

    def __unicode__(self):
        clientName = self.client.firstName + " " + self.client.lastName
        date = self.dateAdded.date().isoformat()
        return "Prescription - %s - %s" % (clientName, date)

    def __str__(self):
        return self.__unicode__()


class Invoice(models.Model):
    PAYMENT_TYPES = (("Assignment", "Assignment"),
                     ("Non-assignment", "Non-assignment"))

    claim = models.ForeignKey(Claim)
    dispensed_by = models.CharField(max_length=128)
    payment_type = models.CharField(max_length=15, choices=PAYMENT_TYPES)
    payment_terms = models.CharField(max_length=256)
    payment_made = models.IntegerField(default=0)

    def balance(self):
        return self.total() - self.payment_made

    def total(self):
        total = 0
        for item in self.item_set.all():
            total += item.total()
        return total

    def __str__(self):
        return self.dispensed_by


class Item(models.Model):
    invoice = models.ForeignKey(Invoice)
    description = models.CharField(max_length=512)
    unit_price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)

    def total(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return self.description


class InsuranceLetter(models.Model):
    claim = models.ForeignKey(Claim)

    practitioner_name = models.CharField(max_length=128)
    diagnosis = models.CharField(max_length=512)
    biomedical_and_gait_analysis_date = models.DateTimeField()
    examiner = models.CharField(max_length=128)
    dispensing_practitioner = models.CharField(max_length=128)
    dispense_date = models.DateTimeField()

    orthopedic_shoes = models.BooleanField(default=False)
    foot_orthotics_orthosis = models.BooleanField(default=False)
    internally_modified_footwear = models.BooleanField(default=False)

    foam_plaster = models.BooleanField(default=False)
    gaitscan = models.BooleanField(default=False)

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

    def __str__(self):
        return self.practitioner_name


class Laboratory(models.Model):
    insurance_letter = models.ForeignKey(InsuranceLetter)
    description = models.CharField(max_length=512)

    def __str__(self):
        return self.description


class ProofOfManufacturing(models.Model):
    claim = models.ForeignKey(Claim)

    laboratory_name = models.CharField(max_length=128)
    laboratory_address = models.CharField(max_length=128)
    laboratory_city = models.CharField(max_length=128)
    laboratory_postal_code = models.CharField(max_length=6)
    laboratory_country = models.CharField(max_length=128)
    laboratory_phone = models.CharField(max_length=14)
    laboratory_fax = models.CharField(max_length=14)

    invoice_date = models.DateTimeField()
    invoice_number = models.IntegerField()

    bill_name = models.CharField(max_length=128)
    bill_address = models.CharField(max_length=128)
    bill_city = models.CharField(max_length=128)
    bill_postal_code = models.CharField(max_length=6)
    bill_country = models.CharField(max_length=128)
    ship_name = models.CharField(max_length=128)
    ship_address = models.CharField(max_length=128)
    ship_city = models.CharField(max_length=128)
    ship_postal_code = models.CharField(max_length=6)
    ship_country = models.CharField(max_length=128)

    patient = models.CharField(max_length=128)
    product = models.CharField(max_length=256)
    quantity = models.IntegerField()

    laboratory_information = models.CharField(max_length=128)
    laboratory_supervisor = models.CharField(max_length=128)
    raw_materials = models.TextField()
    manufacturing = models.TextField()
    casting_technique = models.TextField()
