import os
import datetime
from django.utils import timezone


def populate():
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
    DIRECT = Insurance.DIRECT
    INDIRECT = Insurance.INDIRECT
    # Add Insurances
    # Commening out for now, looks like we are changing the way we do this
    eric_insurance = add_insurance(eric, "Some_provider",
                                   "PN9999", "CN9999", DIRECT)
    chris_insurance = add_insurance(chris, "Some_provider",
                                    "PN9998", "CN9998", DIRECT)
    jay_insurance = add_insurance(jay, "Some_provider",
                                  "PN9997", "CN9997", DIRECT)
    dan_insurance = add_insurance(dan, "Some_provider",
                                  "PN9996", "CN9996", DIRECT)
    cloney_insurance = add_insurance(cloney, "Some_provider",
                                     "PN9995", "CN9995", DIRECT)
    jane_insurance = add_insurance(jane, "Some_provider",
                                   "PN9994", "CN9994", DIRECT)
    john_insurance = add_insurance(john, "Some_provider",
                                   "PN9994", "CN9994", INDIRECT)

    # Constants for coverage types model
    ORTHOTICS = CoverageType.ORTHOTICS
    COMPRESSION = CoverageType.COMPRESSION_STOCKINGS
    ORTHO_SHOES = CoverageType.ORTHOPEDIC_SHOES
    # Add CoverageTypes
    eric_coverage_type = add_coverage_type(eric_insurance, ORTHOTICS,
                                           100, 250)
    chris_coverage_type = add_coverage_type(chris_insurance, COMPRESSION,
                                            100, 300)
    jay_coverage_type = add_coverage_type(jay_insurance, ORTHO_SHOES,
                                          100, 350)
    dan_coverage_type = add_coverage_type(dan_insurance, ORTHO_SHOES,
                                          100, 350)
    cloney_coverage_type = add_coverage_type(cloney_insurance, ORTHO_SHOES,
                                             100, 350)
    jane_coverage_type = add_coverage_type(jane_insurance, ORTHO_SHOES,
                                           100, 350)
    john_coverage_type = add_coverage_type(john_insurance, ORTHO_SHOES,
                                           100, 350)

    # Constants for claim model
    CASH = Claim.CASH
    # Add Claims
    eric_claim = add_claim(eric, timezone.now(), CASH)
    chris_claim = add_claim(chris, timezone.now(), CASH)
    jay_claim = add_claim(jay, timezone.now(), CASH)
    dan_claim = add_claim(dan, timezone.now(), CASH)
    cloney_claim = add_claim(cloney, timezone.now(), CASH)
    jane_claim = add_claim(jane, timezone.now(), CASH)
    john_claim = add_claim(john, timezone.now(), CASH)

    eric_claim.coverage_types.add(eric_coverage_type)
    chris_claim.coverage_types.add(chris_coverage_type)
    jay_claim.coverage_types.add(jay_coverage_type)
    dan_claim.coverage_types.add(dan_coverage_type)
    cloney_claim.coverage_types.add(cloney_coverage_type)
    jane_claim.coverage_types.add(jane_coverage_type)
    john_claim.coverage_types.add(john_coverage_type)

    # Add admin users
    # Have to hash passwords so get_or_create will work
    password = hashers.make_password("admin")
    add_admin("admin", password)
    add_admin("jay", password)
    add_admin("dan", password)
    add_admin("eric", password)
    add_admin("chris", password)


def add_admin(username, password):
    # Need to try and return here since django admin users are dumb
    try:
        a = User.objects.get_or_create(username=username,
                                       password=password,
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


def add_insurance(client, provider, policyNumber, contractNumber, billing):
    i = Insurance.objects.get_or_create(client=client,
                                        provider=provider,
                                        policy_number=policyNumber,
                                        contract_number=contractNumber,
                                        billing=billing)
    return i[0]


def add_coverage_type(insurance, coverage_type, coverage_percent,
                      max_claim_amount):
    c = CoverageType.objects.get_or_create(insurance=insurance,
                                           coverage_type=coverage_type,
                                           coverage_percent=coverage_percent,
                                           max_claim_amount=max_claim_amount)
    return c[0]


def add_claim(client, submittedDate, paymentType):
    c = Claim.objects.get_or_create(client=client,
                                    submitted_date=submittedDate,
                                    payment_type=paymentType)
    return c[0]


if __name__ == '__main__':
    print("Starting PerfectArchOrthotics database population script...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          'perfect_arch_orthotics.settings')
    import django
    django.setup()
    from django.contrib.auth.models import User
    import django.contrib.auth.hashers as hashers
    from clients.models import Client, Insurance, Claim, \
        Dependent, CoverageType
    populate()
    print("Finished PerfectArchOrthotics database population script.")
