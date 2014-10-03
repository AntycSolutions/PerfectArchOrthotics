"""Models for the clients app.

The following tables will be contained within:
- Dependent
- Client
- Insurance
- Claim
- Prescription

"""
from django.db import models


class Dependent(models.Model):

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

    firstName = models.CharField(max_length=128, blank=True, default="")
    lastName = models.CharField(max_length=128, blank=True, default="")
    relationship = models.CharField(max_length=6, choices=RELATIONSHIP_CHOICES, blank=True, default="")
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True, default="")
    birthdate = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return "%s %s" % (self.firstName, self.lastName)

    def __str__(self):
        return self.__unicode__()


class Client(models.Model):

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

    firstName = models.CharField(max_length=128, blank=True, default="")
    lastName = models.CharField(max_length=128, blank=True, default="")
    address = models.CharField(max_length=128, blank=True, default="")
    city = models.CharField(max_length=128, blank=True, default="")
    postalCode = models.CharField(max_length=6, blank=True, default="")
    # TODO Write validators for the phone numbers below
    phoneNumber = models.CharField(max_length=14, blank=True, default="")  # In the form of (780)-937-1514
    cellNumber = models.CharField(max_length=14, blank=True, default="")  # In the form of (780)-937-1514
    # will cover all RFC3696/5321-compliant email addresses
    email = models.EmailField(max_length=254, blank=True, null=True)
    healthcareNumber = models.CharField(max_length=20, blank=True, default="")
    birthdate = models.DateField(blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True, default="")
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

    EX. Dental will have $500 per year, orthotics will have $300 max every three years.

    Modeling:
    Have the total coverage amount, amount remaining and amount claimed. The
    calc for amount remaining should be as easy as taking the total and minus
    the amount claimed. However this may change if they go elsewhere for something
    that is covered elsewhere and then comes back to us. The amount remaining then
    should be dynamic and calculated separately from our numbers. (Have to ask Danny)
    Coverage % may be different for each plan, say some will be 50%, others 100% and
    will obviously drop to 0% once the coverage is used during the roll-over timeframe.

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
    provider = models.CharField(max_length=128, blank=True, default="")
    policyNumber = models.CharField(max_length=128, blank=True, default="")
    contractNumber = models.CharField(max_length=128, blank=True, default="")
    billing = models.CharField(max_length=8, choices=BILLING_CHOICES, blank=True, default="")
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
    coverageType = models.CharField(max_length=21, choices=COVERAGE_TYPE, blank=True, default="")
    coveragePercent = models.IntegerField(blank=True, null=True)
    maxClaimAmount = models.IntegerField(default=0, blank=True)
    totalClaimed = models.IntegerField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    period = models.IntegerField(default=1)

    def __unicode__(self):
        return "%s - Coverage percent: %s" % (self.coverageType, self.coveragePercent)

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

    client = models.ForeignKey(Client, blank=True, null=True)
    # TODO figure out how to get the insurance from the client to calidate this
    # TODO remove this, coveraged the the insurance claim model now
    insurance = models.ForeignKey(Insurance, blank=True, null=True)
    submittedDate = models.DateTimeField(auto_now_add=True)
    invoiceDate = models.DateTimeField(blank=True, null=True)
    paidDate = models.DateTimeField(blank=True, null=True)
    amountClaimed = models.IntegerField(blank=True, default=0)
    # TODO validate based on clients insurance, amount left in coverage and coverage percent
    expectedBack = models.IntegerField(blank=True, default=0)
    paymentType = models.CharField(max_length=6, choices=PAYMENT_CHOICES, blank=True, default="")
    claimType = models.CharField(max_length=21, choices=CLAIM_TYPE, blank=True, default="")

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
        return "%s - %s - Amount claimed: %s" % (self.claim, self.coverageType, self.amountClaimed)


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
    # TODO file field for uploading and saving the prescription, optional for now

    def __unicode__(self):
        clientName = self.client.firstName + " " + self.client.lastName
        date = self.dateAdded.date().isoformat()
        return "Prescription - %s - %s" % (clientName, date)

    def __str__(self):
        return self.__unicode__()
