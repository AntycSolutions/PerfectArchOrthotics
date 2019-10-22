import csv

from django import http
from django.db import models as db_models
from django.shortcuts import render

from inventory import models as inventory_models
from perfect_arch_orthotics import utils


def index(request):
    context = {'lazy': True}

    return render(request, 'index.html', context)


def inventory_csv(request):
    '''
        Restore backup from May 1, <year> to snapshot.perfectarch.ca

        Comment out auditlog tracking

        Load this view

        To get the total in-stock and total cost, run the following in shell:

        from inventory import models
        shoes=models.Shoe.objects.prefetch_related('shoeattributes_set')
        cost = 0
        quantity_total = 0
        for shoe in shoes:
            quantity = 0
            for shoe_attribute in shoe.shoeattributes_set.all():
                quantity += (
                    shoe_attribute.quantity -
                    shoe_attribute.dispensed() +
                    shoe_attribute.returned()
                )
            quantity_total += quantity
            cost += quantity * shoe.cost
    '''

    # Create the HttpResponse object with the appropriate CSV header.
    response = http.HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inventory.csv"'

    writer = csv.writer(response)

    max_pairs = inventory_models.Shoe.objects.annotate(
        db_models.Count('shoeattributes')
    ).aggregate(
        db_models.Max('shoeattributes__count')
    )['shoeattributes__count__max']

    pairs = []
    for i in range(max_pairs):
        pairs += ['Size', 'Quantity']

    # headers
    writer.writerow([
        'Category',
        'Availability',
        'Brand',
        'Style',
        'Name',
        'SKU',
        'Colour',
        'Description',
        'Credit Value',
        'Cost',
    ] + pairs)

    shoes = inventory_models.Shoe.objects.prefetch_related(
        'shoeattributes_set'
    )
    for shoe in shoes:
        shoe_attributes = []
        for shoe_attribute in shoe.shoeattributes_set.all():
            quantity = (
                shoe_attribute.quantity -
                shoe_attribute.dispensed() +
                shoe_attribute.returned()
            )
            shoe_attributes += [shoe_attribute.size, quantity]

        writer.writerow([
            shoe.get_category_display(),
            shoe.get_availability_display(),
            shoe.brand,
            shoe.style,
            shoe.name,
            shoe.sku,
            shoe.colour,
            shoe.description,
            shoe.credit_value,
            '${}'.format(shoe.cost),
        ] + shoe_attributes)

    return response


def git_commit(request):
    branch, commit_hash = utils.get_git_info()

    return http.JsonResponse({'branch': branch, 'commit': commit_hash})
