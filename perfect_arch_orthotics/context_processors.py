from django.conf import settings


def site(request):
    resp = {
        'settings': settings,
    }

    return resp
