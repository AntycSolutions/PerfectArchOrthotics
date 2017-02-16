import datetime

from django.db import models as db_models
from django.utils import timezone

from clients import models as clients_models
from inventory import models as inventory_models

from . import models as reminders_models


# TODO: setup these to use a cron or similar system
"""
    Instead of using a cron like system of creating reminders
    we create the reminders upon viewing the page, not exactly
    the best implmentation but it works
"""


def _find_unpaid_claims(persons=None):
    if persons:
        claims_filter = db_models.Q(claim__patient_id__in=persons)
        patients_filter = db_models.Q(patient_id__in=persons)
    else:
        claims_filter = db_models.Q()
        patients_filter = db_models.Q()

    three_weeks = datetime.timedelta(weeks=3)
    now = timezone.now()
    now_date = timezone.localtime(now).date()
    three_weeks_ago = now - three_weeks

    claims = clients_models.Claim.objects.prefetch_related(
        'unpaidclaimreminder_set',
    ).filter(
        patients_filter,
        claimcoverage__actual_paid_date__isnull=True,
        submitted_datetime__lte=three_weeks_ago
    ).distinct()

    new_unpaid_claims_reminders = []
    for claim in claims:
        if not claim.unpaidclaimreminder_set.exists():
            new_unpaid_claims_reminders.append(
                reminders_models.UnpaidClaimReminder(
                    claim=claim, created=now_date
                )
            )
    # create new unpaid claims reminders
    reminders_models.UnpaidClaimReminder.objects.bulk_create(
        new_unpaid_claims_reminders
    )

    REQUIRED = reminders_models.Reminder.REQUIRED
    COMPLETED = reminders_models.Reminder.COMPLETED

    # update old unpaid claims reminders
    reminders_models.UnpaidClaimReminder.objects.filter(
        claims_filter,
        claim__claimcoverage__actual_paid_date__isnull=True,
        created__lte=timezone.localtime(three_weeks_ago).date()
    ).update(
        follow_up=REQUIRED,
        result='',
        created=now_date
    )

    possibly_paid_claims_reminders = (
        reminders_models.UnpaidClaimReminder.objects.filter(
            claims_filter,
            claim__claimcoverage__actual_paid_date__isnull=False
        ).exclude(
            follow_up__contains=COMPLETED
        ).prefetch_related(
            'claim__claimcoverage_set'
        )
    )
    for possibly_paid_claims_reminder in possibly_paid_claims_reminders:
        is_paid = True
        claimcoverages = (
            possibly_paid_claims_reminder.claim.claimcoverage_set.all()
        )
        for claimcoverage in claimcoverages:
            if claimcoverage.actual_paid_date is None:
                is_paid = False
                break
        if is_paid:
            # complete unpaid claims reminder
            is_required = (
                REQUIRED in possibly_paid_claims_reminder.follow_up
            )
            if is_required:
                possibly_paid_claims_reminder.follow_up.remove(REQUIRED)
            possibly_paid_claims_reminder.follow_up.append(COMPLETED)
            possibly_paid_claims_reminder.save()


def _find_arrived_orders(persons=None):
    if persons:
        orders_filter = db_models.Q(order__claimant_id__in=persons)
        claimants_filter = db_models.Q(claimant_id__in=persons)
    else:
        orders_filter = db_models.Q()
        claimants_filter = db_models.Q()

    one_week = datetime.timedelta(weeks=1)
    now = timezone.now()
    now_date = timezone.localtime(now).date()
    one_week_ago = now - one_week

    orders = inventory_models.CoverageOrder.objects.prefetch_related(
        'orderarrivedreminder_set',
    ).filter(
        claimants_filter,
        order_type=clients_models.Coverage.ORTHOTICS,
        dispensed_date__isnull=True,
        arrived_date__lte=one_week_ago
    )

    new_arrived_orders_reminders = []
    for order in orders:
        if not order.orderarrivedreminder_set.exists():
            new_arrived_orders_reminders.append(
                reminders_models.OrderArrivedReminder(
                    order=order, created=now_date
                )
            )
    # create new arrived order reminders
    reminders_models.OrderArrivedReminder.objects.bulk_create(
        new_arrived_orders_reminders
    )

    REQUIRED = reminders_models.Reminder.REQUIRED
    COMPLETED = reminders_models.Reminder.COMPLETED

    # update old arrived order reminders
    reminders_models.OrderArrivedReminder.objects.filter(
        orders_filter,
        order__dispensed_date__isnull=True,
        created__lte=timezone.localtime(one_week_ago).date()
    ).update(
        follow_up=REQUIRED,
        result='',
        created=now_date
    )

    uncompleted_order_arrived_reminders = (
        reminders_models.OrderArrivedReminder.objects.filter(
            orders_filter,
            order__dispensed_date__isnull=False
        ).exclude(
            follow_up__contains=COMPLETED
        )
    )
    for order_arrived_reminder in uncompleted_order_arrived_reminders:
        # complete arrived order reminder
        is_required = REQUIRED in order_arrived_reminder.follow_up
        if is_required:
            order_arrived_reminder.follow_up.remove(REQUIRED)
        order_arrived_reminder.follow_up.append(COMPLETED)
        order_arrived_reminder.save()


def _find_claims_without_orders(persons=None):
    if persons:
        claims_filter = db_models.Q(claim__patient_id__in=persons)
        patients_filter = db_models.Q(patient_id__in=persons)
    else:
        claims_filter = db_models.Q()
        patients_filter = db_models.Q()

    now = timezone.now()
    now_date = timezone.localtime(now).date()
    one_day_ago = now - datetime.timedelta(days=1)

    ORTHOTICS = clients_models.Coverage.ORTHOTICS
    cutoff = (
        inventory_models.CoverageOrder.ORDERS_TIED_TO_CLAIMS_START_DATETIME
    )
    has_orthotics = (
        db_models.Q(
            coverages__coverage_type=ORTHOTICS
        ) |
        db_models.Q(
            claimcoverage__items__coverage_type=ORTHOTICS
        )
    )
    claims = clients_models.Claim.objects.filter(
        patients_filter,
        has_orthotics,
        coverageorder=None,
        submitted_datetime__lte=one_day_ago,
        submitted_datetime__gte=cutoff
    )

    new_claims_without_orders_reminders = []
    for claim in claims:
        if not claim.claimorderreminder_set.exists():
            new_claims_without_orders_reminders.append(
                reminders_models.ClaimOrderReminder(
                    claim=claim, created=now_date
                )
            )
    # create new claims without orders reminders
    reminders_models.ClaimOrderReminder.objects.bulk_create(
        new_claims_without_orders_reminders
    )

    # delete unneeded claims without orders reminders
    reminders_models.ClaimOrderReminder.objects.filter(
        claims_filter,
        claim__coverageorder__order_type=ORTHOTICS
    ).delete()
