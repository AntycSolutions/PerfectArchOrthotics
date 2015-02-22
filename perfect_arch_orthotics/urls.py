from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from ajax_select import urls as ajax_select_urls

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns(
    '',  # Tells django to view the rest as str
    url(r'^$', 'views.index', name='index'),
    url(r'^login/',
        'django.contrib.auth.views.login',
        {'template_name': 'login.html'},
        name='user_login'),
    url(r'^logout/', 'views.user_logout', name='user_logout'),
    url(r'^admin/lookups/', include(ajax_select_urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^clients/', include('clients.urls')),
    url(r'^inventory/', include('inventory.urls')),
    url(r'^utils/', include('utils.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
