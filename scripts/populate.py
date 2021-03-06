import os
import datetime
import time

from django.utils import timezone

# TODO: this is out of date, but do we really need it?


def populate():
    clients()
    inventory()


def clients():
    # Constants for the client model
    MALE = Client.MALE
    FEMALE = Client.FEMALE
    # Add Clients
    eric = add_client("Eric", "Klinger", "11408 44 ave",
                      "Edmonton", "T6J0Z2", "780 437 1514",
                      datetime.date(1988, 12, 30), MALE)
    chris = add_client("Chris", "Klinger", "11408 44 ave",
                       "Edmonton", "T6J0Z2", "780 937 1077",
                       datetime.date(1991, 6, 14), MALE)
    jay = add_client("Jason", "Mu", "4077 69ave",
                     "Edmonton", "blah", "number",
                     datetime.date(1980, 6, 14), MALE)
    dan = add_client("Danny", "Mu", "13499 70ave",
                     "Edmonton", "blah", "number",
                     datetime.date(1983, 8, 14), MALE)
    cloney = add_client("Cloney", "McStudent", "12345 42 ave",
                        "Providence", "blah", "number",
                        datetime.date(1993, 5, 22), MALE)
    jane = add_client("Jane", "Doe", "2943 69 ave",
                      "Vancouver", "blah", "number",
                      datetime.date(1985, 12, 8), FEMALE)
    john = add_client("John", "Doe", "2943 69 ave",
                      "Vancouver", "blah", "number",
                      datetime.date(1984, 8, 20), MALE)

    # Constants for Dependent model
    SPOUSE = Dependent.SPOUSE
    CHILD = Dependent.CHILD
    # Add Dependents
    kid_one = add_dependent(eric, "Kid", "one", CHILD, MALE,
                            datetime.date(1999, 1, 1))
    kid_two = add_dependent(eric, "Kid", "two", CHILD, FEMALE,
                            datetime.date(2001, 1, 1))
    wife = add_dependent(eric, "Jane", "Doe", SPOUSE, FEMALE,
                         datetime.date(1985, 12, 8))

    # Constants for insurance model
    ASSIGNMENT = Insurance.ASSIGNMENT
    NON_ASSIGNMENT = Insurance.NON_ASSIGNMENT
    # Add Insurances
    # Commening out for now, looks like we are changing the way we do this
    eric_insurance = add_insurance(eric, "Some_provider",
                                   "PN9999", "CN9999", ASSIGNMENT)
    chris_insurance = add_insurance(chris, "Some_provider",
                                    "PN9998", "CN9998", ASSIGNMENT)
    jay_insurance = add_insurance(jay, "Some_provider",
                                  "PN9997", "CN9997", ASSIGNMENT)
    dan_insurance = add_insurance(dan, "Some_provider",
                                  "PN9996", "CN9996", ASSIGNMENT)
    cloney_insurance = add_insurance(cloney, "Some_provider",
                                     "PN9995", "CN9995", ASSIGNMENT)
    jane_insurance = add_insurance(jane, "Some_provider",
                                   "PN9994", "CN9994", ASSIGNMENT)
    john_insurance = add_insurance(john, "Some_provider",
                                   "PN9994", "CN9994", NON_ASSIGNMENT)

    # Constants for coverage types model
    ORTHOTICS = Coverage.ORTHOTICS
    COMPRESSION = Coverage.COMPRESSION_STOCKINGS
    ORTHO_SHOES = Coverage.ORTHOPEDIC_SHOES
    # Add Coverages
    eric_coverage = add_coverage(
        eric_insurance, ORTHOTICS, 100, 250, eric)
    chris_coverage = add_coverage(
        chris_insurance, COMPRESSION, 100, 300, chris)
    jay_coverage = add_coverage(
        jay_insurance, ORTHO_SHOES, 100, 350, jay)
    dan_coverage = add_coverage(
        dan_insurance, ORTHO_SHOES, 100, 350, dan)
    cloney_coverage = add_coverage(
        cloney_insurance, ORTHO_SHOES, 100, 350, cloney)
    jane_coverage = add_coverage(
        jane_insurance, ORTHO_SHOES, 100, 350, jane)
    john_coverage = add_coverage(
        john_insurance, ORTHO_SHOES, 100, 350, john)

    # Add Claims
    tz = timezone.get_current_timezone()
    eric_claim = add_claim(eric, eric_insurance, eric,
                           timezone.make_aware(datetime.datetime.now(), tz))
    time.sleep(0.01)
    chris_claim = add_claim(chris, chris_insurance, chris,
                            timezone.make_aware(datetime.datetime.now(), tz))
    time.sleep(0.01)
    jay_claim = add_claim(jay, jay_insurance, jay,
                          timezone.make_aware(datetime.datetime.now(), tz))
    time.sleep(0.01)
    dan_claim = add_claim(dan, dan_insurance, dan,
                          timezone.make_aware(datetime.datetime.now(), tz))
    time.sleep(0.01)
    cloney_claim = add_claim(cloney, cloney_insurance, cloney,
                             timezone.make_aware(datetime.datetime.now(), tz))
    time.sleep(0.01)
    jane_claim = add_claim(jane, jane_insurance, jane,
                           timezone.make_aware(datetime.datetime.now(), tz))
    time.sleep(0.01)
    john_claim = add_claim(john, john_insurance, john,
                           timezone.make_aware(datetime.datetime.now(), tz))

    ClaimCoverage.objects.create(
        claim=eric_claim, coverage=eric_coverage)
    ClaimCoverage.objects.create(
        claim=chris_claim, coverage=chris_coverage)
    ClaimCoverage.objects.create(
        claim=jay_claim, coverage=jay_coverage)
    ClaimCoverage.objects.create(
        claim=dan_claim, coverage=dan_coverage)
    ClaimCoverage.objects.create(
        claim=cloney_claim, coverage=cloney_coverage)
    ClaimCoverage.objects.create(
        claim=jane_claim, coverage=jane_coverage)
    ClaimCoverage.objects.create(
        claim=john_claim, coverage=john_coverage)

    # Add admin users
    # Have to hash passwords so get_or_create will work
    password = hashers.make_password("admin")
    add_admin("admin", password, "Admin")
    add_admin("jay", password, "Jay")
    add_admin("dan", password, "Dan")
    add_admin("eric", password, "Eric")
    add_admin("chris", password, "Chris")

    add_admin("airith", hashers.make_password("perfectarch"), "Andrew")


def inventory():
    # Constants for Shoe
    WOMENS = Shoe.WOMENS
    ORDERABLE = Shoe.ORDERABLE
    # Add Shoes
    s1 = add_shoe(
        "Test Shoe", category=WOMENS, availability=ORDERABLE, style="Toe Shoe")
    sa1 = add_shoe_attributes(
        s1, "1", 1)


def add_admin(username, password, first_name):
    # Need to try and return here since django admin users are dumb
    try:
        a = User.objects.get_or_create(username=username,
                                       password=password,
                                       first_name=first_name,
                                       is_staff=True,
                                       is_superuser=True)
        return a[0]
    except:
        return


def add_client(firstName, lastName, address, city,
               postalCode, phoneNumber, birthdate, gender):
    c = Client.objects.get_or_create(first_name=firstName,
                                     last_name=lastName,
                                     address=address,
                                     city=city,
                                     postal_code=postalCode,
                                     phone_number=phoneNumber,
                                     birth_date=birthdate,
                                     gender=gender)
    return c[0]


def add_dependent(client, firstName, lastName,
                  relationship, gender, birthdate):
    d = Dependent.objects.get_or_create(client=client,
                                        first_name=firstName,
                                        last_name=lastName,
                                        relationship=relationship,
                                        gender=gender,
                                        birth_date=birthdate)
    return d[0]


def add_insurance(main_claimant, provider, policyNumber, contractNumber,
                  benefits):
    i = Insurance.objects.get_or_create(main_claimant=main_claimant,
                                        provider=provider,
                                        policy_number=policyNumber,
                                        contract_number=contractNumber,
                                        benefits=benefits)
    return i[0]


def add_coverage(insurance, coverage_type, coverage_percent,
                 max_claim_amount, claimant):
    c = Coverage.objects.get_or_create(insurance=insurance,
                                       coverage_type=coverage_type,
                                       coverage_percent=coverage_percent,
                                       max_claim_amount=max_claim_amount,
                                       claimant=claimant)
    return c[0]


def add_claim(client, insurance, patient, submitted_datetime):
    c = Claim.objects.get_or_create(insurance=insurance,
                                    patient=patient,
                                    submitted_datetime=submitted_datetime)
    return c[0]


def add_shoe(name, image=None, category="", size="", availability="",
             brand="", style="", sku="", colour="", description="",
             credit_value=0, quantity=0, cost=0):
    s = Shoe.objects.get_or_create(
        image=image, category=category, availability=availability,
        brand=brand, style=style, name=name, sku=sku, colour=colour,
        description=description, credit_value=credit_value,
        cost=cost)
    return s[0]


def add_shoe_attributes(shoe, size, quantity=0):
    sa = ShoeAttributes.objects.get_or_create(
        shoe=shoe, size=size, quantity=quantity)
    return sa[0]


if __name__ == '__main__':
    print("Starting PerfectArchOrthotics database population script...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'perfect_arch_orthotics.settings')
    import django
    django.setup()
    from django.contrib.auth.models import User
    import django.contrib.auth.hashers as hashers
    from clients.models import Client, Insurance, Claim, \
        Dependent, Coverage, ClaimCoverage
    from inventory.models import Shoe, ShoeAttributes
    populate()
    print("Finished PerfectArchOrthotics database population script.")
