import datetime

from django.utils import timezone

from django.apps import apps as apps_apps


def get_credit_divisor(created):
    CreditDivisor = apps_apps.get_model('clients.CreditDivisor')

    if isinstance(created, datetime.date):
        # To datetime
        created = datetime.datetime.combine(created, datetime.time.max)
        # To timezone
        created = timezone.make_aware(created)

    credit_divisor = CreditDivisor.objects.filter(
        created__lte=created,
    ).latest('created')

    return credit_divisor.value


def claimcoverage_pre_save(sender, instance, **kwargs):
    # print('claimcoverage_pre_save')

    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:  # created
        if instance.actual_paid_date:
            client = instance.claim.patient.get_client()
            update_credit(
                (
                    instance.expected_back /
                    get_credit_divisor(instance.claim.submitted_datetime)
                ),
                client
            )
    else:  # updated
        if not obj.actual_paid_date and instance.actual_paid_date:
            client = instance.claim.patient.get_client()
            update_credit(
                (
                    instance.expected_back /
                    get_credit_divisor(instance.claim.submitted_datetime)
                ),
                client
            )
        elif obj.actual_paid_date and not instance.actual_paid_date:
            client = instance.claim.patient.get_client()
            update_credit(
                (
                    -instance.expected_back /
                    get_credit_divisor(obj.claim.submitted_datetime)
                ),
                client
            )
        elif obj.actual_paid_date and instance.actual_paid_date:
            if (
                (obj.expected_back != instance.expected_back) or
                (obj.actual_paid_date != instance.actual_paid_date)
                    ):
                client = instance.claim.patient.get_client()
                update_credit(
                    (
                        (instance.expected_back - obj.expected_back) /
                        get_credit_divisor(instance.claim.submitted_datetime)
                    ),
                    client
                )
        # not not do nothing


def claimcoverage_post_delete(sender, instance, **kwargs):
    if instance.actual_paid_date:
        client = instance.claim.patient.get_client()
        update_credit(
            (
                -instance.expected_back /
                get_credit_divisor(instance.claim.submitted_datetime)
            ),
            client
        )


def shoeorder_pre_save(sender, instance, **kwargs):
    try:
        sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:  # created
        update_credit(
            -instance.shoe_attributes.shoe.credit_value,
            instance.claimant.get_client()
        )
    # else:  # updated, do nothing


def coverageorder_and_adjustmentorder_pre_save(sender, instance, **kwargs):
    # ignore coverageorder quantity as credit_value is already the total
    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:  # created
        update_credit(
            -instance.credit_value,
            instance.claimant.get_client()
        )
    else:  # updated
        if obj.credit_value != instance.credit_value:
            update_credit(
                -(instance.credit_value - obj.credit_value),
                instance.claimant.get_client()
            )


def shoeorder_post_delete(sender, instance, **kwargs):
    update_credit(
        instance.shoe_attributes.shoe.credit_value,
        instance.claimant.get_client()
    )


def coverageorder_and_adjustmentorder_post_delete(sender, instance, **kwargs):
    # ignore coverageorder quantity as credit_value is already the total
    update_credit(
        instance.credit_value,
        instance.claimant.get_client()
    )


def referral_pre_save(sender, instance, **kwargs):
    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:  # created
        update_credit(
            instance.credit_value,
            instance.client
        )
    else:  # updated
        if obj.credit_value != instance.credit_value:
            update_credit(
                instance.credit_value - obj.credit_value,
                instance.client
            )


def referral_post_delete(sender, instance, **kwargs):
    update_credit(
        -instance.credit_value,
        instance.client
    )


def shoe_pre_save(sender, instance, **kwargs):
    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:  # created
        pass
    else:  # updated
        if obj.credit_value != instance.credit_value:
            for shoeattributes in instance.shoeattributes_set.all():
                for shoeorder in shoeattributes.shoeorder_set.all():
                    update_credit(
                        -(instance.credit_value - obj.credit_value),
                        shoeorder.claimant.get_client()
                    )


def update_credit(amount, client):
    # print('update_credit')
    # TODO: remove credit() and rename credit2 to credit
    client.credit2 += amount
    client.save()
