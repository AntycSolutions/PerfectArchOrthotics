# Python
import os
import io
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
from search import get_query
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

    return render_to_response('clients/make_insurance_letter.html',
                              {'patient': patient,
                               'claim': claim,
                               'insurance_letter': insurance_letter},
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
    paginator = Paginator(client_list, 5)
    page = request.GET.get('page')
    try:
        clients = paginator.page(page)
    except PageNotAnInteger:
        clients = paginator.page(1)
    except EmptyPage:
        clients = paginator.page(paginator.num_pages)

    client_dict = {'clients': clients}

    return render_to_response('clients/clients.html', client_dict, context)


@login_required
def claimsView(request):
    context = RequestContext(request)

    # TODO: Change this order_by to be on time
    claim_list = Claim.objects.order_by('-id')
    paginator = Paginator(claim_list, 5)
    page = request.GET.get('page')
    try:
        claims = paginator.page(page)
    except PageNotAnInteger:
        claims = paginator.page(1)
    except EmptyPage:
        claims = paginator.page(paginator.num_pages)

    context_dict = {'claims': claims}
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
    paginator = Paginator(insurance_list, 5)
    page = request.GET.get('page')
    try:
        insurances = paginator.page(page)
    except PageNotAnInteger:
        insurances = paginator.page(1)
    except EmptyPage:
        insurances = paginator.page(paginator.num_pages)

    context_dict = {'insurances': insurances}
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
        context_dict['q'] = query_string
        client_query = get_query(query_string, fields)
        found_clients = Client.objects.filter(client_query)
        paginator = Paginator(found_clients, 5)
        try:
            clients = paginator.page(page)
        except PageNotAnInteger:
            clients = paginator.page(1)
        except EmptyPage:
            clients = paginator.page(paginator.num_pages)
        context_dict['clients'] = clients

    return render_to_response('clients/clients.html',
                              context_dict,
                              context)


@login_required
def claimSearchView(request):
    context = RequestContext(request)
    context_dict = {}
    query_string = request.GET['q']
    fields = ['patient__first_name', 'patient__last_name',
              'insurance__provider', 'patient__employer']
    claims = None
    if ('q' in request.GET) and request.GET['q'].strip():
        page = request.GET.get('page')
        query_string = request.GET['q']
        context_dict['q'] = query_string
        claim_query = get_query(query_string, fields)
        found_claims = Claim.objects.filter(claim_query)
        paginator = Paginator(found_claims, 5)
        try:
            claims = paginator.page(page)
        except PageNotAnInteger:
            claims = paginator.page(1)
        except EmptyPage:
            claims = paginator.page(paginator.num_pages)
        context_dict['claims'] = claims

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
        context_dict['q'] = query_string
        insurance_query = get_query(query_string, fields)
        found_insurances = Insurance.objects.filter(insurance_query)
        paginator = Paginator(found_insurances, 5)
        try:
            insurances = paginator.page(page)
        except PageNotAnInteger:
            insurances = paginator.page(1)
        except EmptyPage:
            insurances = paginator.page(paginator.num_pages)
        context_dict['insurances'] = insurances

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
    spouse = None
    children = []
    for dependent in dependents:
        if dependent.relationship == Dependent.SPOUSE:
            spouse = dependent
            insurance = insurance | spouse.insurance_set.all()
        else:
            children.append(dependent)
        claims = claims | dependent.claim_set.all()

    context_dict = {'client': client,
                    'client_insurance': insurance,
                    'client_claims': claims.order_by('-submitted_datetime'),
                    'spouse': spouse,
                    'children': children,
                    'dependent_class': Dependent}
    return render_to_response('clients/client.html', context_dict, context)


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
