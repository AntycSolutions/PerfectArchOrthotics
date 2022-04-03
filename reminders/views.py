import smtplib
import json

from django.views import generic
from django.core import urlresolvers, mail
from django.conf import settings
from django.template import loader
from django.db import models as db_models
from django.contrib.auth import mixins

import twilio
from django_twilio import client as django_twilio_client
from utils import views_utils
from simple_search import search

from perfect_arch_orthotics.templatetags import groups as tt_groups
from clients import models as clients_models

from . import models as reminders_models, forms


class Reminders(generic.TemplateView):
    template_name = "reminders/reminders.html"

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

        created_filter = search.get_date_query(
            self.request,
            'filter-created_from',
            'filter-created_to',
            ['created'],
            context=context
        )

        insurance_str = filter_prefix + '-insurance'
        insurance_filter = db_models.Q()
        if insurance_str in GET and GET[insurance_str]:
            insurance_filter = db_models.Q(
                claim__insurance__provider=GET[insurance_str]
            )

        claims_reminder_search_filter = search.get_query(
            self.request,
            'filter-reminder_search',
            [
                'claim__patient__first_name',
                'claim__patient__last_name',
                'claim__patient__client__phone_number',
                'claim__patient__client__cell_number',
                'claim__patient__dependent__primary__phone_number',
                'claim__patient__dependent__primary__cell_number',
                'claim__insurances__provider',
            ],
            context=context
        )

        # Unpaid Claims
        unpaid_claims_reminders = (
            reminders_models.UnpaidClaimReminder.objects.select_related(
                # for patient links
                'claim__patient__client',
                'claim__patient__dependent',
            ).prefetch_related(
                # for benefits lookup
                'claim__insurances__main_claimant__client',
                'claim__insurances__main_claimant__dependent',
                # for expected back/amount claimed calcs
                (
                    'claim__claimcoverage_set__claimitem_set__item__'
                    'itemhistory_set'
                ),
                'unpaidclaimmessagelog_set',
            ).filter(
                reminder_filter,
                created_filter,
                insurance_filter,
                claims_reminder_search_filter,
            )
        )
        unpaid_claims_reminders_rows_per_page = views_utils._get_paginate_by(
            self.request, 'unpaid_claims_reminders_rows_per_page'
        )
        context['unpaid_claims_reminders_rows_per_page'] = (
            unpaid_claims_reminders_rows_per_page
        )
        unpaid_claims_reminders = views_utils._paginate(
            self.request,
            unpaid_claims_reminders,
            'unpaid_claims_reminders_page',
            unpaid_claims_reminders_rows_per_page
        )
        context['unpaid_claims_reminders'] = unpaid_claims_reminders

        arrived_orders_reminder_search_filter = search.get_query(
            self.request,
            'filter-reminder_search',
            [
                'order__claimant__first_name',
                'order__claimant__last_name',
                'order__claimant__client__phone_number',
                'order__claimant__client__cell_number',
                'order__claimant__dependent__primary__phone_number',
                'order__claimant__dependent__primary__cell_number',
            ],
            context=context
        )

        # Arrived Orders
        arrived_orders_reminders = (
            reminders_models.OrderArrivedReminder.objects.select_related(
                # for claimant links
                'order__claimant__client',
                'order__claimant__dependent',
            ).prefetch_related(
                'orderarrivedmessagelog_set',
            ).filter(
                reminder_filter,
                created_filter,
                arrived_orders_reminder_search_filter,
            )
        )
        arrived_orders_reminders_rows_per_page = views_utils._get_paginate_by(
            self.request, 'arrived_orders_reminders_rows_per_page'
        )
        context['arrived_orders_reminders_rows_per_page'] = (
            arrived_orders_reminders_rows_per_page
        )
        arrived_orders_reminders = views_utils._paginate(
            self.request,
            arrived_orders_reminders,
            'arrived_orders_reminders_page',
            arrived_orders_reminders_rows_per_page
        )
        context['arrived_orders_reminders'] = arrived_orders_reminders

        benefits_reminder_search_filter = search.get_query(
            self.request,
            'filter-reminder_search',
            [
                'client__first_name',
                'client__last_name',
                'client__phone_number',
                'client__cell_number',
                'client__dependent__primary__phone_number',
                'client__dependent__primary__cell_number',
            ],
            context=context
        )

        # Benefits Rollovers
        benefits_reminders = (
            reminders_models.BenefitsReminder.objects.select_related(
                # for claimant links
                'client',
            ).prefetch_related(
                'benefitsmessagelog_set',
            ).filter(
                reminder_filter,
                created_filter,
                benefits_reminder_search_filter,
            )
        )
        benefits_reminders_rows_per_page = views_utils._get_paginate_by(
            self.request, 'benefits_reminders_rows_per_page'
        )
        context['benefits_reminders_rows_per_page'] = (
            benefits_reminders_rows_per_page
        )
        benefits_reminders = views_utils._paginate(
            self.request,
            benefits_reminders,
            'benefits_reminders_page',
            benefits_reminders_rows_per_page
        )
        context['benefits_reminders'] = benefits_reminders

        # Claims without Orders
        claims_without_orders_reminders = (
            reminders_models.ClaimOrderReminder.objects.select_related(
                # for patient links
                'claim__patient__client',
                'claim__patient__dependent'
            ).filter(
                created_filter,
                insurance_filter,
                claims_reminder_search_filter,
            )
        )
        claims_without_orders_reminders_rows_per_page = (
            views_utils._get_paginate_by(
                self.request, 'claims_without_orders_reminders_rows_per_page'
            )
        )
        context['claims_without_orders_reminders_rows_per_page'] = (
            claims_without_orders_reminders_rows_per_page
        )
        claims_without_orders_reminders = views_utils._paginate(
            self.request,
            claims_without_orders_reminders,
            'claims_without_orders_reminders_page',
            claims_without_orders_reminders_rows_per_page
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
        context['benefits_reminder_form'] = (
            forms.BenefitsReminderForm(prefix="benefitsreminder")
        )

        return context


# send_email expects body to end in two newlines: \n\n
def send_email(client, subject, body, user=None, html_message=None):
    if settings.ENV != 'prod':
        debug = 'ENV: ' + settings.ENV
        if user:
            debug += ' - {}'.format(user)
        debug += '\n\n'

        body += debug
        if html_message:
            html_message = html_message.replace(
                '</body>', '<h3>' + debug + '</h3></body>'
            )

    try:
        mail.send_mail(
            subject, body, '', [client.email], html_message=html_message
        )
    except smtplib.SMTPRecipientsRefused:
        return (
            'Could not send email to \'{email}\''.format(
                email=client.email
            )
        )

    return ''


def send_reminder_email(
    reminder,
    client,
    old_follow_up,
    subject,
    body,
    user=None,
    html_message=None,
):
    EMAIL = reminders_models.Reminder.EMAIL
    sending_email = (
        EMAIL in reminder.follow_up and EMAIL not in old_follow_up
    )
    error = ''
    if sending_email:
        error = send_email(
            client, subject, body, user=user, html_message=html_message
        )
        if not error:
            if isinstance(reminder, reminders_models.OrderArrivedReminder):
                reminders_models.OrderArrivedMessageLog.objects.create(
                    order_arrived_reminder=reminder,
                    msg_type=reminders_models.MessageLog.EMAIL
                )
            elif isinstance(reminder, reminders_models.UnpaidClaimReminder):
                reminders_models.UnpaidClaimMessageLog.objects.create(
                    unpaid_claim_reminder=reminder,
                    msg_type=reminders_models.MessageLog.EMAIL
                )
            elif isinstance(reminder, reminders_models.BenefitsReminder):
                reminders_models.BenefitsMessageLog.objects.create(
                    benefits_reminder=reminder,
                    msg_type=reminders_models.MessageLog.EMAIL
                )
            else:
                raise Exception('Unhandled Reminder type: ' + type(reminder))

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
        if not error:
            if isinstance(reminder, reminders_models.OrderArrivedReminder):
                reminders_models.OrderArrivedMessageLog.objects.create(
                    order_arrived_reminder=reminder,
                    msg_type=reminders_models.MessageLog.TEXT
                )
            elif isinstance(reminder, reminders_models.UnpaidClaimReminder):
                reminders_models.UnpaidClaimMessageLog.objects.create(
                    unpaid_claim_reminder=reminder,
                    msg_type=reminders_models.MessageLog.TEXT
                )
            elif isinstance(reminder, reminders_models.BenefitsReminder):
                reminders_models.BenefitsMessageLog.objects.create(
                    benefits_reminder=reminder,
                    msg_type=reminders_models.MessageLog.TEXT
                )
            else:
                raise Exception('Unhandled Reminder type: ' + type(reminder))

    return error


class UnpaidClaimReminderUpdate(
    mixins.UserPassesTestMixin,
    views_utils.AjaxResponseMixin,
    generic.UpdateView,
):
    template_name = 'reminders/reminders.html'
    model = reminders_models.UnpaidClaimReminder
    form_class = forms.UnpaidClaimReminderForm
    success_url = urlresolvers.reverse_lazy('reminders:reminders')

    def test_func(self):
        return tt_groups.check_groups(self.request.user, 'Edit')

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
        address = settings.BILL_TO[0][1]
        body = (
            'Hi {patient},\n'
            '\n'
            'This is a payment reminder for your account. '
            'Please call us at (587) 400-4588.'
            '\n'
            'Thank you,\n'
            '\n'
            '-The Perfect Arch Orthotics Team\n'
            '\n\n'
            '{address}\n'
            '\n'
            'Hours:\n'
            'Monday - Friday, 10:30 AM - 7 PM\n'
            'Saturday, 11 AM - 5 PM\n'
            'Sunday, Closed\n'
            '\n'
            'This is an automated message, do not reply to this email.\n'
            '\n'.format(
                patient=patient,
                address=address,
            )
        )
        html_message = loader.render_to_string(
            'reminders/emails/unpaid_claim.html', {
                'recipient': patient,
                'subject': subject,
                'address': address,
            }
        )
        error += send_reminder_email(
            self.object,
            client,
            self.old_follow_up,
            subject,
            body,
            user=self.request.user,
            html_message=html_message,
        )

        if error:
            error += '\\n\\n'

        body = (
            'Hi {patient}, this is a payment reminder for your account with '
            'Perfect Arch Orthotics.\n\n'
            'This is an automated message, do not reply or call this number, '
            'please call us at (587) 400-4588 instead. '
            'Thank you.'.format(
                patient=patient,
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

        CALL = reminders_models.Reminder.CALL
        calling = (
            CALL in self.object.follow_up and CALL not in self.old_follow_up
        )
        if calling:
            reminders_models.UnpaidClaimMessageLog.objects.create(
                unpaid_claim_reminder=self.object,
                msg_type=reminders_models.MessageLog.CALL
            )

        return response


class OrderArrivedReminderUpdate(
    mixins.UserPassesTestMixin,
    views_utils.AjaxResponseMixin,
    generic.UpdateView,
):
    template_name = 'reminders/reminders.html'
    model = reminders_models.OrderArrivedReminder
    form_class = forms.OrderArrivedReminderForm
    success_url = urlresolvers.reverse_lazy('reminders:reminders')

    def test_func(self):
        return tt_groups.check_groups(self.request.user, 'Edit')

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

        subject = 'Order Reminder'
        address = settings.BILL_TO[0][1]
        body = (
            'Hi {claimant},\n'
            '\n'
            'This is a reminder that your {type} Order has arrived. '
            'Please kindly call us at (587) 400-4588 to schedule an'
            ' appointment to ensure availability.\n'
            '\n'
            'Thank you,\n'
            '\n'
            '-The Perfect Arch Orthotics Team\n'
            '\n\n'
            '{address}\n'
            '\n'
            'Hours:\n'
            'Monday - Friday, 10:30 AM - 7 PM\n'
            'Saturday, 11 AM - 5 PM\n'
            'Sunday, Closed\n'
            '\n'
            'This is an automated message, do not reply to this email.\n'
            '\n'.format(
                type=order.get_order_type_display(),
                claimant=claimant,
                address=address,
            )
        )
        html_message = loader.render_to_string(
            'reminders/emails/order_arrived.html', {
                'type': order.get_order_type_display(),
                'recipient': claimant,
                'subject': subject,
                'address': address,
            }
        )
        error += send_reminder_email(
            self.object,
            client,
            self.old_follow_up,
            subject,
            body,
            user=self.request.user,
            html_message=html_message,
        )

        if error:
            error += '\\n\\n'

        body = (
            'Hi {claimant}, this is a reminder that your {type} Order has'
            ' arrived at Perfect Arch Orthotics.\n\n'
            'This is an automated message, do not reply or call this number. '
            'Please kindly call us at (587) 400-4588 to schedule an'
            ' appointment to ensure availability.'
            ''.format(
                type=order.get_order_type_display(), claimant=claimant
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

        CALL = reminders_models.Reminder.CALL
        calling = (
            CALL in self.object.follow_up and CALL not in self.old_follow_up
        )
        if calling:
            reminders_models.OrderArrivedMessageLog.objects.create(
                order_arrived_reminder=self.object,
                msg_type=reminders_models.MessageLog.CALL
            )

        return response


class BenefitsReminderUpdate(
    mixins.UserPassesTestMixin,
    views_utils.AjaxResponseMixin,
    generic.UpdateView,
):
    template_name = 'reminders/reminders.html'
    model = reminders_models.BenefitsReminder
    form_class = forms.BenefitsReminderForm
    success_url = urlresolvers.reverse_lazy('reminders:reminders')

    def test_func(self):
        return tt_groups.check_groups(self.request.user, 'Edit')

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

        client = self.object.client
        error = ''

        subject = 'Benefits Rollover'
        address = settings.BILL_TO[0][1]
        new_year_body = (
            'It\'s a new year! We would like to remind you that you may'
            ' be eligible to do a new claim.'
        )
        body = (
            'Hi {client},\n'
            '\n'
            # 'This is a reminder that your Benefits have rolled over. '
            '{new_year_body} '
            'Please kindly call us at (587) 400-4588 to schedule an'
            ' appointment to ensure availability.\n'
            '\n'
            'Thank you,\n'
            '\n'
            '-The Perfect Arch Orthotics Team\n'
            '\n\n'
            '{address}\n'
            '\n'
            'Hours:\n'
            'Monday - Friday, 10:30 AM - 7 PM\n'
            'Saturday, 11 AM - 5 PM\n'
            'Sunday, Closed\n'
            '\n'
            'This is an automated message, do not reply to this email.\n'
            '\n'.format(
                client=client,
                new_year_body=new_year_body,
                address=address,
            )
        )
        html_message = loader.render_to_string(
            'reminders/emails/benefits_rollover.html', {
                'recipient': client,
                'subject': subject,
                'address': address,
            }
        )
        error += send_reminder_email(
            self.object,
            client,
            self.old_follow_up,
            subject,
            body,
            user=self.request.user,
            html_message=html_message,
        )

        if error:
            error += '\\n\\n'

        body = (
            'Hi {client},'
            ' {new_year_body}'
            # ' this is a reminder that your Benefits have rolled over.'
            '\n\n'
            '-Perfect Arch Team\n'
            'This is an automated message, do not reply or call this number. '
            'Please kindly call us at (587) 400-4588 to schedule an'
            ' appointment to ensure availability.'
            ''.format(
                client=client,
                new_year_body=new_year_body,
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

        CALL = reminders_models.Reminder.CALL
        calling = (
            CALL in self.object.follow_up and CALL not in self.old_follow_up
        )
        if calling:
            reminders_models.BenefitsMessageLog.objects.create(
                benefits_reminder=self.object,
                msg_type=reminders_models.MessageLog.CALL
            )

        return response
