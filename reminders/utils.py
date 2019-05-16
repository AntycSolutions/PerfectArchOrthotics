import datetime

from django.db import models as db_models
from django.utils import timezone

from clients import models as clients_models
from inventory import models as inventory_models

from . import models as reminders_models


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
    DELETED = reminders_models.Reminder.DELETED

    # update old unpaid claims reminders
    reminders_models.UnpaidClaimReminder.objects.filter(
        claims_filter,
        claim__claimcoverage__actual_paid_date__isnull=True,
        created__lte=timezone.localtime(three_weeks_ago).date()
    ).exclude(
        follow_up__contains=DELETED
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

    coverage_types_list = dict(
        inventory_models.CoverageOrder.COVERAGE_TYPES
    ).keys()
    orders = inventory_models.CoverageOrder.objects.prefetch_related(
        'orderarrivedreminder_set',
    ).filter(
        claimants_filter,
        order_type__in=coverage_types_list,
        dispensed_date__isnull=True,
        arrived_date__isnull=False
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
    DELETED = reminders_models.Reminder.DELETED

    # update old arrived order reminders
    reminders_models.OrderArrivedReminder.objects.filter(
        orders_filter,
        order__dispensed_date__isnull=True,
        created__lte=timezone.localtime(one_week_ago).date()
    ).exclude(
        follow_up__contains=DELETED
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


def find_benefits_clients():
    now = timezone.now()
    jan_1 = datetime.datetime(
        year=now.year, month=1, day=1, tzinfo=now.tzinfo
    )
    client_ids = {}

    all_benefit_coverages = (
        clients_models.Coverage.objects.select_related(
            'claimant__client'
        ).prefetch_related(
            'claimcoverage_set__claim'
        ).filter(
            period=clients_models.Coverage.BENEFIT_YEAR,
            period_date__isnull=False
        )
    )
    # TODO in django 2.2+ we can use ExtractFunction to get month/day
    benefit_coverages = []
    for coverage in all_benefit_coverages:
        add = True
        for claimcoverage in coverage.claimcoverage_set.all():
            submitted_datetime = claimcoverage.claim.submitted_datetime
            year = submitted_datetime.year
            month = submitted_datetime.month
            day = submitted_datetime.day
            period_date = coverage.period_date
            if (
                year >= now.year and
                month >= period_date.month and
                day > period_date.day
            ):
                add = False
                break
        if add:
            benefit_coverages.append(coverage)

    calendar_coverages = clients_models.Coverage.objects.select_related(
        'claimant__client'
    ).filter(
        period=clients_models.Coverage.CALENDAR_YEAR
    ).exclude(
        claimcoverage__claim__submitted_datetime__gt=jan_1
    )

    twelve_months_ago = now - datetime.timedelta(days=365)
    twelve_coverages = clients_models.Coverage.objects.select_related(
        'claimant__client'
    ).filter(
        period=clients_models.Coverage.TWELVE_ROLLING_MONTHS
    ).exclude(
        claimcoverage__claim__submitted_datetime__gt=twelve_months_ago
    )

    twenty_four_months_ago = now - datetime.timedelta(days=730)
    twenty_four_coverages = clients_models.Coverage.objects.select_related(
        'claimant__client'
    ).filter(
        period=clients_models.Coverage.TWENTY_FOUR_ROLLING_MONTHS
    ).exclude(
        claimcoverage__claim__submitted_datetime__gt=twenty_four_months_ago
    )

    thirty_six_months_ago = now - datetime.timedelta(days=1095)
    thirty_six_coverages = clients_models.Coverage.objects.select_related(
        'claimant__client'
    ).filter(
        period=clients_models.Coverage.THIRTY_SIX_ROLLING_MONTHS
    ).exclude(
        claimcoverage__claim__submitted_datetime__gt=thirty_six_months_ago
    )

    coverages = benefit_coverages + list(
        calendar_coverages |
        twelve_coverages |
        twenty_four_coverages |
        thirty_six_coverages
    )
    for coverage in coverages:
        client_id = coverage.claimant.get_client().pk
        client_coverage_ids = client_ids.get(client_id, set())
        client_coverage_ids.add(coverage.pk)
        client_ids[client_id] = client_coverage_ids

    reminders = reminders_models.BenefitsReminder.objects.select_related(
        'client'
    ).exclude(
        follow_up__contains=reminders_models.Reminder.DELETED
    )
    six_weeks = datetime.timedelta(weeks=6)
    six_weeks_ago = now.date() - six_weeks
    for reminder in reminders:
        coverage_ids = client_ids.pop(reminder.client.pk, None)
        if coverage_ids is None:
            reminder.follow_up = reminders_models.Reminder.COMPLETED
            reminder.result = ''
            reminder.created = now
            reminder.save()
            reminder.coverages.clear()
            continue

        if reminders_models.Reminder.REQUIRED not in reminder.follow_up:
            if reminder.created <= six_weeks_ago:
                reminder.follow_up = reminders_models.Reminder.REQUIRED
                reminder.result = ''
                reminder.created = now
                reminder.save()
        reminder.coverages.set(coverage_ids)
    for client_id, coverage_ids in client_ids.items():
        reminder = reminders_models.BenefitsReminder.objects.create(
            client_id=client_id,
            created=now.date()
        )
        reminder.coverages.set(coverage_ids)
