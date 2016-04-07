# Python
import os
import io
import collections
import itertools
from cgi import escape

# Django
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django import http
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.template.loader import get_template
from django.template import Context
from django.contrib import messages
from django.db.models import Sum, Case, When, Q
from django.core import urlresolvers
from django.utils import safestring

# xhtml2pdf
import xhtml2pdf.pisa as pisa

# PerfectArchOrthotics
from utils.search import get_query, get_date_query
from utils import views_utils
from clients.models import Client, Dependent, Claim, Insurance, \
    Item, Coverage, ClaimItem, ClaimCoverage
from clients import models as clients_models
from inventory import models as inventory_models
from clients.forms.forms import ClientForm, DependentForm
from clients.forms import forms as clients_forms


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
        return path
    elif os.path.isfile(path2):
        return os.path.normpath(path2)
    else:
        raise Exception('media URI must start with %s or %s' %
                        (sUrl, mUrl))


@login_required
def render_to_pdf(request, template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    result = io.BytesIO()

    # 'utf-8' didn't work
    # pdf = pisa.pisaDocument(io.BytesIO("Test".encode("ISO-8859-1")),
    #                         result,
    #                         link_callback=link_callback)
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")),
                            result,
                            link_callback=link_callback)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')

    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))


def invoice_view(request, claim_id):
    claim, patient, invoice, invoice_number = _invoice(claim_id)
    bill_to = settings.BILL_TO[0][1]
    perfect_arch_name = bill_to.split('\n')[0]
    perfect_arch_address = bill_to.replace(perfect_arch_name + '\n', '')

    return render_to_pdf(request,
                         'clients/pdfs/invoice.html',
                         {'pagesize': 'A4',
                          'claim': claim,
                          'invoice': invoice,
                          'invoice_number': invoice_number,
                          'perfect_arch_name': perfect_arch_name,
                          'perfect_arch_address': perfect_arch_address,
                          'item_class': Item,
                          'claim_item_class': ClaimItem,
                          # 'insurance_class': Insurance,
                          'is_prod': request.get_host() == "perfectarch.ca"}
                         )


def _invoice(claim_id):
    claim = Claim.objects.get(id=claim_id)
    patient = claim.patient
    invoice = None
    try:
        invoice = claim.invoice
    except clients_models.Invoice.DoesNotExist:
        pass
    invoice_number = "{0:04d}".format(claim.id)

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

    return render_to_pdf(request,
                         'clients/pdfs/insurance_letter.html',
                         {'pagesize': 'A4',
                          'claim': claim,
                          'patient': patient,
                          'insurance_letter': insurance_letter,
                          'underline': underline,
                          'notunderline': notunderline})


def _insurance_letter(claim_id):
    claim = Claim.objects.get(id=claim_id)
    patient = claim.patient
    insurance_letter = None
    try:
        insurance_letter = claim.insuranceletter
    except clients_models.InsuranceLetter.DoesNotExist:
        pass

    return claim, patient, insurance_letter


def proof_of_manufacturing_view(request, claim_id):
    claim, proof_of_manufacturing, invoice_number = _proof_of_manufacturing(
        claim_id)

    return render_to_pdf(request,
                         'clients/pdfs/proof_of_manufacturing.html',
                         {'pagesize': 'A4',
                          'claim': claim,
                          'proof_of_manufacturing': proof_of_manufacturing,
                          'invoice_number': invoice_number})


def _proof_of_manufacturing(claim_id):
    claim = Claim.objects.get(id=claim_id)
    proof_of_manufacturing = None
    try:
        proof_of_manufacturing = claim.proofofmanufacturing
    except clients_models.ProofOfManufacturing.DoesNotExist:
        pass
    invoice_number = "{0:04d}".format(claim.id + 7500)

    return claim, proof_of_manufacturing, invoice_number


@login_required
def fillOutInvoiceView(request, claim_id):
    context = RequestContext(request)

    claim, patient, invoice, invoice_number = _invoice(claim_id)

    return render_to_response('clients/make_invoice.html',
                              {'patient': patient,
                               'claim': claim,
                               'invoice': invoice,
                               'insurance_class': Insurance,
                               'invoice_number': invoice_number},
                              context)


@login_required
def fillOutInsuranceLetterView(request, claim_id):
    context = RequestContext(request)

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

    return render_to_response('clients/make_insurance_letter.html',
                              {'patient': patient,
                               'claim': claim,
                               'insurance_letter': insurance_letter,
                               'underline': underline,
                               'notunderline': notunderline},
                              context)


@login_required
def fillOutProofOfManufacturingView(request, claim_id):
    context = RequestContext(request)

    claim, proof_of_manufacturing, invoice_number = _proof_of_manufacturing(
        claim_id)

    return render_to_response(
        'clients/make_proof_of_manufacturing.html',
        {'claim': claim,
         'proof_of_manufacturing': proof_of_manufacturing,
         'invoice_number': invoice_number},
        context)


@login_required
def claimView(request, claim_id):
    context = RequestContext(request)

    claim = Claim.objects.get(id=claim_id)
    has_orthotics = claim.coverages.filter(coverage_type="o").count() > 0
    context_dict = {'claim': claim,
                    'has_orthotics': has_orthotics,
                    'claim_coverage_class': ClaimCoverage,
                    'coverage_class': Coverage,
                    'claim_item_class': ClaimItem,
                    'item_class': Item
                    }
    return render_to_response('clients/claim.html', context_dict, context)


@login_required
def clientSearchView(request):
    context = RequestContext(request)
    context_dict = {}

    found_clients = Client.objects.order_by('-id')
    found_dependents = Dependent.objects.order_by('-id')
    if ('q' in request.GET) and request.GET['q'].strip():
        fields = ['first_name', 'last_name', 'address', 'phone_number',
                  'employer', 'health_care_number']
        query_string = request.GET['q']
        context_dict['q'] = query_string

        client_query = get_query(query_string, fields)
        found_clients = Client.objects.filter(client_query)

        fields = ['first_name', 'last_name',
                  'employer', 'health_care_number']
        query_string = request.GET['q']
        context_dict['q'] = query_string

        client_query = get_query(query_string, fields)
        found_dependents = Dependent.objects.filter(client_query)

    clients_rows_per_page = views_utils._get_paginate_by(
        request, 'clients_rows_per_page'
    )

    clients = views_utils._paginate(
        request,
        list(itertools.chain(found_clients, found_dependents)),
        'page',
        clients_rows_per_page
    )

    context_dict['clients'] = clients
    context_dict['clients_rows_per_page'] = clients_rows_per_page

    return render_to_response('clients/clients.html', context_dict, context)


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


def _date_from_date_to(request, context_dict, found_claims, df, dt,
                       date_field):
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


@login_required
def claimSearchView(request):
    context = RequestContext(request)
    context_dict = {}

    claims = None
    # Start from all, drilldown to q df dt
    found_claims = Claim.objects.select_related(
        'insurance'
    ).prefetch_related(
        'claimcoverage_set__claimitem_set__item'
    ).order_by(
        '-submitted_datetime'
    )

    # Query, Date From, Date To
    if ('q' in request.GET) and request.GET['q'].strip():
        fields = ['patient__first_name', 'patient__last_name',
                  'insurance__provider', 'patient__employer']
        query_string = request.GET['q']
        context_dict['q'] = query_string
        claim_query = get_query(query_string, fields)
        if found_claims:
            found_claims = found_claims.filter(claim_query)
        else:
            found_claims = Claim.objects.filter(claim_query)

    found_claims = _date_from_date_to(request, context_dict, found_claims,
                                      'apdf', 'apdt',
                                      'claimcoverage__actual_paid_date')

    found_claims = _date_from_date_to(request, context_dict, found_claims,
                                      'sdf', 'sdt', 'submitted_datetime')

    found_claims = _actual_paid_date(request, context_dict, found_claims)

    # Expected Back
    totals = ClaimCoverage.objects.filter(
        claim__in=found_claims,
    ).aggregate(
        non_assignment_expected_back=Sum(Case(
            When(
                claim__insurance__benefits='na',
                then='expected_back',
            ),
            default=0,
        )),
        assignment_expected_back=Sum(Case(
            When(
                Q(claim__insurance__benefits='a') &
                Q(actual_paid_date__isnull=False),
                then='expected_back',
            ),
            default=0,
        )),
        pending_assignment_expected_back=Sum(Case(
            When(
                Q(claim__insurance__benefits='a') &
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
        benefits = amount_claimed_claim.insurance.benefits

        for claimcoverage in amount_claimed_claim.claimcoverage_set.all():
            for claimitem in claimcoverage.claimitem_set.all():
                if benefits == Insurance.ASSIGNMENT:
                    assignment_amount_claimed += claimitem.unit_price_amount()
                elif benefits == Insurance.NON_ASSIGNMENT:
                    assignment_amount_claimed += claimitem.unit_price_amount()
                elif not benefits:
                    pass
                else:
                    raise Exception('Unknown Insurance benefits')

    claims_rows_per_page = views_utils._get_paginate_by(
        request, 'claims_rows_per_page'
    )
    claims = views_utils._paginate(request, found_claims, 'page',
                                   claims_rows_per_page)

    total_assignment_expected_back = \
        assignment_expected_back + pending_assignment_expected_back
    context_dict['claims'] = claims
    context_dict['claims_rows_per_page'] = claims_rows_per_page
    context_dict['assignment_amount_claimed'] = assignment_amount_claimed
    context_dict['non_assignment_amount_claimed'] = \
        non_assignment_amount_claimed
    context_dict['total_amount_claimed'] = \
        assignment_amount_claimed + non_assignment_amount_claimed
    context_dict['non_assignment_expected_back'] = non_assignment_expected_back
    context_dict['assignment_expected_back'] = assignment_expected_back
    context_dict['pending_assignment_expected_back'] = \
        pending_assignment_expected_back
    context_dict['total_assignment_expected_back'] = \
        total_assignment_expected_back
    context_dict['total_expected_back'] = \
        non_assignment_expected_back + total_assignment_expected_back

    return render_to_response(
        'clients/claims.html', context_dict, context
    )


@login_required
def insuranceSearchView(request):
    context = RequestContext(request)
    context_dict = {}

    found_insurances = Insurance.objects.all()
    if ('q' in request.GET) and request.GET['q'].strip():
        fields = ["provider", "policy_number",
                  "main_claimant__first_name", "main_claimant__last_name",
                  "main_claimant__employer"]
        query_string = request.GET['q']
        context_dict['q'] = query_string
        insurance_query = get_query(query_string, fields)
        found_insurances = Insurance.objects.filter(insurance_query)

    insurances_rows_per_page = views_utils._get_paginate_by(
        request, 'insurances_rows_per_page'
    )
    insurances = views_utils._paginate(request, found_insurances, 'page',
                                       insurances_rows_per_page)

    context_dict['insurances'] = insurances
    context_dict['insurances_rows_per_page'] = insurances_rows_per_page

    return render_to_response('clients/insurances.html', context_dict, context)


def getFieldsFromRequest(request, default=""):
    """This is not used currently, will maybe be used in the future."""
    if 'fields' in request.GET and request.GET['fields'].strip():
        querydict = dict(request.GET.iterlists())
        return querydict['fields']
    else:
        return [default]


@login_required
def clientView(request, client_id):
    context = RequestContext(request)

    client = Client.objects.prefetch_related(
        'insurance_set',
        'dependent_set',
        'claim_set__claimcoverage_set__claimitem_set__item'
    ).get(id=client_id)
    insurance = client.insurance_set.all()
    dependents = client.dependent_set.all()
    claims = client.claim_set.all()

    orders = []
    if client.order_set.exists():
        orders.append(_order_info(client, request))
    spouse = None
    children = []
    for dependent in dependents:
        if dependent.relationship == Dependent.SPOUSE:
            spouse = dependent
            insurance = insurance | spouse.insurance_set.all()
        else:
            children.append(dependent)
        claims = claims | dependent.claim_set.all()
        if dependent.order_set.exists():
            orders.append(_order_info(dependent, request))

    totals = ClaimCoverage.objects.filter(
        actual_paid_date__isnull=False,
        claim__in=claims,
    ).aggregate(
        expected_back__sum=Sum('expected_back'),
    )
    client_total_expected_back = totals['expected_back__sum'] or 0

    client_total_amount_claimed = 0
    client_total_cost = 0
    pending_client_total_amount_claimed = 0
    pending_client_total_cost = 0
    for claim in claims:
        for claimcoverage in claim.claimcoverage_set.all():
            for claimitem in claimcoverage.claimitem_set.all():
                amounts = claimitem.get_amount()
                if claimcoverage.actual_paid_date:
                    client_total_amount_claimed += amounts['unit_price']
                    client_total_cost += amounts['cost']
                else:
                    pending_client_total_amount_claimed += \
                        amounts['unit_price']
                    pending_client_total_cost += amounts['cost']

    totals = ClaimCoverage.objects.filter(
        actual_paid_date__isnull=True,
        claim__in=claims,
    ).aggregate(
        expected_back__sum=Sum('expected_back'),
    )
    pending_client_total_expected_back = totals['expected_back__sum'] or 0

    dependents_pks = list(dependents.values_list('pk', flat=True))
    pks = dependents_pks + [client.pk]
    total = inventory_models.ShoeOrder.objects.filter(
        claimant__pk__in=pks
    ).aggregate(
        shoe_order_cost=Sum('shoe_attributes__shoe__cost')
    )
    shoe_order_cost = total['shoe_order_cost'] or 0

    # Paginate Claims
    page = request.GET.get('claims_page')
    paginator = Paginator(claims.order_by('-submitted_datetime'), 5)
    try:
        claims = paginator.page(page)
    except PageNotAnInteger:
        claims = paginator.page(1)
    except EmptyPage:
        claims = paginator.page(paginator.num_pages)

    client_expected_back = (
        client_total_expected_back + pending_client_total_expected_back
    )
    client_cost = (
        client_total_cost + pending_client_total_cost + shoe_order_cost
    )

    if request.method == 'GET':
        try:
            referral_form = clients_forms.ReferralForm(client)
        except clients_forms.ReferralForm.EmptyClaimsQuerySet:
            referral_form = None

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
            note_form = clients_forms.NoteForm(request.POST)
            if note_form.is_valid():
                note = note_form.save(commit=False)
                note.client = client
                note.save()

        return http.HttpResponseRedirect(
            urlresolvers.reverse('client', args=[client_id])
        )

    context_dict = {
        'client': client,
        'client_insurance': insurance,
        'client_claims': claims,
        'client_total_amount_claimed': client_total_amount_claimed,
        'client_total_expected_back': client_total_expected_back,
        'pending_client_total_amount_claimed':
            pending_client_total_amount_claimed,
        'pending_client_total_expected_back':
            pending_client_total_expected_back,
        'client_expected_back': client_expected_back,
        'client_cost': client_cost,
        'margin': client_expected_back - client_cost,
        'orders': orders,
        'spouse': spouse,
        'children': children,
        'dependent_class': Dependent,
        'referral_form': referral_form,
        'note_form': note_form,
    }

    return render_to_response('clients/client.html', context_dict, context)


def _order_info(person, request):
    OrderInfo = collections.namedtuple(
        'OrderInfo', ['person_pk', 'name', 'order_set', 'rows_per_page']
    )

    rows_per_page = views_utils._get_paginate_by(
        request, '%s_rows_per_page' % person.pk
    )

    return OrderInfo(
        person.pk,
        person.full_name(),
        views_utils._paginate(
            request,
            person.order_set.all().extra(
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
            ),
            '%s_page' % person.pk,
            rows_per_page),
        rows_per_page
    )


@login_required
def add_client(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = ClientForm(request.POST)

        if form.is_valid():
            saved = form.save(commit=True)

            form = DependentForm()
            return redirect('add_dependent', saved.id)
    else:
        form = ClientForm()
        queryset = form.fields['referred_by'].queryset
        queryset = queryset.extra(
            select={
                'lower_first_name': 'lower(first_name)'
                }).order_by('lower_first_name')
        form.fields['referred_by'].queryset = queryset
        form.fields['referred_by'].label_from_instance = (
            lambda obj:
                "%s" % (obj.full_name())
        )

    cancel_url = urlresolvers.reverse('client_list')

    return render_to_response(
        'utils/generics/create.html',
        {'form': form,
         'model_name_plural': Client._meta.verbose_name_plural,
         'model_name': Client._meta.verbose_name,
         'indefinite_article': 'a',
         'cancel_url': cancel_url},
        context)


@login_required
def editClientView(request, client_id):
    context = RequestContext(request)

    client = Client.objects.get(id=client_id)
    if request.method == 'POST':
        client_form = ClientForm(request.POST, instance=client)
        if client_form.is_valid():
            saved = client_form.save(commit=True)
            return redirect('client', saved.id)

    else:
        client_form = ClientForm(instance=client)
        queryset = client_form.fields['referred_by'].queryset
        queryset = queryset.extra(
            select={
                'lower_first_name': 'lower(first_name)'
                }).order_by('lower_first_name')
        client_form.fields['referred_by'].queryset = queryset
        client_form.fields['referred_by'].label_from_instance = (
            lambda obj:
                "%s" % (obj.full_name())
        )

    cancel_url = urlresolvers.reverse('client',
                                      kwargs={'client_id': client.pk})

    return render_to_response(
        'utils/generics/update.html',
        {'form': client_form,
         'model_name_plural': Client._meta.verbose_name_plural,
         'model_name': Client._meta.verbose_name,
         'indefinite_article': 'a',
         'cancel_url': cancel_url},
        context)


@login_required
def editDependentsView(request, client_id, dependent_id):
    context = RequestContext(request)

    client = Client.objects.get(id=client_id)
    dependent = client.dependent_set.get(id=dependent_id)
    if request.method == 'POST':
        dependent_form = DependentForm(request.POST, instance=dependent)
        if dependent_form.is_valid():
            saved = dependent_form.save(commit=False)
            saved.client = client
            saved.save()
            return redirect('client', client_id)

    else:
        dependent_form = DependentForm(instance=dependent)

    cancel_url = urlresolvers.reverse('client',
                                      kwargs={'client_id': client.pk})

    return render_to_response(
        'utils/generics/update.html',
        {'form': dependent_form,
         'model_name_plural': Dependent._meta.verbose_name_plural,
         'model_name': Dependent._meta.verbose_name,
         'indefinite_article': 'a',
         'cancel_url': cancel_url},
        context)


@login_required
def add_new_dependent(request, client_id):
    context = RequestContext(request)

    client = Client.objects.get(id=client_id)
    if request.method == 'POST':
        form = DependentForm(request.POST)

        if form.is_valid():
            saved = form.save(commit=False)

            client = Client.objects.get(id=client_id)
            saved.client = client
            saved.save()
            return redirect('client', client_id)
    else:
        form = DependentForm()

    cancel_url = urlresolvers.reverse('client',
                                      kwargs={'client_id': client.pk})

    return render_to_response(
        'utils/generics/create.html',
        {'form': form,
         'model_name_plural': Dependent._meta.verbose_name_plural,
         'model_name': Dependent._meta.verbose_name,
         'indefinite_article': 'a',
         'cancel_url': cancel_url},
        context)


@login_required
def add_dependent(request, client_id):
    context = RequestContext(request)

    if request.method == 'POST':
        if request.POST['submit'] == "Skip step":
            return redirect('insurance_create', client_id=client_id)

        form = DependentForm(request.POST)

        if form.is_valid():
            saved = form.save(commit=False)

            client = Client.objects.get(id=client_id)
            saved.client = client
            saved.save()

            if request.POST['submit'] == "Create and proceed":
                # This means we want to add insurance
                return redirect('insurance_create', client_id=client_id)
            else:
                # This means we want to add another
                form = DependentForm()
    else:
        # TODO need to create a formset here isntead of a form
        form = DependentForm()

    cancel_url = urlresolvers.reverse('client',
                                      kwargs={'client_id': client_id})

    create_and_proceed = ('<input class="btn btn-default" type="submit" '
                          'name="submit" value="Create and proceed" />')
    skip_step = ('<input class="btn btn-default" type="submit" '
                 'name="submit" value="Skip step" />')
    multistep_buttons = safestring.mark_safe(
        "{0} {1}".format(create_and_proceed, skip_step)
    )

    return render_to_response(
        'utils/generics/create.html',
        {'form': form,
         'model_name_plural': Dependent._meta.verbose_name_plural,
         'model_name': Dependent._meta.verbose_name,
         'indefinite_article': 'a',
         'cancel_url': cancel_url,
         'multistep_buttons': multistep_buttons},
        context)
