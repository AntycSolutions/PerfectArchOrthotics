from django.conf.urls import patterns, include, url

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
    url(r'^admin/', include(admin.site.urls)),
    url(r'^clients/', include('clients.urls')),
    url(r'^inventory/', include('inventory.urls')),
)
