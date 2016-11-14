import datetime
import collections
import smtplib

from django.views import generic
from django.utils import timezone
from django.core import urlresolvers, mail
from django.conf import settings
from django.template import defaultfilters
from django.db import models as db_models

import twilio
from django_twilio import client as django_twilio_client
from utils import views_utils

from clients import models as clients_models
from inventory import models as inventory_models
from . import models as reminders_models, forms


class Reminders(generic.TemplateView):
    template_name = "reminders/reminders.html"

    def _find_unpaid_claims(self):
        three_weeks = datetime.timedelta(weeks=3)
        three_weeks_ago = timezone.now() - three_weeks

        claims = clients_models.Claim.objects.prefetch_related(
            'claimreminder_set',
        ).filter(
            claimcoverage__actual_paid_date__isnull=True,
            submitted_datetime__lte=three_weeks_ago,
        ).distinct()

        unpaid_claims_reminders = []
        for claim in claims:
            if not claim.claimreminder_set.exists():
                created = claim.submitted_datetime.date() - three_weeks
                unpaid_claims_reminders.append(
                    reminders_models.ClaimReminder(
                        claim=claim, created=created
                    )
                )
        reminders_models.ClaimReminder.objects.bulk_create(
            unpaid_claims_reminders
        )

    def _find_arrived_orders(self):
        one_week = datetime.timedelta(weeks=1)
        one_week_ago = timezone.now() - one_week

        orders = inventory_models.CoverageOrder.objects.prefetch_related(
            'orderreminder_set',
        ).filter(
            order_type=clients_models.Coverage.ORTHOTICS,
            dispensed_date__isnull=True,
            arrived_date__lte=one_week_ago,
        )

        arrived_orders_reminders = []
        for order in orders:
            if not order.orderreminder_set.exists():
                created = order.arrived_date - one_week
                arrived_orders_reminders.append(
                    reminders_models.OrderReminder(
                        order=order, created=created
                    )
                )
        reminders_models.OrderReminder.objects.bulk_create(
            arrived_orders_reminders
        )

    def _find_claims_without_orders(self):
        one_day_ago = timezone.now() - datetime.timedelta(days=1)

        claims = clients_models.Claim.objects.filter(
            # add filter for missing orders
            submitted_datetime__lte=one_day_ago,
        )

        # bulk_create new claim reminder
        for claim in claims:
            pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        Option = collections.namedtuple(
            'Option', ['value', 'value_display', 'selected']
        )
        Select = collections.namedtuple('Select', ['label', 'options'])
        follow_up_types = []
        GET = self.request.GET.copy()
        no_value = (
            ('follow_up_type' not in GET) or
            (not GET.getlist('follow_up_type'))
        )
        if no_value:
            GET.setlist('follow_up_type', [reminders_models.Reminder.REQUIRED])
        follow_up_type_list = GET.getlist('follow_up_type')
        for follow_up_type in reminders_models.Reminder.FOLLOW_UP_TYPES:
            if (follow_up_type[0] in follow_up_type_list):
                follow_up_types.append(
                    Option(follow_up_type[0], follow_up_type[1], True)
                )
            else:
                follow_up_types.append(
                    Option(follow_up_type[0], follow_up_type[1], False)
                )
        selects = collections.OrderedDict()
        selects.update(
            {"follow_up_type": Select("Follow up type", follow_up_types)}
        )
        context['selects'] = selects

        """
            Instead of using a cron like system of creating reminders
            we create the reminders upon viewing the page, not exactly
            the best implmentation but it works
        """

        follow_up_filter = db_models.Q()
        for follow_up in follow_up_type_list:
            follow_up_filter &= db_models.Q(follow_up__contains=follow_up)

        self._find_unpaid_claims()
        unpaid_claims_reminders = (
            reminders_models.ClaimReminder.objects.select_related(
                'claim__patient__client',
                'claim__patient__dependent',
                'claim__insurance__main_claimant__client',
                'claim__insurance__main_claimant__dependent',
            ).prefetch_related(
                'claim__claimcoverage_set__claimitem_set__item__'
                'itemhistory_set',
            ).filter(follow_up_filter)
        )
        context['unpaid_claims_reminders'] = unpaid_claims_reminders

        self._find_arrived_orders()
        arrived_orders_reminders = (
            reminders_models.OrderReminder.objects.select_related(
                'order__claimant__client',
                'order__claimant__dependent',
            ).filter(follow_up_filter)
        )
        context['arrived_orders_reminders'] = arrived_orders_reminders

        # self._find_claims_without_orders()
        # claims_without_orders_reminders = (
        #     reminders_models.ClaimReminder.objects.all()
        # )
        # context['claims_without_orders_reminders'] = (
        #     claims_without_orders_reminders
        # )

        context['claim_reminder_form'] = forms.ClaimReminderForm(
            prefix="claimreminder"
        )
        context['order_reminder_form'] = forms.OrderReminderForm(
            prefix="orderreminder"
        )

        return context


# send_email expects body to end in two newlines: \n\n
def send_email(client, subject, body, user=None):
    if settings.ENV != 'prod':
        body += settings.ENV
        if user:
            body += ' - {}'.format(user)
        body += '\n\n'

    try:
        mail.send_mail(subject, body, '', [client.email])
    except smtplib.SMTPRecipientsRefused:
        return (
            'Could not send email to \'{email}\''.format(
                email=client.email
            )
        )

    return ''


def send_reminder_email(
    reminder, client, old_follow_up, subject, body, user=None
):
    EMAIL = reminders_models.Reminder.EMAIL
    sending_email = (
        EMAIL in reminder.follow_up and EMAIL not in old_follow_up
    )
    error = ''
    if sending_email:
        error = send_email(client, subject, body, user=user)

    return error


def send_text_message(client, body, user=None):
    if settings.ENV != 'prod':
        body += '\n' + settings.ENV
        if user:
            body += ' - {}'.format(user)

    number = None
    if client.cell_number:
        number = client.cell_number
    elif client.phone_number:
        number = client.phone_number

    try:
        django_twilio_client.twilio_client.messages.create(
            to='+1{}'.format(number),
            from_=settings.DEFAULT_FROM_NUMBER,
            body=body
        )
    except twilio.TwilioRestException as e:
        return (
            'Could not send text message to'
            ' \'{number}\'\\n\\nError: {msg}'.format(
                number=number,
                msg=e.msg
            )
        )

    return ''


def send_reminder_text_message(
    reminder, client, old_follow_up, body, user=None
):
    TEXT = reminders_models.Reminder.TEXT
    sending_text = (
        TEXT in reminder.follow_up and TEXT not in old_follow_up
    )
    error = ''
    if sending_text:
        error = send_text_message(client, body, user=user)

    return error


class ClaimReminderUpdate(views_utils.AjaxResponseMixin, generic.UpdateView):
    template_name = 'reminders/reminders.html'
    model = reminders_models.ClaimReminder
    form_class = forms.ClaimReminderForm
    success_url = urlresolvers.reverse_lazy('reminders:reminders')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # store old folllow_up so we can compare later
        self.old_follow_up = self.object.follow_up

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)

        claim = self.object.claim
        patient = claim.patient
        client = patient.get_client()
        error = ''

        subject = 'Payment Reminder'
        body = (
            'Hi {patient},\n'
            '\n'
            'This is a payment reminder for your Claim '
            'submitted on {submitted}\n'
            '\n'
            'Regards,\n'
            '\n'
            '-Perfect Arch Team\n'
            '\n'
            '{address}\n'
            '\n'.format(
                patient=patient,
                submitted=defaultfilters.date(
                    claim.submitted_datetime, "N j, Y, P"
                ),
                address=settings.BILL_TO[0][1],
            )
        )
        error += send_reminder_email(
            self.object,
            client,
            self.old_follow_up,
            subject,
            body,
            user=self.request.user
        )

        if error:
            error += '\\n\\n'

        body = (
            'Hi {patient}, this is a payment reminder for your '
            'Claim submitted on {submitted}'.format(
                patient=patient,
                submitted=defaultfilters.date(
                    claim.submitted_datetime, "N j, Y, P"
                ),
            )
        )
        error += send_reminder_text_message(
            self.object,
            client,
            self.old_follow_up,
            body,
            user=self.request.user
        )

        if error:
            response.content = response.content.replace(
                b'}', ', "error": "{}"}}'.format(error).encode()
            )
            response.status_code = 400

        return response


class OrderReminderUpdate(views_utils.AjaxResponseMixin, generic.UpdateView):
    template_name = 'reminders/reminders.html'
    model = reminders_models.OrderReminder
    form_class = forms.OrderReminderForm
    success_url = urlresolvers.reverse_lazy('reminders:reminders')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # store old folllow_up so we can compare later
        self.old_follow_up = self.object.follow_up

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        response = super().form_valid(form)

        order = self.object.order
        claimant = order.claimant
        client = claimant.get_client()
        error = ''

        subject = 'Payment Reminder'
        body = (
            'Hi {claimant},\n'
            '\n'
            'This is a reminder that your Order '
            'arrived on {arrived}, and is available for pickup.\n'
            '\n'
            'Regards,\n'
            '\n'
            '-Perfect Arch Team\n'
            '\n'
            '{address}\n'
            '\n'.format(
                claimant=claimant,
                arrived=defaultfilters.date(
                    order.arrived_date, "N j, Y"
                ),
                address=settings.BILL_TO[0][1],
            )
        )
        error += send_reminder_email(
            self.object,
            client,
            self.old_follow_up,
            subject,
            body,
            user=self.request.user
        )

        if error:
            error += '\\n\\n'

        body = (
            'Hi {claimant}, this is a reminder that your '
            'Order arrived on {arrived}, and is available for pickup.'.format(
                claimant=claimant,
                arrived=defaultfilters.date(
                    order.arrived_date, "N j, Y"
                ),
            )
        )
        error += send_reminder_text_message(
            self.object,
            client,
            self.old_follow_up,
            body,
            user=self.request.user
        )

        if error:
            response.content = response.content.replace(
                b'}', ', "error": "{}"}}'.format(error).encode()
            )
            response.status_code = 400

        return response
