#!/usr/bin/env python
import os
import datetime
from django.utils import timezone



def populate():
    # Constants for the client model
    MALE = Client.GENDER_CHOICES[0][0]
    FEMALE = Client.GENDER_CHOICES[1][0]
    # Add Clients
    eric = add_client("Eric", "Klinger", "11408 44 ave", "Edmonton", "T6J0Z2", "780 437 1514", datetime.date(1988, 12, 30), MALE)
    chris = add_client("Chris", "Klinger", "11408 44 ave", "Edmonton", "T6J0Z2", "780 937 1077", datetime.date(1991, 6, 14), MALE)
    jay = add_client("Jason", "Mu", "4077 69ave", "Edmonton", "blah", "number", datetime.date(1980, 6, 14), MALE)
    dan = add_client("Danny", "Mu", "13499 70ave", "Edmonton", "blah", "number", datetime.date(1983, 8, 14), MALE)
    cloney = add_client("Cloney", "McStudent", "12345 42 ave", "Providence", "blah", "number", datetime.date(1993, 5, 22), MALE)
    jane = add_client("Jane", "Doe", "2943 69 ave", "Vancouver", "blah", "number", datetime.date(1985, 12, 8), FEMALE)
    john = add_client("John", "Doe", "2943 69 ave", "Vancouver", "blah", "number", datetime.date(1984, 8, 20), MALE)

    # Constants for Dependent model
    SPOUSE = Dependent.RELATIONSHIP_CHOICES[0][0]
    CHILD = Dependent.RELATIONSHIP_CHOICES[1][0]
    # Add Dependants
    kid_one = add_dependent("Kid", "one", CHILD, MALE, datetime.date(1999, 1, 1))
    kid_two = add_dependent("Kid", "two", CHILD, FEMALE, datetime.date(2001, 1, 1))
    wife = add_dependent("Jane", "Doe", SPOUSE, FEMALE, datetime.date(1985, 12, 8))
    eric.dependents.add(kid_one)
    eric.dependents.add(kid_two)
    eric.dependents.add(wife)

    # Add prescriptions
    add_prescription(eric, timezone.now())
    add_prescription(eric, timezone.now())
    add_prescription(chris, timezone.now())
    add_prescription(chris, timezone.now())
    add_prescription(jay, timezone.now())
    add_prescription(jay, timezone.now())
    add_prescription(dan, timezone.now())
    add_prescription(dan, timezone.now())
    add_prescription(cloney, timezone.now())
    add_prescription(jane, timezone.now())
    add_prescription(john, timezone.now())

    # Constants for insurance model
    DIRECT = Insurance.BILLING_CHOICES[0][0]
    INDIRECT = Insurance.BILLING_CHOICES[1][0]
    ORTHOTICS = Insurance.COVERAGE_TYPE[0][0]
    COMPRESSION = Insurance.COVERAGE_TYPE[1][0]
    ORTHO_SHOES = Insurance.COVERAGE_TYPE[2][0]
    # Add insurance
    eric_insurance = add_insurance(eric, "Some_provider", ORTHOTICS, "PN9999", "CN9999", 50, DIRECT)
    chris_insurance = add_insurance(chris, "Some_provider", ORTHOTICS, "PN9998", "CN9998", 50, DIRECT)
    jay_insurance = add_insurance(jay, "Some_provider", ORTHOTICS, "PN9997", "CN9997", 50, DIRECT)
    dan_insurance = add_insurance(dan, "Some_provider", ORTHOTICS, "PN9996", "CN9996", 50, DIRECT)
    cloney_insurance = add_insurance(cloney, "Some_provider", ORTHOTICS, "PN9995", "CN9995", 50, DIRECT)
    jane_insurance = add_insurance(jane, "Some_provider", ORTHOTICS, "PN9994", "CN9994", 50, DIRECT)
    john_insurance = add_insurance(john, "Some_provider", ORTHOTICS, "PN9994", "CN9994", 50, DIRECT)

    # Constants for claim model
    CASH = Claim.PAYMENT_CHOICES[0][0]
    # Add claims
    add_claim(eric, eric_insurance, timezone.now(), CASH)
    add_claim(chris, chris_insurance, timezone.now(), CASH)
    add_claim(jay, jay_insurance, timezone.now(), CASH)
    add_claim(dan, dan_insurance, timezone.now(), CASH)
    add_claim(cloney, cloney_insurance, timezone.now(), CASH)
    add_claim(jane, jane_insurance, timezone.now(), CASH)
    add_claim(john, john_insurance, timezone.now(), CASH)

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


def add_client(firstName, lastName, address, city, postalCode, phoneNumber, birthdate, gender):
    c = Client.objects.get_or_create(firstName=firstName,
                                     lastName=lastName,
                                     address=address,
                                     city=city,
                                     postalCode=postalCode,
                                     phoneNumber=phoneNumber,
                                     birthdate=birthdate,
                                     gender=gender)
    return c[0]


def add_dependent(firstName, lastName, relationship, gender, birthdate):
    d = Dependent.objects.get_or_create(firstName=firstName,
                                        lastName=lastName,
                                        relationship=relationship,
                                        gender=gender,
                                        birthdate=birthdate)
    return d[0]


def add_prescription(client, dateAdded):
    p = Prescription.objects.get_or_create(client=client,
                                           dateAdded=dateAdded)
    return p[0]


def add_insurance(client, provider, coverageType, policyNumber, contractNumber, coveragePercent,
                  billing):
    i = Insurance.objects.get_or_create(client=client,
                                        provider=provider,
                                        coverageType=coverageType,
                                        policyNumber=policyNumber,
                                        contractNumber=contractNumber,
                                        coveragePercent=coveragePercent,
                                        billing=billing)
    return i[0]


def add_claim(client, insurance, submittedDate, paymentType):
    c = Claim.objects.get_or_create(client=client,
                                    insurance=insurance,
                                    submittedDate=submittedDate,
                                    paymentType=paymentType)
    return c[0]


# Start execution here!
if __name__ == '__main__':
    print "Starting database population script"
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    # from app.models import <model>, <model>
    from django.contrib.auth.models import User
    import django.contrib.auth.hashers as hashers
    from clients.models import Client, Prescription, Insurance, Claim, Dependent
    populate()
    print "Done populating database"
