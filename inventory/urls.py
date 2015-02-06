from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required

from inventory.views import views
from inventory.views import shoe
from inventory.views import order


order_patterns = patterns(
    '',
    url(r'^$',
        login_required(order.ListOrderView.as_view()),
        name='order_list'),
    url(r'^(?P<pk>\d+)/$',
        login_required(order.DetailOrderView.as_view()),
        name='order_detail'),
    url(r'^update/(?P<pk>\d+)/$',
        login_required(order.UpdateOrderView.as_view()),
        name='order_update'),
    url(r'^delete/(?P<pk>\d+)/$',
        login_required(order.DeleteOrderView.as_view()),
        name='order_delete'),
    url(r'^create/$',
        login_required(order.CreateOrderView.as_view()),
        name='order_create'),
)


shoe_patterns = patterns(
    '',
    url(r'^$',
        login_required(shoe.ListShoeView.as_view()),
        name='shoe_list'),
    url(r'^(?P<pk>\d+)/$',
        login_required(shoe.DetailShoeView.as_view()),
        name='shoe_detail'),
    url(r'^update/(?P<pk>\d+)/$',
        login_required(shoe.UpdateShoeView.as_view()),
        name='shoe_update'),
    url(r'^delete/(?P<pk>\d+)/$',
        login_required(shoe.DeleteShoeView.as_view()),
        name='shoe_delete'),
    url(r'^create/$',
        login_required(shoe.CreateShoeView.as_view()),
        name='shoe_create'),
)

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='inventory_index'),
    url(r'^shoe/', include(shoe_patterns)),
    url(r'^order/', include(order_patterns)),
)
