from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib.auth import views as django_views
from django.contrib.auth.decorators import login_required
from django.views.generic import base

from ajax_select import urls as ajax_select_urls

from utils import views as utils_views
from utils.forms import forms as utils_forms

import views

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns(
    '',  # Tells django to view the rest as str
    url(r'^$',
        views.index,
        name='index'),
    url(r'^login/',
        django_views.login,
        {
            'template_name': 'login.html',
            'authentication_form': utils_forms.AuthenticationForm,
        },
        name='user_login'),
    url(r'^logout/',
        views.user_logout,
        name='user_logout'),
    url(r'^admin/lookups/', include(ajax_select_urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^clients/', include('clients.urls')),
    url(r'^inventory/', include('inventory.urls')),
    url(r'^thumbnail/(?P<width>\d+)/(?P<height>\d+)/(?P<url>.+)/$',
        login_required(utils_views.get_thumbnail),
        name='get_thumbnail'),
    url(r'^404/',
        base.TemplateView.as_view(template_name='404.html'),
        name='404'),
    url(r'^500/',
        base.TemplateView.as_view(template_name='500.html'),
        name='500')
)

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
