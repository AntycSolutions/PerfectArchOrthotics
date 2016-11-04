from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.views.generic import base

from ajax_select import urls as ajax_select_urls

from accounts import urls as account_urls
from utils import views as utils_views

import views

from django.contrib import admin
admin.autodiscover()


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(
        r'^inventory_csv/$',
        login_required(views.inventory_csv),
        name='inventory_csv'
    ),

    url(r'^accounts/', include(account_urls, namespace='accounts')),
    url(r'^admin/lookups/', include(ajax_select_urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^clients/', include('clients.urls')),
    url(r'^inventory/', include('inventory.urls')),
    url(r'^', include('utils.urls')),
    url(r'^thumbnail/(?P<width>\d+)/(?P<height>\d+)/(?P<url>.+)/$',
        login_required(utils_views.get_thumbnail),
        name='get_thumbnail'),

    url(r'^404/$',
        base.TemplateView.as_view(template_name='404.html'),
        name='404'),
    url(r'^500/$',
        base.TemplateView.as_view(template_name='500.html'),
        name='500'),
    url(r'^raise_exception/$',
        utils_views.raise_exception,
        name='raise_exception')
]

urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
