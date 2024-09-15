import os
import io
import collections
import itertools
from cgi import escape

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import http, forms
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.template.loader import get_template
from django.contrib import messages
from django.db.models import Sum, Case, When, Q
from django.core import urlresolvers
from django.utils import safestring, timezone

import xhtml2pdf.pisa as pisa
from crispy_forms import helper

from simple_search.utils import get_query, get_date_query
from utils import views_utils

from perfect_arch_orthotics.templatetags import groups as tt_groups
from clients.models import Client, Dependent, Claim, Insurance, \
    Item, Coverage, ClaimItem, ClaimCoverage
from clients import models as clients_models
from inventory import models as inventory_models
from clients.forms.forms import ClientForm, DependentForm
from clients.forms import forms as clients_forms
from reminders import (
    models as reminders_models,
    forms as reminders_forms,
)


# TODO: split into multiple views

# Convert HTML URIs to absolute system paths so xhtml2pdf can access those
# resources
def link_callback(uri, rel):
    # use short variable names
    sUrl = settings.STATIC_URL    # Typically /static/
    sRoot = settings.STATIC_ROOT  # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL     # Typically /static/media/
    mRoot = settings.MEDIA_ROOT   # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    path = ""
    path2 = ""
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
        # Also check other static dirs, for devl
        path2 = path.replace("static", "assets")

    # make sure that file exists
    if os.path.isfile(path):
        return os.path.normpath(path)
    elif os.path.isfile(path2):
        return os.path.normpath(path2)
    else:
        raise Exception(
            'media URI must start with {} or {}'.format(sUrl, mUrl)
        )


@login_required
def render_to_pdf(request, template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = io.BytesIO()

    # UTF-8 or ISO-8859-1
    # pdf = pisa.pisaDocument(
    #     io.BytesIO("Test".encode("UTF-8")),
    #     result,
    #     link_callback=link_callback
    # )
    pdf = pisa.pisaDocument(
        io.BytesIO(html.encode("UTF-8")),
        result,
        link_callback=link_callback,
        encoding="UTF-8"
    )
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')

    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))


def invoice_view(request, claim_id):
    claim, patient, invoice, invoice_number = _invoice(claim_id)
    bill_to = settings.BILL_TO[0][1]
    logo = 'images/PerfectArchLogo.jpg'
    template = 'clients/pdfs/invoice.html'
    if invoice.company == invoice.PC_MEDICAL:
        bill_to = settings.BILL_TO[1][1]
        logo = 'images/PCMedicalLogo.jpg'
        template = 'clients/pdfs/pc_medical_invoice.html'
    elif invoice.company == invoice.BRACE_AND_BODY:
        bill_to = settings.BILL_TO[2][1]
        logo = 'images/BraceAndBodyLogo.png'
        template = 'clients/pdfs/brace_and_body_invoice.html'
    company_name = bill_to.split('\n')[0]
    company_address = bill_to.replace(company_name + '\n', '')

    return render_to_pdf(
        request,
        template,
        {'pagesize': 'A4',
         'claim': claim,
         'invoice': invoice,
         'invoice_number': invoice_number,
         'company_name': company_name,
         'company_address': company_address,
         'logo': logo,
         'item_class': Item,
         'claim_item_class': ClaimItem,
         # 'insurance_class': Insurance,
         'is_prod': request.get_host() == "perfectarch.ca"}
    )


def _invoice(claim_id):
    try:
        claim = Claim.objects.get(id=claim_id)
    except Claim.DoesNotExist:
        raise http.Http404("No Claim matches that ID")
    patient = claim.patient
    invoice = None
    try:
        invoice = claim.invoice
        invoice_number = invoice.invoice_number
    except clients_models.Invoice.DoesNotExist:
        invoice_number = claim.id
    invoice_number = "{0:05d}".format(invoice_number)

    return claim, patient, invoice, invoice_number


def insurance_letter_view(request, claim_id):
    claim, patient, insurance_letter = _insurance_letter(claim_id)

    # Because !@#$ xhtml2pdf (putting these in css classes didnt work)
    underline = (
        'border-bottom: 1pt solid #000000;'
        ' width: 25px;'
        ' text-align: center;'
        ' line-height: 5px;'
        ' font-family: monospace;'
    )
    notunderline = (
        'text-align: left;'
        ' line-height: 5px;'
    )

    return render_to_pdf(
        request,
        'clients/pdfs/insurance_letter.html',
        {
            'pagesize': 'A4',
            'claim': claim,
            'patient': patient,
            'insurance_letter': insurance_letter,
            'underline': underline,
            'notunderline': notunderline,
            'address': settings.BILL_TO[0][1],
            'three_d_laser_scan': claim.insurances.filter(
                three_d_laser_scan=True
            ).exists(),
        }
    )


def _insurance_letter(claim_id):
    try:
        claim = Claim.objects.get(id=claim_id)
    except Claim.DoesNotExist:
        raise http.Http404("No Claim matches that ID")
    patient = claim.patient
    insurance_letter = None
    try:
        insurance_letter = claim.insuranceletter
    except clients_models.InsuranceLetter.DoesNotExist:
        pass

    return claim, patient, insurance_letter


def proof_of_manufacturing_view(request, claim_id):
    claim, proof_of_manufacturing, invoice_number = _proof_of_manufacturing(
        claim_id
    )
    orthotics_pros_lab = settings.LABORATORIES[5][1]
    tokens = orthotics_pros_lab.split('\n')
    address = '\n'.join(tokens[1:3])
    phone = tokens[5].split(' ', 1)[1]

    return render_to_pdf(
        request,
        'clients/pdfs/proof_of_manufacturing.html',
        {
            'pagesize': 'A4',
            'claim': claim,
            'proof_of_manufacturing': proof_of_manufacturing,
            'invoice_number': invoice_number,
            'address': address,
            'phone': phone,
        }
    )


def _proof_of_manufacturing(claim_id):
    try:
        claim = Claim.objects.get(id=claim_id)
    except Claim.DoesNotExist:
        raise http.Http404("No Claim matches that ID")
    proof_of_manufacturing = None
    try:
        proof_of_manufacturing = claim.proofofmanufacturing
    except clients_models.ProofOfManufacturing.DoesNotExist:
        pass

    invoice_number = (
        ((proof_of_manufacturing and proof_of_manufacturing.id) or claim.id)
        + 500  # add 500 to make invoice numbers seem higher
    )

    return claim, proof_of_manufacturing, invoice_number


@login_required
def fillOutInvoiceView(request, claim_id):
    claim, patient, invoice, invoice_number = _invoice(claim_id)

    context = {
        'patient': patient,
        'claim': claim,
        'invoice': invoice,
        'insurance_class': Insurance,
        'invoice_number': invoice_number
    }

    return render(request, 'clients/make_invoice.html', context)


@login_required
def fillOutInsuranceLetterView(request, claim_id):
    claim, patient, insurance_letter = _insurance_letter(claim_id)

    underline = (
        'border-bottom: 1pt solid #000000;'
        ' width: 30px;'
        ' text-align: center;'
        ' line-height: 10px;'
        ' font-family: monospace;'
    )
    notunderline = (
        'text-align: left;'
        ' line-height: 10px;'
    )

    context = {
        'patient': patient,
        'claim': claim,
        'insurance_letter': insurance_letter,
        'underline': underline,
        'notunderline': notunderline,
        'three_d_laser_scan': claim.insurances.filter(
            three_d_laser_scan=True
        ).exists(),
    }

    return render(request, 'clients/make_insurance_letter.html', context)


@login_required
def fillOutProofOfManufacturingView(request, claim_id):
    claim, proof_of_manufacturing, invoice_number = _proof_of_manufacturing(
        claim_id)

    context = {
        'claim': claim,
        'proof_of_manufacturing': proof_of_manufacturing,
        'invoice_number': invoice_number
    }

    return render(request, 'clients/make_proof_of_manufacturing.html', context)


@login_required
def claimView(request, claim_id):
    try:
        claim = Claim.objects.select_related(
            'patient__client', 'patient__dependent__primary'
        ).prefetch_related(
            'insurances__coverage_set',
            'claimcoverage_set__claimitem_set__item__itemhistory_set',
            'claimcoverage_set__coverage',
            'coverageorder_set'
        ).get(id=claim_id)
    except Claim.DoesNotExist:
        raise http.Http404("No Claim matches that ID")

    invalid_coverages = False
    for insurance in claim.insurances.all():
        for coverage in insurance.coverage_set.all():
            is_BENEFIT_YEAR = (
                coverage.period == clients_models.Coverage.BENEFIT_YEAR
            )
            if is_BENEFIT_YEAR and coverage.period_date is None:
                invalid_coverages = True
                messages.add_message(
                    request,
                    messages.ERROR,
                    safestring.mark_safe(
                        "One of {}'s Coverages is set to Benefit Year "
                        "but does not have a Period Date set. Please "
                        "<a href='{}'>Click here to edit it</a> ".format(
                            coverage.claimant,
                            urlresolvers.reverse(
                                'insurance_update',
                                kwargs={'insurance_id': coverage.insurance.pk}
                            )
                        )
                    )
                )

    context = {
        'claim': claim,
        'claim_coverage_class': ClaimCoverage,
        'coverage_class': Coverage,
        'claim_item_class': ClaimItem,
        'item_class': Item,
        'now': timezone.now(),
        'invalid_coverages': invalid_coverages,
    }

    return render(request, 'clients/claim.html', context)


@login_required
def clientSearchView(request):
    context = {}

    found_clients = Client.objects.order_by('-id')
    found_dependents = Dependent.objects.order_by('-id')
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        context['q'] = query_string

        person_fields = [
            'first_name', 'last_name', 'health_care_number', 'employer'
        ]

        client_fields = person_fields + [
            'address', 'phone_number', 'cell_number', 'email'
        ]
        client_query = get_query(query_string, client_fields)
        found_clients = Client.objects.filter(client_query)

        dependent_fields = person_fields
        dependent_query = get_query(query_string, dependent_fields)
        found_dependents = Dependent.objects.filter(dependent_query)

    clients_rows_per_page = views_utils._get_paginate_by(
        request, 'clients_rows_per_page'
    )

    clients = views_utils._paginate(
        request,
        list(itertools.chain(found_clients, found_dependents)),
        'page',
        clients_rows_per_page
    )

    context['clients'] = clients
    context['clients_rows_per_page'] = clients_rows_per_page

    return render(request, 'clients/clients.html', context)


def _actual_paid_date(request, context_dict, found_claims):
    apd = 'apd'
    if apd in request.GET and request.GET[apd].strip():
        apd_value = request.GET[apd]
        context_dict[apd] = apd_value

        if apd_value == 'has_actual_paid_date':
            actual_paid_date = False
        elif apd_value == 'no_actual_paid_date':
            actual_paid_date = True
        elif apd_value == 'both_actual_paid_date':
            return found_claims

        if found_claims:
            found_claims = found_claims.filter(
                claimcoverage__actual_paid_date__isnull=actual_paid_date
            ).distinct()
        else:
            found_claims = Claim.objects.filter(
                claimcoverage__actual_paid_date__isnull=actual_paid_date
            ).distinct()

    return found_claims


def _run_query(request, claim_query, found_claims):
    if claim_query:
        if found_claims:
            found_claims = found_claims.filter(claim_query)
        else:
            found_claims = Claim.objects.filter(claim_query)
    else:
        messages.add_message(request, messages.WARNING,
                             "Invalid date. Please use MM/DD/YYYY.")

    return found_claims


def _date_from_date_to(
    request, context_dict, found_claims, df, dt, date_field
):
    if ((df in request.GET) and request.GET[df].strip()
            and (dt in request.GET) and request.GET[dt].strip()):
        query_date_from_string = request.GET[df]
        query_date_to_string = request.GET[dt]
        context_dict[df] = query_date_from_string
        context_dict[dt] = query_date_to_string
        claim_query = get_date_query(query_date_from_string,
                                     query_date_to_string, [date_field])

        found_claims = _run_query(request, claim_query, found_claims)
    elif (df in request.GET) and request.GET[df].strip():
        query_date_from_string = request.GET[df]
        context_dict[df] = query_date_from_string
        claim_query = get_date_query(query_date_from_string,
                                     None, [date_field])

        found_claims = _run_query(request, claim_query, found_claims)
    elif (dt in request.GET) and request.GET[dt].strip():
        query_date_to_string = request.GET[dt]
        context_dict[dt] = query_date_to_string
        claim_query = get_date_query(None,
                                     query_date_to_string, [date_field])

        found_claims = _run_query(request, claim_query, found_claims)

    return found_claims


class PaymentTypeForm(forms.ModelForm):
    class Meta:
        model = ClaimCoverage
        fields = ('payment_type',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['payment_type'].label += ':'

        self.helper = helper.FormHelper(self)
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.field_template = 'bootstrap3/layout/inline_field.html'


def _payment_type(request, context_dict, found_claims):
    context_dict['payment_type_form'] = PaymentTypeForm(request.GET)

    payment_type_filter = (
        'payment_type' in request.GET and request.GET['payment_type'].strip()
    )
    if payment_type_filter:
        fields = ['claimcoverage__payment_type']
        query_string = request.GET['payment_type'].strip()
        context_dict['payment_type'] = query_string
        claim_query = get_query(query_string, fields)
        if found_claims:
            found_claims = found_claims.filter(claim_query)
        else:
            found_claims = Claim.objects.filter(claim_query)

    return found_claims


def _found_claims(request, context):
    # Start from all, drilldown to q df dt
    found_claims = Claim.objects.select_related(
        'patient__client',
        'patient__dependent__primary'
    ).prefetch_related(
        'insurances',
        'claimcoverage_set__claimitem_set__item__itemhistory_set',
        'claimcoverage_set__coverage',
        'coverageorder_set'
    ).order_by(
        '-submitted_datetime'
    )

    # Query, Date From, Date To
    if ('q' in request.GET) and request.GET['q'].strip():
        fields = ['patient__first_name', 'patient__last_name',
                  'insurances__provider', 'patient__employer']
        query_string = request.GET['q']
        context['q'] = query_string
        claim_query = get_query(query_string, fields)
        if found_claims:
            found_claims = found_claims.filter(claim_query)
        else:
            found_claims = Claim.objects.filter(claim_query)

    found_claims = _date_from_date_to(request, context, found_claims,
                                      'apdf', 'apdt',
                                      'claimcoverage__actual_paid_date')

    found_claims = _date_from_date_to(request, context, found_claims,
                                      'sdf', 'sdt', 'submitted_datetime')

    found_claims = _payment_type(request, context, found_claims)

    found_claims = _actual_paid_date(request, context, found_claims)

    return found_claims


@login_required
def claims_search_stats(request):
    context = {}

    found_claims = _found_claims(request, {})

    # Expected Back
    totals = ClaimCoverage.objects.filter(
        claim__in=found_claims,
    ).aggregate(
        non_assignment_expected_back=Sum(Case(
            When(
                claim__insurances__benefits='na',
                then='expected_back',
            ),
            default=0,
        )),
        assignment_expected_back=Sum(Case(
            When(
                Q(claim__insurances__benefits='a') &
                Q(actual_paid_date__isnull=False),
                then='expected_back',
            ),
            default=0,
        )),
        pending_assignment_expected_back=Sum(Case(
            When(
                Q(claim__insurances__benefits='a') &
                Q(actual_paid_date__isnull=True),
                then='expected_back',
            ),
            default=0,
        )),
    )
    non_assignment_expected_back = (
        totals['non_assignment_expected_back'] or 0
    )
    assignment_expected_back = (totals['assignment_expected_back'] or 0)
    pending_assignment_expected_back = (
        totals['pending_assignment_expected_back'] or 0
    )

    # Amount Claimed
    assignment_amount_claimed = 0
    non_assignment_amount_claimed = 0
    # amount looks up the Item's historical value, so we can't do this is an
    #  aggregate
    for amount_claimed_claim in found_claims:
        for claimcoverage in amount_claimed_claim.claimcoverage_set.all():
            benefits = claimcoverage.coverage.insurance.benefits
            for claimitem in claimcoverage.claimitem_set.all():
                if benefits == Insurance.ASSIGNMENT:
                    assignment_amount_claimed += claimitem.unit_price_amount()
                elif benefits == Insurance.NON_ASSIGNMENT:
                    assignment_amount_claimed += claimitem.unit_price_amount()
                elif not benefits:
                    pass
                else:
                    raise Exception('Unknown Insurance benefits')

    total_assignment_expected_back = \
        assignment_expected_back + pending_assignment_expected_back

    context['assignment_amount_claimed'] = assignment_amount_claimed
    context['non_assignment_amount_claimed'] = \
        non_assignment_amount_claimed
    context['total_amount_claimed'] = \
        assignment_amount_claimed + non_assignment_amount_claimed
    context['non_assignment_expected_back'] = non_assignment_expected_back
    context['assignment_expected_back'] = assignment_expected_back
    context['pending_assignment_expected_back'] = \
        pending_assignment_expected_back
    context['total_assignment_expected_back'] = \
        total_assignment_expected_back
    context['total_expected_back'] = \
        non_assignment_expected_back + total_assignment_expected_back

    return http.JsonResponse(context)


@login_required
def claimSearchView(request):
    context = {}

    found_claims = _found_claims(request, context)

    claims_rows_per_page = views_utils._get_paginate_by(
        request, 'claims_rows_per_page'
    )
    claims = views_utils._paginate(request, found_claims, 'page',
                                   claims_rows_per_page)

    context['claims'] = claims
    context['claims_rows_per_page'] = claims_rows_per_page
    context['now'] = timezone.now()

    return render(request, 'clients/claims.html', context)


@login_required
def insuranceSearchView(request):
    context = {}

    found_insurances = Insurance.objects.select_related(
        'main_claimant__client',
        'main_claimant__dependent__primary'
    ).prefetch_related(
        'coverage_set__claimcoverage_set__claimitem_set',
        'coverage_set__claimant__client',
        'coverage_set__claimant__dependent__primary'
    ).all()
    if ('q' in request.GET) and request.GET['q'].strip():
        fields = ["provider", "policy_number",
                  "main_claimant__first_name", "main_claimant__last_name",
                  "main_claimant__employer"]
        query_string = request.GET['q']
        context['q'] = query_string
        insurance_query = get_query(query_string, fields)
        found_insurances = Insurance.objects.filter(insurance_query)

    insurances_rows_per_page = views_utils._get_paginate_by(
        request, 'insurances_rows_per_page'
    )
    insurances = views_utils._paginate(request, found_insurances, 'page',
                                       insurances_rows_per_page)

    context['insurances'] = insurances
    context['insurances_rows_per_page'] = insurances_rows_per_page

    return render(request, 'clients/insurances.html', context)


@login_required
def clientView(request, client_id):
    context = {}

    try:
        client = Client.objects.select_related(
            'referred_by',
            'person_ptr'
        ).prefetch_related(
            'dependent_set__person_ptr__referred_set',
            'person_ptr__referred_set'
        ).get(
            id=client_id
        )
    except Client.DoesNotExist:
        raise http.Http404("No Client matches that ID")
    context['client'] = client
    dependents = client.dependent_set.all()
    person_pk_list = [client.pk]

    orders = []
    if client.order_set.exists():
        orders.append(_order_info(client, request))
    context['orders'] = orders
    has_shoe_info = tt_groups.check_groups(request.user, 'Shoe_Info')
    if not has_shoe_info:
        context['hidden_order_fields'] = ['description']

    spouse = None
    children = []
    for dependent in dependents:
        if dependent.relationship == Dependent.SPOUSE:
            spouse = dependent
        else:
            children.append(dependent)
        person_pk_list.append(dependent.pk)
        if dependent.order_set.exists():
            orders.append(_order_info(dependent, request))
    context['spouse'] = spouse
    context['children'] = children

    insurances = Insurance.objects.select_related(
        'main_claimant__client',
        'main_claimant__dependent__primary'
    ).prefetch_related(
        'coverage_set__claimant__client',
        'coverage_set__claimant__dependent__primary'
    ).filter(
        main_claimant_id__in=person_pk_list
    )

    invalid_coverages = False
    for insurance in insurances:
        for coverage in insurance.coverage_set.all():
            is_BENEFIT_YEAR = (
                coverage.period == clients_models.Coverage.BENEFIT_YEAR
            )
            if is_BENEFIT_YEAR and coverage.period_date is None:
                invalid_coverages = True
                messages.add_message(
                    request,
                    messages.ERROR,
                    safestring.mark_safe(
                        "One of {}'s Coverages is set to Benefit Year "
                        "but does not have a Period Date set. Please "
                        "<a href='{}'>Click here to edit it</a> ".format(
                            coverage.claimant,
                            urlresolvers.reverse(
                                'insurance_update',
                                kwargs={'insurance_id': coverage.insurance.pk}
                            )
                        )
                    )
                )
    if invalid_coverages:
        insurances = None
    context['insurances'] = insurances

    claims = Claim.objects.select_related(
        'patient__client',
        'patient__dependent__primary'
    ).prefetch_related(
        'insurances',
        'claimcoverage_set__claimitem_set__item__itemhistory_set',
        'claimcoverage_set__coverage',
        'claimcoverage_set__items',
        'coverages'
    ).filter(
        patient_id__in=person_pk_list
    )

    totals = ClaimCoverage.objects.filter(
        actual_paid_date__isnull=False,
        claim__in=claims,
    ).aggregate(
        expected_back__sum=Sum('expected_back'),
    )
    client_total_expected_back = totals['expected_back__sum'] or 0
    context['client_total_expected_back'] = client_total_expected_back

    client_total_amount_claimed = 0
    pending_client_total_amount_claimed = 0
    for claim in claims:
        for claimcoverage in claim.claimcoverage_set.all():
            for claimitem in claimcoverage.claimitem_set.all():
                amounts = claimitem.get_amount()
                if claimcoverage.actual_paid_date:
                    client_total_amount_claimed += amounts['unit_price']
                else:
                    pending_client_total_amount_claimed += \
                        amounts['unit_price']
    context['client_total_amount_claimed'] = client_total_amount_claimed
    context['pending_client_total_amount_claimed'] = (
        pending_client_total_amount_claimed
    )

    totals = ClaimCoverage.objects.filter(
        actual_paid_date__isnull=True,
        claim__in=claims,
    ).aggregate(
        expected_back__sum=Sum('expected_back'),
    )
    pending_client_total_expected_back = totals['expected_back__sum'] or 0
    context['pending_client_total_expected_back'] = (
        pending_client_total_expected_back
    )

    total = inventory_models.ShoeOrder.objects.filter(
        claimant_id__in=person_pk_list,
        returned_date__isnull=True,
    ).aggregate(
        shoe_order_cost=Sum('shoe_attributes__shoe__cost')
    )
    shoe_order_cost = total['shoe_order_cost'] or 0
    total = inventory_models.CoverageOrder.objects.filter(
        claimant_id__in=person_pk_list
    ).aggregate(
        coverage_order_cost=Sum('credit_value')
    )
    coverage_order_cost = total['coverage_order_cost'] or 0

    # Paginate Claims
    claims = views_utils._paginate(
        request, claims.order_by('-submitted_datetime'), 'claims_page', 5
    )
    context['client_claims'] = claims

    client_expected_back = (
        client_total_expected_back + pending_client_total_expected_back
    )
    context['client_expected_back'] = client_expected_back
    client_cost = (
        shoe_order_cost + coverage_order_cost
    )
    context['client_cost'] = client_cost

    biomechanical_gaits = \
        clients_models.BiomechanicalGait.objects.select_related(
            'patient__client',
            'patient__dependent__primary'
        ).filter(
            patient_id__in=person_pk_list
        )
    context['biomechanical_gaits'] = biomechanical_gaits
    biomechanical_gaits_2 = \
        clients_models.BiomechanicalGait2.objects.select_related(
            'patient__client',
            'patient__dependent__primary'
        ).filter(
            patient_id__in=person_pk_list
        )
    context['biomechanical_gaits_2'] = biomechanical_gaits_2

    # Reminders
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
            claim__patient_id__in=person_pk_list
        )
    )
    unpaid_claims_reminders_rows_per_page = views_utils._get_paginate_by(
        request, 'unpaid_claims_reminders_rows_per_page', context=context
    )
    unpaid_claims_reminders = views_utils._paginate(
        request,
        unpaid_claims_reminders,
        'unpaid_claims_reminders_page',
        unpaid_claims_reminders_rows_per_page
    )
    context['unpaid_claims_reminders'] = unpaid_claims_reminders
    arrived_orders_reminders = (
        reminders_models.OrderArrivedReminder.objects.select_related(
            # for claimant links
            'order__claimant__client',
            'order__claimant__dependent',
        ).prefetch_related(
            'orderarrivedmessagelog_set',
        ).filter(
            order__claimant_id__in=person_pk_list
        )
    )
    arrived_orders_reminders_rows_per_page = views_utils._get_paginate_by(
        request, 'arrived_orders_reminders_rows_per_page', context=context
    )
    arrived_orders_reminders = views_utils._paginate(
        request,
        arrived_orders_reminders,
        'arrived_orders_reminders_page',
        arrived_orders_reminders_rows_per_page
    )
    context['arrived_orders_reminders'] = arrived_orders_reminders
    claims_without_orders_reminders = (
        reminders_models.ClaimOrderReminder.objects.select_related(
            # for patient links
            'claim__patient__client',
            'claim__patient__dependent',
        ).filter(
            claim__patient_id__in=person_pk_list
        )
    )
    claims_without_orders_reminders_rows_per_page = (
        views_utils._get_paginate_by(
            request,
            'claims_without_orders_reminders_rows_per_page',
            context=context
        )
    )
    claims_without_orders_reminders = views_utils._paginate(
        request,
        claims_without_orders_reminders,
        'claims_without_orders_reminders_page',
        claims_without_orders_reminders_rows_per_page
    )
    context['claims_without_orders_reminders'] = (
        claims_without_orders_reminders
    )

    # Reminders Forms
    unpaid_claim_reminder_form = (
        reminders_forms.UnpaidClaimReminderForm(prefix="unpaidclaimreminder")
    )
    context['unpaid_claim_reminder_form'] = unpaid_claim_reminder_form
    order_arrived_reminder_form = (
        reminders_forms.OrderArrivedReminderForm(prefix="orderarrivedreminder")
    )
    context['order_arrived_reminder_form'] = order_arrived_reminder_form

    # Message Logs
    unpaid_claim_message_logs = (
        reminders_models.UnpaidClaimMessageLog.objects.filter(
            unpaid_claim_reminder__claim__patient_id__in=person_pk_list
        ).order_by('-created')
    )
    unpaid_claim_message_logs_rows_per_page = views_utils._get_paginate_by(
        request, 'unpaid_claim_message_logs_rows_per_page', context=context
    )
    unpaid_claim_message_logs = views_utils._paginate(
        request,
        unpaid_claim_message_logs,
        'unpaid_claim_message_logs_page',
        unpaid_claim_message_logs_rows_per_page
    )
    context['unpaid_claim_message_logs'] = unpaid_claim_message_logs
    order_arrived_message_logs = (
        reminders_models.OrderArrivedMessageLog.objects.filter(
            order_arrived_reminder__order__claimant_id__in=person_pk_list
        ).order_by('-created')
    )
    order_arrived_message_logs_rows_per_page = views_utils._get_paginate_by(
        request, 'order_arrived_message_logs_rows_per_page', context=context
    )
    order_arrived_message_logs = views_utils._paginate(
        request,
        order_arrived_message_logs,
        'order_arrived_message_logs_page',
        order_arrived_message_logs_rows_per_page
    )
    context['order_arrived_message_logs'] = order_arrived_message_logs

    # Forms
    if request.method == 'GET':
        # Referral Form
        try:
            referral_form = clients_forms.ReferralForm(client)
        except clients_forms.ReferralForm.EmptyClaimsQuerySet:
            referral_form = None

        # Note Form
        note_form = clients_forms.NoteForm()
    elif request.method == 'POST':
        if 'referral_submit' in request.POST:
            referral_form = clients_forms.ReferralForm(client, request.POST)
            if referral_form.is_valid():
                referral = referral_form.save(commit=False)
                referral.client = client
                referral.save()
                referral_form.save_m2m()

        if 'note_submit' in request.POST:
            if 'note_id' in request.POST:
                instance = clients_models.Note.objects.get(
                    id=request.POST['note_id']
                )
            else:
                instance = None
            note_form = clients_forms.NoteForm(request.POST, instance=instance)
            if note_form.is_valid():
                note = note_form.save(commit=False)
                note.client = client
                note.save()

        if 'delete_note_id' in request.POST:
            clients_models.Note.objects.get(
                id=request.POST['delete_note_id']
            ).delete()

        return http.HttpResponseRedirect(
            urlresolvers.reverse('client', args=[client_id])
        )
    context['referral_form'] = referral_form
    context['note_form'] = note_form

    context['margin'] = client_expected_back - client_cost
    context['dependent_class'] = Dependent
    context['now'] = timezone.now()

    return render(request, 'clients/client.html', context)


def _order_info(person, request):
    OrderInfo = collections.namedtuple(
        'OrderInfo', ['person_pk', 'name', 'order_set', 'rows_per_page']
    )

    rows_per_page = views_utils._get_paginate_by(
        request, '%s_rows_per_page' % person.pk
    )

    has_shoe_info = tt_groups.check_groups(request.user, 'Shoe_Info')
    order_set = person.order_set.all().extra(
        select={
            'null_both': ' inventory_order.dispensed_date'
                         ' is null'
                         ' and inventory_order.ordered_date'
                         ' is null',
            'null_dispensed_date': ' inventory_order.dispensed_date'
                                   ' is null',
            # 'null_ordered_date': ' inventory_order.ordered_date'
            #                      ' is null',
        }
    ).order_by(
        'null_both',
        'null_dispensed_date',
        '-dispensed_date',
        '-ordered_date',
        # '-null_ordered_date',
    )
    if not has_shoe_info:
        order_set = order_set.exclude(order_type=inventory_models.Order.SHOE)

    return OrderInfo(
        person.pk,
        person.full_name(),
        views_utils._paginate(
            request,
            order_set,
            '%s_page' % person.pk,
            rows_per_page
        ),
        rows_per_page
    )


@login_required
def add_client(request):
    has_edit = tt_groups.check_groups(request.user, 'Edit')
    if not has_edit:
        return redirect('/')
    if request.method == 'POST':
        form = ClientForm(request.POST)

        if form.is_valid():
            client = form.save()

            return redirect('add_dependent', client.id)
    else:
        form = ClientForm()

    cancel_url = urlresolvers.reverse('client_list')

    context = {
        'form': form,
        'model_name_plural': Client._meta.verbose_name_plural,
        'model_name': Client._meta.verbose_name,
        'indefinite_article': 'a',
        'cancel_url': cancel_url
    }

    return render(request, 'utils/generics/create.html', context)


@login_required
def editClientView(request, client_id):
    has_edit = tt_groups.check_groups(request.user, 'Edit')
    if not has_edit:
        return redirect('/')
    try:
        client = Client.objects.get(id=client_id)
    except Client.DoesNotExist:
        raise http.Http404("No Client matches that ID")
    if request.method == 'POST':
        client_form = ClientForm(request.POST, instance=client)
        if client_form.is_valid():
            saved = client_form.save(commit=True)

            return redirect('client', saved.id)
    else:
        client_form = ClientForm(instance=client)

    cancel_url = urlresolvers.reverse(
        'client', kwargs={'client_id': client.pk}
    )

    context = {
        'form': client_form,
        'model_name_plural': Client._meta.verbose_name_plural,
        'model_name': Client._meta.verbose_name,
        'indefinite_article': 'a',
        'cancel_url': cancel_url
    }

    return render(request, 'utils/generics/update.html', context)


@login_required
def editDependentsView(request, client_id, dependent_id):
    has_edit = tt_groups.check_groups(request.user, 'Edit')
    if not has_edit:
        return redirect('/')

    context = {}

    try:
        client = Client.objects.get(id=client_id)
    except Client.DoesNotExist:
        raise http.Http404("No Client matches that ID")
    try:
        dependent = client.dependent_set.get(id=dependent_id)
    except Dependent.DoesNotExist:
        raise http.Http404("No Dependent matches that ID")

    if request.method == 'POST':
        dependent_form = DependentForm(request.POST, instance=dependent)
        if dependent_form.is_valid():
            dependent = dependent_form.save(commit=False)
            dependent.primary_id = client_id
            dependent.save()

            return redirect('client', client_id)

    else:
        dependent_form = DependentForm(instance=dependent)

    cancel_url = urlresolvers.reverse(
        'client', kwargs={'client_id': client.pk}
    )

    context = {
        'form': dependent_form,
        'model_name_plural': Dependent._meta.verbose_name_plural,
        'model_name': Dependent._meta.verbose_name,
        'indefinite_article': 'a',
        'cancel_url': cancel_url
    }

    return render(request, 'utils/generics/update.html', context)


@login_required
def add_new_dependent(request, client_id):
    has_edit = tt_groups.check_groups(request.user, 'Edit')
    if not has_edit:
        return redirect('/')

    context = {}

    try:
        client = Client.objects.get(id=client_id)
    except Client.DoesNotExist:
        raise http.Http404("No Client matches that ID")

    if request.method == 'POST':
        form = DependentForm(request.POST)

        if form.is_valid():
            saved = form.save(commit=False)
            saved.primary_id = client_id
            saved.save()

            return redirect('client', client_id)
    else:
        form = DependentForm()

    cancel_url = urlresolvers.reverse(
        'client', kwargs={'client_id': client.pk}
    )

    context = {
        'form': form,
        'model_name_plural': Dependent._meta.verbose_name_plural,
        'model_name': Dependent._meta.verbose_name,
        'indefinite_article': 'a',
        'cancel_url': cancel_url
    }

    return render(request, 'utils/generics/create.html', context)


@login_required
def add_dependent(request, client_id):
    has_edit = tt_groups.check_groups(request.user, 'Edit')
    if not has_edit:
        return redirect('/')

    context = {}

    if request.method == 'POST':
        if request.POST['submit'] == "Skip step":
            return redirect('insurance_create', client_id=client_id)

        form = DependentForm(request.POST)

        if form.is_valid():
            saved = form.save(commit=False)
            saved.primary_id = client_id
            saved.save()

            if request.POST['submit'] == "Create and proceed":
                # This means we want to add insurance
                return redirect('insurance_create', client_id=client_id)
            else:
                # This means we want to add another
                form = DependentForm()
    else:
        # TODO need to create a formset here instead of a form
        form = DependentForm()

    cancel_url = urlresolvers.reverse(
        'client', kwargs={'client_id': client_id}
    )

    create_and_proceed = ('<input class="btn btn-default" type="submit" '
                          'name="submit" value="Create and proceed" />')
    skip_step = ('<input class="btn btn-default" type="submit" '
                 'name="submit" value="Skip step" />')
    multistep_buttons = safestring.mark_safe(
        "{0} {1}".format(create_and_proceed, skip_step)
    )

    context = {
        'form': form,
        'model_name_plural': Dependent._meta.verbose_name_plural,
        'model_name': Dependent._meta.verbose_name,
        'indefinite_article': 'a',
        'cancel_url': cancel_url,
        'multistep_buttons': multistep_buttons
    }

    return render(request, 'utils/generics/create.html', context)
