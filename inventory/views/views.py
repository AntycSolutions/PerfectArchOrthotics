from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from inventory import models


def order_detail(request, pk):
    return HttpResponseRedirect(
        models.Order.objects.get(pk=pk).get_absolute_url()
    )


def order_update(request, pk):
    try:
        order = models.ShoeOrder.objects.get(pk=pk)
        return HttpResponseRedirect(reverse('shoe_order_update',
                                            kwargs={'pk': order.pk}))
    except:
        pass
    try:
        order = models.CoverageOrder.objects.get(pk=pk)
        return HttpResponseRedirect(reverse('coverage_order_update',
                                            kwargs={'pk': order.pk}))
    except:
        pass
    try:
        order = models.AdjustmentOrder.objects.get(pk=pk)
        return HttpResponseRedirect(reverse('adjustment_order_update',
                                            kwargs={'pk': order.pk}))
    except:
        pass


def order_delete(request, pk):
    try:
        order = models.ShoeOrder.objects.get(pk=pk)
        return HttpResponseRedirect(reverse('shoe_order_delete',
                                            kwargs={'pk': order.pk}))
    except:
        pass
    try:
        order = models.CoverageOrder.objects.get(pk=pk)
        return HttpResponseRedirect(reverse('coverage_order_delete',
                                            kwargs={'pk': order.pk}))
    except:
        pass
    try:
        order = models.AdjustmentOrder.objects.get(pk=pk)
        return HttpResponseRedirect(reverse('adjustment_order_delete',
                                            kwargs={'pk': order.pk}))
    except:
        pass
