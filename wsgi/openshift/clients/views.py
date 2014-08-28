from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from clients.models import Client, Dependent, Claim, Insurance
from clients.forms import ClientForm

def index(request):
    context = RequestContext(request)

    client_list = Client.objects.all()
    client_dict = {'clients': client_list}

    return render_to_response('clients/index.html', client_dict, context)


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
    print context_dict
    return render_to_response('clients/client.html', context_dict, context)


def add_client(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = ClientForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            client_list = Client.objects.all()
            client_dict = {'clients': client_list}
            return render_to_response('clients/index.html', client_dict, context)
        else:
            print form.errors
    else:
        form = ClientForm()

    return render_to_response('clients/add_client.html', {'form':form}, context)


def claimsView(request):
    context = RequestContext(request)

    claims = Claim.objects.all()

    context_dict = {'claims': claims}
    return render_to_response('clients/claims.html', context_dict, context)


def coverageView(request):
    context = RequestContext(request)

    insurance = Insurance.objects.all()

    context_dict = {'insurances': insurance}
    return render_to_response('clients/coverage.html', context_dict, context)


def insuranceView(request):
    context = RequestContext(request)

    insurance = Insurance.objects.all()

    context_dict = {'insurances': insurance}
    return render_to_response('clients/insurance.html', context_dict, context)
