from django.conf import urls

from . import views


claimreminder_urls = [
    urls.url(
        r'^update/(?P<pk>\d+)/$',
        views.ClaimReminderUpdate.as_view(),
        name='claimreminder_update'
    ),
]

orderreminder_urls = [
    urls.url(
        r'^update/(?P<pk>\d+)/$',
        views.OrderReminderUpdate.as_view(),
        name='orderreminder_update'
    ),
]

api_urls = [
    urls.url(r'^claimreminder/', urls.include(claimreminder_urls)),
    urls.url(r'^orderreminder/', urls.include(orderreminder_urls)),
]

urlpatterns = [
    urls.url(r'^$', views.Reminders.as_view(), name='reminders'),
    urls.url(r'^api/', urls.include(api_urls)),
]
