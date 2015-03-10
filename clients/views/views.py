# Python
import os
import io
import collections
from cgi import escape

# Django
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.template.loader import get_template
from django.template import Context

# xhtml2pdf
import xhtml2pdf.pisa as pisa

# PerfectArchOrthotics
from utils.search import get_query, get_date_query
from clients.models import Client, Dependent, Claim, Insurance, \
    Item, Coverage, ClaimItem, ClaimCoverage
from clients.forms.forms import ClientForm, DependentForm, \
    ClaimForm, nestedformset_factory


#TODO: split into multiple views

# Convert HTML URIs to absolute system paths
#  so xhtml2pdf can access those resources
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
    #                         link_callback=link_callback
    #                         )
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")),
                            result,
                            link_callback=link_callback
                            )
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

    #file = open(os.join(settings.MEDIA_ROOT, 'test.pdf'), "w+b")
    #pisaStatus = pisa.CreatePDF(html, dest=file, link_callback=link_callback)


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
        invoice = claim.invoice_set.all()[0]
    except:
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
        insurance_letter = claim.insuranceletter_set.all()[0]
    except:
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
        proof_of_manufacturing = claim.proofofmanufacturing_set.all()[0]
    except:
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
def clients(request):
    context = RequestContext(request)

    client_list = Client.objects.order_by('-id')

    page = request.GET.get('page')
    clients_rows_per_page = _get_paginate_by(request, 'clients_rows_per_page')
    clients = _paginate(client_list, page, clients_rows_per_page)

    client_dict = {'clients': clients,
                   'clients_rows_per_page': clients_rows_per_page,
                   }

    return render_to_response('clients/clients.html', client_dict, context)


@login_required
def claimsView(request):
    context = RequestContext(request)

    claim_list = Claim.objects.order_by('-submitted_datetime')

    claims_total_amount_claimed = 0
    claims_total_expected_back = 0
    for claim in claim_list:
        claims_total_amount_claimed += (
            claim.total_amount_quantity_claimed().total_amount_claimed
        )
        claims_total_expected_back += claim.total_expected_back()

    page = request.GET.get('page')
    claims_rows_per_page = _get_paginate_by(request, 'claims_rows_per_page')
    claims = _paginate(claim_list, page, claims_rows_per_page)

    context_dict = {'claims': claims,
                    'claims_total_amount_claimed': claims_total_amount_claimed,
                    'claims_total_expected_back': claims_total_expected_back,
                    'claims_rows_per_page': claims_rows_per_page,
                    }

    return render_to_response('clients/claims.html', context_dict, context)


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
def insuranceView(request):
    context = RequestContext(request)

    insurance_list = Insurance.objects.all()

    page = request.GET.get('page')
    insurances_rows_per_page = _get_paginate_by(request,
                                                'insurances_rows_per_page')
    insurances = _paginate(insurance_list, page, insurances_rows_per_page)

    context_dict = {'insurances': insurances,
                    'insurances_rows_per_page': insurances_rows_per_page,
                    }

    return render_to_response('clients/insurances.html', context_dict, context)


@login_required
def clientSearchView(request):
    context = RequestContext(request)
    context_dict = {}
    query_string = request.GET['q']
    fields = ['first_name', 'last_name', 'address', 'phone_number', 'employer',
              'health_care_number']
    clients = None
    if ('q' in request.GET) and request.GET['q'].strip():
        page = request.GET.get('page')
        query_string = request.GET['q']
        client_query = get_query(query_string, fields)
        found_clients = Client.objects.filter(client_query)

        clients_rows_per_page = _get_paginate_by(request,
                                                 'clients_rows_per_page')
        clients = _paginate(found_clients, page, clients_rows_per_page)

        context_dict = {'q': query_string,
                        'clients': clients,
                        'clients_rows_per_page': clients_rows_per_page,
                        }

    return render_to_response('clients/clients.html',
                              context_dict,
                              context)


@login_required
def claimSearchView(request):
    context = RequestContext(request)
    context_dict = {}

    claims = None
    # Start from all, drilldown to q df dt
    found_claims = Claim.objects.all().order_by('-submitted_datetime')

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

    if (('df' in request.GET) and request.GET['df'].strip()
            and ('dt' in request.GET) and request.GET['dt'].strip()):
        date_fields = ['submitted_datetime', 'insurance_paid_date']
        query_date_from_string = request.GET['df']
        query_date_to_string = request.GET['dt']
        context_dict['df'] = query_date_from_string
        context_dict['dt'] = query_date_to_string
        claim_query = get_date_query(query_date_from_string,
                                     query_date_to_string, date_fields)
        if found_claims:
            found_claims = found_claims.filter(claim_query)
        else:
            found_claims = Claim.objects.filter(claim_query)
    elif ('df' in request.GET) and request.GET['df'].strip():
        date_fields = ['submitted_datetime', 'insurance_paid_date']
        query_date_from_string = request.GET['df']
        context_dict['df'] = query_date_from_string
        claim_query = get_date_query(query_date_from_string,
                                     None, date_fields)
        if found_claims:
            found_claims = found_claims.filter(claim_query)
        else:
            found_claims = Claim.objects.filter(claim_query)
    elif ('dt' in request.GET) and request.GET['dt'].strip():
        date_fields = ['submitted_datetime', 'insurance_paid_date']
        query_date_to_string = request.GET['dt']
        context_dict['dt'] = query_date_to_string
        claim_query = get_date_query(None,
                                     query_date_to_string, date_fields)
        if found_claims:
            found_claims = found_claims.filter(claim_query)
        else:
            found_claims = Claim.objects.filter(claim_query)

    claims_total_amount_claimed = 0
    claims_total_expected_back = 0
    for claim in found_claims:
        claims_total_amount_claimed += (
            claim.total_amount_quantity_claimed().total_amount_claimed
        )
        claims_total_expected_back += claim.total_expected_back()

    page = request.GET.get('page')
    claims_rows_per_page = _get_paginate_by(request, 'claims_rows_per_page')
    claims = _paginate(found_claims, page, claims_rows_per_page)

    context_dict['claims'] = claims
    context_dict['claims_rows_per_page'] = claims_rows_per_page
    context_dict['claims_total_amount_claimed'] = claims_total_amount_claimed
    context_dict['claims_total_expected_back'] = claims_total_expected_back

    return render_to_response('clients/claims.html',
                              context_dict,
                              context)


@login_required
def insuranceSearchView(request):
    context = RequestContext(request)
    context_dict = {}
    query_string = request.GET['q']
    fields = ["provider", "policy_number",
              "main_claimant__first_name", "main_claimant__last_name",
              "main_claimant__employer"]
    insurances = None
    if ('q' in request.GET) and request.GET['q'].strip():
        page = request.GET.get('page')
        query_string = request.GET['q']
        insurance_query = get_query(query_string, fields)
        found_insurances = Insurance.objects.filter(insurance_query)

        insurances_rows_per_page = _get_paginate_by(request,
                                                    'insurances_rows_per_page')
        insurances = _paginate(found_insurances, page,
                               insurances_rows_per_page)

        context_dict = {'q': query_string,
                        'insurances': insurances,
                        'insurances_rows_per_page': insurances_rows_per_page,
                        }

    return render_to_response('clients/insurances.html',
                              context_dict,
                              context)


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

    client = Client.objects.get(id=client_id)
    insurance = client.insurance_set.all()
    dependents = client.dependent_set.all()
    claims = client.claim_set.all()

    orders = []
    if client.order_set.all():
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
        if dependent.order_set.all():
            orders.append(_order_info(dependent, request))

    client_total_amount_claimed = 0
    client_total_expected_back = 0
    for claim in claims:
        client_total_amount_claimed += (
            claim.total_amount_quantity_claimed().total_amount_claimed
        )
        client_total_expected_back += claim.total_expected_back()

    # Paginate Claims
    page = request.GET.get('claims_page')
    paginator = Paginator(claims.order_by('-submitted_datetime'), 5)
    try:
        claims = paginator.page(page)
    except PageNotAnInteger:
        claims = paginator.page(1)
    except EmptyPage:
        claims = paginator.page(paginator.num_pages)

    context_dict = {'client': client,
                    'client_insurance': insurance,
                    'client_claims': claims,
                    'client_total_amount_claimed': client_total_amount_claimed,
                    'client_total_expected_back': client_total_expected_back,
                    'orders': orders,
                    'spouse': spouse,
                    'children': children,
                    'dependent_class': Dependent}
    return render_to_response('clients/client.html', context_dict, context)


def _get_paginate_by(request, rows_per_page):
    paginate_by = 5
    if request.session.get(rows_per_page, False):
        paginate_by = request.session[rows_per_page]
    if (rows_per_page in request.GET
            and request.GET[rows_per_page].strip()):
        paginate_by = request.GET[rows_per_page]
        request.session[rows_per_page] = paginate_by
    return paginate_by


def _order_info(person, request):
    OrderInfo = collections.namedtuple(
        'OrderInfo', ['person_pk', 'name', 'order_set', 'rows_per_page']
    )

    rows_per_page = _get_paginate_by(request, '%s_rows_per_page' % person.pk)
    page = request.GET.get('%s_page' % person.pk)

    return OrderInfo(
        person.pk,
        person.full_name(),
        _paginate(
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
            page,
            rows_per_page),
        rows_per_page
    )


def _paginate(queryset, page, rows_per_page):
    paginator = Paginator(queryset, rows_per_page)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    return queryset


@login_required
def add_client(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = ClientForm(request.POST)

        if form.is_valid():
            saved = form.save(commit=True)

            form = DependentForm()
            return redirect('add_dependent', saved.id)
            #return render_to_response('clients/add_dependent.html',
                                       # {'form': form}, context)
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

    return render_to_response('clients/add_client.html',
                              {'form': form}, context)


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

    return render_to_response('clients/edit_client.html',
                              {'client': client,
                               'client_form': client_form},
                              context)


# @login_required
# def makeClaimView(request, client_id):
#     context = RequestContext(request)

#     client = Client.objects.get(id=client_id)
#     claim_form = ClaimForm(client)
#     ClaimCoverageFormFormSet = nestedformset_factory(
#         Claim, ClaimCoverage, ClaimItem,
#         extra=1, exclude=('items',),  # formset=CoverageFormSet,
#         nested_extra=1, nested_fields='__all__')

#     nestedformset = ClaimCoverageFormFormSet()
#     nestedformset.form.base_fields[
#         'coverage'].queryset = Coverage.objects.filter(
#             insurance__in=client.insurance_set.all())
#     nestedformset.form.base_fields[
#         'coverage'].label_from_instance = (
#             lambda obj:
#                 "%s - %s" % (obj.get_coverage_type_display(),
#                              obj.claimant.full_name())
#         )

#     if request.method == 'POST':
#         claim_form = ClaimForm(client, request.POST)
#         nestedformset = ClaimCoverageFormFormSet(request.POST)
#         if (claim_form.is_valid()
#                 and nestedformset.is_valid()):
#             claim = claim_form.save()
#             object_tuples = nestedformset.save(commit=False)
#             for claim_coverage, claim_items in object_tuples:
#                 if claim_coverage:
#                     claim_coverage.claim = claim
#                     claim_coverage.save()
#                     for claim_item in claim_items:
#                         claim_item.claim_coverage = claim_coverage
#                         claim_item.save()

#             return redirect('claim', client.id, claim.id)

#     return render_to_response('clients/make_claim.html',
#                               {'client': client,
#                                'claim_form': claim_form,
#                                'nestedformset': nestedformset,
#                                },
#                               context)


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

    return render_to_response('clients/dependent/edit_dependent.html',
                              {'client': client,
                               'dependent_form': dependent_form},
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

    return render_to_response('clients/dependent/add_new_dependent.html',
                              {'form': form,
                               'client': client},
                              context)


@login_required
def deleteDependentsView(request, client_id, dependent_id):
    # context = RequestContext(request)

    client = Client.objects.get(id=client_id)
    dependent = client.dependent_set.get(id=dependent_id)
    dependent.delete()
    return redirect('client', client_id)


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

    return render_to_response('clients/dependent/add_dependent.html',
                              {'form': form}, context)
