from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import admin

from auditlog import models


def index(request):
    context = RequestContext(request)

    context['lazy'] = True

    return render_to_response('index.html', context)


# TODO: not sure where to put this
class LogEntryAdmin(admin.ModelAdmin):
    readonly_fields = ['timestamp']

admin.site.register(models.LogEntry, LogEntryAdmin)
