from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required
from django.views.generic import base

from inventory.views import views
from inventory.views import shoe
from inventory.views import order


adjustment_order_patterns = patterns(
    '',
    url(r'^$',
        base.RedirectView.as_view(pattern_name='order_list', permanent=False),
        name='adjustment_order_list'),
    url(r'^create/$',
        login_required(order.AdjustmentCreateOrderView.as_view()),
        name='adjustment_order_create'),
    url(r'^create/(?P<person_pk>\d+)/$',
        login_required(order.AdjustmentCreateOrderView.as_view()),
        name='adjustment_order_person_create'),
    url(r'^(?P<pk>\d+)/$',
        login_required(order.AdjustmentDetailOrderView.as_view()),
        name='adjustment_order_detail'),
    url(r'^update/(?P<pk>\d+)/$',
        login_required(order.AdjustmentUpdateOrderView.as_view()),
        name='adjustment_order_update'),
    url(r'^delete/(?P<pk>\d+)/$',
        login_required(order.AdjustmentDeleteOrderView.as_view()),
        name='adjustment_order_delete'),
)


shoe_order_patterns = patterns(
    '',
    url(r'^$',
        base.RedirectView.as_view(pattern_name='order_list', permanent=False),
        name='shoe_order_list'),
    url(r'^create/$',
        login_required(order.ShoeCreateOrderView.as_view()),
        name='shoe_order_create'),
    url(r'^create/(?P<person_pk>\d+)/$',
        login_required(order.ShoeCreateOrderView.as_view()),
        name='shoe_order_person_create'),
    url(r'^(?P<pk>\d+)/$',
        login_required(order.ShoeDetailOrderView.as_view()),
        name='shoe_order_detail'),
    url(r'^update/(?P<pk>\d+)/$',
        login_required(order.ShoeUpdateOrderView.as_view()),
        name='shoe_order_update'),
    url(r'^delete/(?P<pk>\d+)/$',
        login_required(order.ShoeDeleteOrderView.as_view()),
        name='shoe_order_delete'),
)


coverage_order_patterns = patterns(
    '',
    url(r'^$',
        base.RedirectView.as_view(pattern_name='order_list', permanent=False),
        name='coverage_order_list'),
    url(r'^create/$',
        login_required(order.CoverageCreateOrderView.as_view()),
        name='coverage_order_create'),
    url(r'^create/(?P<person_pk>\d+)/$',
        login_required(order.CoverageCreateOrderView.as_view()),
        name='coverage_order_person_create'),
    url(r'^(?P<pk>\d+)/$',
        login_required(order.CoverageDetailOrderView.as_view()),
        name='coverage_order_detail'),
    url(r'^update/(?P<pk>\d+)/$',
        login_required(order.CoverageUpdateOrderView.as_view()),
        name='coverage_order_update'),
    url(r'^delete/(?P<pk>\d+)/$',
        login_required(order.CoverageDeleteOrderView.as_view()),
        name='coverage_order_delete'),
)


order_patterns = patterns(
    '',
    url(r'^$',
        login_required(order.ListOrderView.as_view()),
        name='order_list'),
    url(r'^(?P<pk>\d+)/$',
        login_required(views.order_detail),
        name='order_detail'),
    url(r'^update/(?P<pk>\d+)/$',
        login_required(views.order_update),
        name='order_update'),
    url(r'^delete/(?P<pk>\d+)/$',
        login_required(views.order_delete),
        name='order_delete'),
    url(r'^shoe/', include(shoe_order_patterns)),
    url(r'^coverage/', include(coverage_order_patterns)),
    url(r'^adjustment/', include(adjustment_order_patterns)),
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
    url(r'^$',
        login_required(views.index),
        name='inventory_index'),
    url(r'^shoe/', include(shoe_patterns)),
    url(r'^order/', include(order_patterns)),
)
