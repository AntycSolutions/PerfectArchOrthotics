from django.db import models
from django.utils import safestring, timezone
from django.template import defaultfilters
from django.core import exceptions, urlresolvers

import multiselectfield
from utils import model_utils
from auditlog.registry import auditlog

from clients import models as clients_models
from inventory import models as inventory_models


class Reminder(models.Model, model_utils.FieldList):
    REQUIRED = 'r'
    TEXT = 't'
    EMAIL = 'e'
    CALL = 'c'
    COMPLETED = 'o'
    DELETED = 'd'
    FOLLOW_UP_TYPES = (
        (REQUIRED, 'Required'),
        (TEXT, 'Text'),
        (EMAIL, 'Email'),
        (CALL, 'Call'),
        (COMPLETED, 'Completed'),
        (DELETED, 'Deleted'),
    )
    follow_up = multiselectfield.MultiSelectField(
        choices=FOLLOW_UP_TYPES, default=REQUIRED
    )

    NO_ANSWER = 'n'
    VOICEMAIL = 'v'
    RESULTS = (
        (NO_ANSWER, 'No answer'),
        (VOICEMAIL, 'Voicemail'),
    )
    result = models.CharField(
        max_length=1, choices=RESULTS, blank=True
    )

    created = models.DateField()

    class Meta:
        abstract = True

    def get_all_fields(self):
        fields = super().get_all_fields()

        fields.pop('id')  # hide detail/update/delete in generic template

        modal_btn_pseudo = model_utils.FieldList.PseudoBtn('Update')
        modal_btn_pseudo.type = 'modal'
        modal_btn = self.Field(modal_btn_pseudo, '')
        fields.update({'modal_btn': modal_btn})
        fields.move_to_end('modal_btn', last=False)

        new_value = fields['follow_up'].value.replace(' ', '<br />')
        follow_up_pseudo = model_utils.FieldList.PseudoField('Follow up')
        follow_up = self.Field(
            follow_up_pseudo, safestring.mark_safe(new_value)
        )
        fields.update({'follow_up': follow_up})

        return fields


class OrderArrivedReminder(Reminder):
    order = models.ForeignKey(inventory_models.CoverageOrder)

    # FOLLOWED_UP = 'fu'
    # NEW = 'ne'
    # STATUSES = (
    #     (FOLLOWED_UP, 'Followed up'),
    #     (NEW, 'New'),
    # )
    # status = models.CharField(
    #     max_length=2, choices=STATUSES, blank=True
    # )

    def clean(self):
        order = self.order

        sending_text = Reminder.TEXT in self.follow_up
        sending_email = Reminder.EMAIL in self.follow_up

        client = order.claimant.get_client()
        if sending_email and not client.email:
            raise exceptions.ValidationError({
                'follow_up':
                    'The client does not have an email address',
            })

        if sending_text and not client.phone_number and not client.cell_number:
            raise exceptions.ValidationError({
                'follow_up':
                    'The client does not have a phone number nor '
                    'a cell number',
            })

    def get_all_fields(self):
        fields = super().get_all_fields()

        claimant = self.Field(
            model_utils.FieldList.PseudoForeignKey("Claimant"),
            self.order.claimant
        )
        fields.update({"claimant": claimant})

        def get_str():
            arrived_date = defaultfilters.date(self.order.arrived_date)

            return "{}".format(arrived_date)
        fields['order'].value.get_str = get_str

        client = self.order.claimant.get_client()
        phone_number = client.phone_number
        cell_number = client.cell_number
        if phone_number:
            phone_number = 'Phone: {}<br />'.format(phone_number)
        if cell_number:
            cell_number = 'Cell: {}'.format(cell_number)
        number = self.Field(
            model_utils.FieldList.PseudoField("number"),
            safestring.mark_safe(
                '{}{}'.format(phone_number, cell_number)
            )
        )
        fields.update({"number": number})

        modal_btn = fields['modal_btn']
        logs = ''
        for log in self.orderarrivedmessagelog_set.all():
            if logs:
                logs += ','
            created = defaultfilters.date(
                timezone.localtime(log.created), "N j, Y, P"
            )
            logs += '{{"type":"{}","created":"{}"}}'.format(
                log.get_msg_type_display(), created
            )
        modal_btn.field.attrs = {
            'data-logs': '[{}]'.format(logs)
        }

        return fields


class UnpaidClaimReminder(Reminder):
    claim = models.ForeignKey(clients_models.Claim)

    # PAID = 'pa'
    # NOT_PAID = 'np'
    # FOLLOWED_UP = 'fu'
    # NEW = 'ne'
    # STATUSES = (
    #     (PAID, 'Paid'),
    #     (NOT_PAID, 'Not paid'),
    #     (FOLLOWED_UP, 'Followed up'),
    #     (NEW, 'New'),
    # )
    # status = models.CharField(
    #     max_length=2, choices=STATUSES, blank=True
    # )

    def clean(self):
        claim = self.claim

        # remove is_ASSIGNMENT check as Claims can have both benefits
        # is_ASSIGNMENT = (
        #     claim.insurance.benefits ==
        #     clients_models.Insurance.ASSIGNMENT
        # )
        sending_text = Reminder.TEXT in self.follow_up
        sending_email = Reminder.EMAIL in self.follow_up
        # following_up = sending_text or sending_email
        # if is_ASSIGNMENT and following_up:
        #     raise exceptions.ValidationError({
        #         'follow_up':
        #             'You cannot send a text or email to Assignment Benefits',
        #     })

        client = claim.patient.get_client()
        if sending_email and not client.email:
            raise exceptions.ValidationError({
                'follow_up':
                    'The client does not have an email address',
            })

        if sending_text and not client.phone_number and not client.cell_number:
            raise exceptions.ValidationError({
                'follow_up':
                    'The client does not have a phone number nor '
                    'a cell number',
            })

    def get_all_fields(self):
        fields = super().get_all_fields()

        patient = self.Field(
            model_utils.FieldList.PseudoForeignKey("Patient"),
            self.claim.patient
        )
        fields.update({"patient": patient})

        def get_str():
            submitted_datetime = timezone.localtime(
                self.claim.submitted_datetime
            )
            submitted_datetime = defaultfilters.date(
                submitted_datetime, "N j, Y, P"
            )

            return "{}".format(submitted_datetime)
        fields['claim'].value.get_str = get_str

        expected_back = self.Field(
            model_utils.FieldList.PseudoField("Expected back"),
            '${}'.format(self.claim.total_expected_back())
        )
        fields.update({"expected_back": expected_back})

        amount_claimed = self.Field(
            model_utils.FieldList.PseudoField("Amount claimed"),
            '${}'.format(
                self.claim.total_amount_quantity_claimed().total_amount_claimed
            )
        )
        fields.update({"amount_claimed": amount_claimed})

        client = self.claim.patient.get_client()
        phone_number = client.phone_number
        cell_number = client.cell_number
        if phone_number:
            phone_number = 'Phone: {}<br />'.format(phone_number)
        if cell_number:
            cell_number = 'Cell: {}'.format(cell_number)
        number = self.Field(
            model_utils.FieldList.PseudoField("number"),
            safestring.mark_safe(
                '{}{}'.format(phone_number, cell_number)
            )
        )
        fields.update({"number": number})

        modal_btn = fields['modal_btn']
        logs = ''
        for log in self.unpaidclaimmessagelog_set.all():
            if logs:
                logs += ','
            created = defaultfilters.date(
                timezone.localtime(log.created), "N j, Y, P"
            )
            logs += '{{"type":"{}","created":"{}"}}'.format(
                log.get_msg_type_display(), created
            )
        modal_btn.field.attrs = {
            'data-logs': '[{}]'.format(logs)
        }

        return fields


class ClaimOrderReminder(models.Model, model_utils.FieldList):
    created = models.DateField()

    claim = models.ForeignKey(clients_models.Claim)

    def get_all_fields(self):
        fields = super().get_all_fields()

        fields.pop('id')  # hide detail/update/delete in generic template

        btn_pseudo = model_utils.FieldList.PseudoBtn(
            'Create Orthotics Order'
        )
        btn_pseudo.attrs = {
            'onclick':
                "location.href='{}'".format(
                    urlresolvers.reverse(
                        'coverage_order_claim_create',
                        kwargs={
                            'claim_pk': self.claim_id,
                            'person_pk': self.claim.patient_id
                        }
                    )
                )
        }
        btn = self.Field(btn_pseudo, '')
        fields.update({'btn': btn})
        fields.move_to_end('btn', last=False)

        patient = self.Field(
            model_utils.FieldList.PseudoForeignKey("Patient"),
            self.claim.patient
        )
        fields.update({"patient": patient})

        def get_str():
            submitted_datetime = timezone.localtime(
                self.claim.submitted_datetime
            )
            submitted_datetime = defaultfilters.date(
                submitted_datetime, "N j, Y, P"
            )

            return "{}".format(submitted_datetime)
        fields['claim'].value.get_str = get_str

        return fields


class MessageLog(models.Model):
    TEXT = 't'
    EMAIL = 'e'
    CALL = 'c'
    MSG_TYPES = (
        (TEXT, 'Text'),
        (EMAIL, 'Email'),
        (CALL, 'Call'),
    )
    msg_type = models.CharField(max_length=1, choices=MSG_TYPES)

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class OrderArrivedMessageLog(MessageLog):
    order_arrived_reminder = models.ForeignKey(
        OrderArrivedReminder, on_delete=models.SET_NULL,
        null=True
    )


class UnpaidClaimMessageLog(MessageLog):
    unpaid_claim_reminder = models.ForeignKey(
        UnpaidClaimReminder, on_delete=models.SET_NULL,
        null=True
    )


auditlog.register(OrderArrivedReminder)
auditlog.register(UnpaidClaimReminder)
auditlog.register(ClaimOrderReminder)
