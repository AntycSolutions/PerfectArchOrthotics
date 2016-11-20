import datetime
import smtplib
import json

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
        now = timezone.now()
        now_date = timezone.localtime(now).date()
        three_weeks_ago = now - three_weeks

        claims = clients_models.Claim.objects.prefetch_related(
            'unpaidclaimreminder_set',
        ).filter(
            claimcoverage__actual_paid_date__isnull=True,
            submitted_datetime__lte=three_weeks_ago,
        ).distinct()

        new_unpaid_claims_reminders = []
        for claim in claims:
            if not claim.unpaidclaimreminder_set.exists():
                new_unpaid_claims_reminders.append(
                    reminders_models.UnpaidClaimReminder(
                        claim=claim, created=now_date
                    )
                )
        reminders_models.UnpaidClaimReminder.objects.bulk_create(
            new_unpaid_claims_reminders
        )

        reminders_models.UnpaidClaimReminder.objects.filter(
            claim__claimcoverage__actual_paid_date__isnull=True,
            created__lte=timezone.localtime(three_weeks_ago).date()
        ).update(
            follow_up=reminders_models.Reminder.REQUIRED,
            result='',
            created=now_date
        )

    def _find_arrived_orders(self):
        one_week = datetime.timedelta(weeks=1)
        now = timezone.now()
        now_date = timezone.localtime(now).date()
        one_week_ago = now - one_week

        orders = inventory_models.CoverageOrder.objects.prefetch_related(
            'orderarrivedreminder_set',
        ).filter(
            order_type=clients_models.Coverage.ORTHOTICS,
            dispensed_date__isnull=True,
            arrived_date__lte=one_week_ago,
        )

        new_arrived_orders_reminders = []
        for order in orders:
            if not order.orderarrivedreminder_set.exists():
                new_arrived_orders_reminders.append(
                    reminders_models.OrderReminder(
                        order=order, created=now_date
                    )
                )
        reminders_models.OrderArrivedReminder.objects.bulk_create(
            new_arrived_orders_reminders
        )

        reminders_models.OrderArrivedReminder.objects.filter(
            order__dispensed_date__isnull=True,
            created__lte=timezone.localtime(one_week_ago).date()
        ).update(
            follow_up=reminders_models.Reminder.REQUIRED,
            result='',
            created=now_date
        )

    def _find_claims_without_orders(self):
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
        reminders_models.ClaimOrderReminder.objects.bulk_create(
            new_claims_without_orders_reminders
        )

        reminders_models.ClaimOrderReminder.objects.filter(
            claim__coverageorder__order_type=ORTHOTICS
        ).delete()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            # PostgreSQL
            providers = list(
                clients_models.Insurance.objects.all().distinct(
                    'provider'
                ).values_list(
                    'provider', flat=True
                )
            )
        except NotImplementedError:
            # SQLite
            providers = list(set(
                clients_models.Insurance.objects.all().values_list(
                    'provider', flat=True
                )
            ))
        context['provider_choices'] = json.dumps(providers)

        GET = self.request.GET.copy()

        follow_up_prefix = 'follow_up'
        follow_up_str = follow_up_prefix + '-follow_up'
        no_value = (
            (follow_up_str not in GET) or (not GET.getlist(follow_up_str))
        )
        if no_value:
            GET.setlist(follow_up_str, [reminders_models.Reminder.REQUIRED])
        follow_up_list = GET.getlist(follow_up_str)
        context['follow_up_form'] = forms.FollowUpForm(
            GET, prefix=follow_up_prefix
        )

        filter_prefix = 'filter'
        result_str = filter_prefix + '-result'
        context['filter_form'] = forms.ReminderForm(GET, prefix=filter_prefix)

        """
            Instead of using a cron like system of creating reminders
            we create the reminders upon viewing the page, not exactly
            the best implmentation but it works
        """

        reminder_filter = db_models.Q()

        for follow_up in follow_up_list:
            reminder_filter &= db_models.Q(follow_up__contains=follow_up)

        if result_str in GET and GET[result_str]:
            reminder_filter &= db_models.Q(result=GET[result_str])

        created_filter = views_utils._get_date_filter(
            self.request,
            context,
            'filter-created_from',
            'filter-created_to',
            ['created']
        )

        insurance_str = filter_prefix + '-insurance'
        insurance_filter = db_models.Q()
        if insurance_str in GET and GET[insurance_str]:
            insurance_filter = db_models.Q(
                claim__insurance__provider=GET[insurance_str]
            )

        self._find_unpaid_claims()
        unpaid_claims_reminders = (
            reminders_models.UnpaidClaimReminder.objects.select_related(
                # for patient links
                'claim__patient__client',
                'claim__patient__dependent',
                # for benefits lookup
                'claim__insurance__main_claimant__client',
                'claim__insurance__main_claimant__dependent',
            ).prefetch_related(
                # for expected back/amount claimed calcs
                'claim__claimcoverage_set__claimitem_set__item__'
                'itemhistory_set',
            ).filter(reminder_filter, created_filter, insurance_filter)
        )
        context['unpaid_claims_reminders'] = unpaid_claims_reminders

        self._find_arrived_orders()
        arrived_orders_reminders = (
            reminders_models.OrderArrivedReminder.objects.select_related(
                # for claimant links
                'order__claimant__client',
                'order__claimant__dependent',
            ).filter(reminder_filter, created_filter)
        )
        context['arrived_orders_reminders'] = arrived_orders_reminders

        self._find_claims_without_orders()
        claims_without_orders_reminders = (
            reminders_models.ClaimOrderReminder.objects.select_related(
                # for patient links
                'claim__patient__client',
                'claim__patient__dependent'
            ).filter(created_filter, insurance_filter)
        )
        context['claims_without_orders_reminders'] = (
            claims_without_orders_reminders
        )

        context['unpaid_claim_reminder_form'] = (
            forms.UnpaidClaimReminderForm(prefix="unpaidclaimreminder")
        )
        context['order_arrived_reminder_form'] = (
            forms.OrderArrivedReminderForm(prefix="orderarrivedreminder")
        )

        return context


# send_email expects body to end in two newlines: \n\n
def send_email(client, subject, body, user=None):
    if settings.ENV != 'prod':
        body += 'ENV: ' + settings.ENV
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
        body += '\nENV: ' + settings.ENV
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


class UnpaidClaimReminderUpdate(
    views_utils.AjaxResponseMixin, generic.UpdateView
):
    template_name = 'reminders/reminders.html'
    model = reminders_models.UnpaidClaimReminder
    form_class = forms.UnpaidClaimReminderForm
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


class OrderArrivedReminderUpdate(
    views_utils.AjaxResponseMixin, generic.UpdateView
):
    template_name = 'reminders/reminders.html'
    model = reminders_models.OrderArrivedReminder
    form_class = forms.OrderArrivedReminderForm
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
