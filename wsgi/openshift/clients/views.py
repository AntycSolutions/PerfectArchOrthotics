from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from clients.models import Client, Dependent, Claim, Insurance
from clients.forms import ClientForm, DependentForm, DependantFormSet
from search import get_query


@login_required
def index(request):
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

    return render_to_response('clients/index.html', client_dict, context)


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
    return render_to_response('clients/insurance.html', context_dict, context)


@login_required
def clientSearchView(request):
    context = RequestContext(request)
    context_dict = {}
    query_string = request.GET['q']
    fields = ['firstName', 'lastName', 'address', 'phoneNumber', 'employer', 'healthcareNumber']
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


    return render_to_response('clients/index.html',
                              context_dict,
                              context)

@login_required
def claimSearchView(request):
    context = RequestContext(request)
    context_dict = {}
    query_string = request.GET['q']
    fields = ['client__firstName', 'client__lastName', 'client__employer', 'insurance__provider']
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
    fields = ["client__employer", "provider", "policyNumber", "client__firstName", "client__lastName"]
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

    return render_to_response('clients/insurance.html',
                              context_dict,
                              context)

def getFieldsFromRequest(request, default=""):
    """This is not used currently, will maybe be used in the future."""
    if 'fields' in request.GET and request.GET['fields'].strip():
        print request.GET
        querydict = dict(request.GET.iterlists())
        print querydict
        print querydict['fields']
        return querydict['fields']
    else:
        return [default]

@login_required
def clientView(request, client_id):
    context = RequestContext(request)

    client = Client.objects.get(id=client_id)
    insurance = client.insurance_set.all()
    dependents = client.dependents.all()
    spouse = None
    children = []
    for dependent in dependents:
        if dependent.relationship == Dependent.SPOUSE:
            spouse = dependent
        else:
            children.append(dependent)

    context_dict = {'client': client,
                    'client_insurance': insurance,
                    'spouse': spouse,
                    'children': children}
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
            #return render_to_response('clients/add_dependent.html', {'form': form}, context)
    else:
        form = ClientForm()

    return render_to_response('clients/add_client.html', {'form': form}, context)


@login_required
def add_dependent(request, client_id):
    context = RequestContext(request)
    print request

    if request.method == 'POST':
        if request.POST['submit'] == "Skip step":
            return redirect('client_index')

        form = DependentForm(request.POST)

        if form.is_valid():
            saved = form.save(commit=True)

            client = Client.objects.get(id=client_id)
            client.dependents.add(saved)

            if request.POST['submit'] == "Create and proceed":
                # This means we want to add insurance
                return redirect('client_index')
            else:
                # This means we want to add another
                form = DependentForm()
    else:
        # TODO need to create a formset here isntead of a form
        form = DependentForm()

    return render_to_response('clients/add_dependent.html', {'form': form}, context)
