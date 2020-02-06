from django.conf import settings


def site(request):
    resp = {
        'settings': settings,
        'groups': {
            'All': 'All',
            'Reminders': 'Reminders',
            'Clients': 'Clients',
            'Claims': 'Claims',
            'Insurances': 'Insurances',
            'Items': 'Items',
            'Inventory': 'Inventory',
            'Orders': 'Orders',
            'Statistics': 'Statistics',
            'Notes': 'Notes',
            'Referrals': 'Referrals',
            'Insurance_Info': 'Insurance_Info',
            'Shoe_Info': 'Shoe_Info',
        },
    }

    return resp
