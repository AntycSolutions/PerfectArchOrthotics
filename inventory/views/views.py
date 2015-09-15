from django import http
from django.core import urlresolvers

from inventory import models


def order_detail(request, pk):
    return http.HttpResponseRedirect(
        models.Order.objects.get(pk=pk).get_absolute_url()
    )


def order_update(request, pk):
    try:
        order = models.ShoeOrder.objects.get(pk=pk)
        return http.HttpResponseRedirect(
            urlresolvers.reverse('shoe_order_update',
                                 kwargs={'pk': order.pk})
        )
    except models.ShoeOrder.DoesNotExist:
        pass
    try:
        order = models.CoverageOrder.objects.get(pk=pk)
        return http.HttpResponseRedirect(
            urlresolvers.reverse('coverage_order_update',
                                 kwargs={'pk': order.pk})
        )
    except models.CoverageOrder.DoesNotExist:
        pass
    try:
        order = models.AdjustmentOrder.objects.get(pk=pk)
        return http.HttpResponseRedirect(
            urlresolvers.reverse('adjustment_order_update',
                                 kwargs={'pk': order.pk})
        )
    except models.AdjustmentOrder.DoesNotExist:
        pass

    raise Exception('Order is not a Shoe Order, Coverage Order, nor'
                    ' Adjustment Order.')


def order_delete(request, pk):
    try:
        order = models.ShoeOrder.objects.get(pk=pk)
        return http.HttpResponseRedirect(
            urlresolvers.reverse('shoe_order_delete',
                                 kwargs={'pk': order.pk})
        )
    except models.ShoeOrder.DoesNotExist:
        pass
    try:
        order = models.CoverageOrder.objects.get(pk=pk)
        return http.HttpResponseRedirect(
            urlresolvers.reverse('coverage_order_delete',
                                 kwargs={'pk': order.pk})
        )
    except models.CoverageOrder.DoesNotExist:
        pass
    try:
        order = models.AdjustmentOrder.objects.get(pk=pk)
        return http.HttpResponseRedirect(
            urlresolvers.reverse('adjustment_order_delete',
                                 kwargs={'pk': order.pk})
        )
    except models.AdjustmentOrder.DoesNotExist:
        pass

    raise Exception('Order is not a Shoe Order, Coverage Order, nor'
                    ' Adjustment Order.')
