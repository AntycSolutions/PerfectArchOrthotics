from django.db import models as db_models
from django.utils import timezone
from django.template import defaultfilters
from django.utils import encoding, dateparse
from django.contrib import auth
from django.contrib.contenttypes import models as ct_models

from rest_framework import serializers, decorators, response

from auditlog import models as auditlog_models

from clients import models as clients_models
from inventory import models as inventory_models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = auth.get_user_model()
        fields = ('id', 'first_name', 'last_name', 'email',)


class LogEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = auditlog_models.LogEntry
        fields = (
            'id',
            'content_type',
            'get_action_display',
            'changes',
            'timestamp',
            'actor',
        )

    content_type = serializers.SerializerMethodField()

    def get_content_type(self, obj):
        content_type = obj.content_type.model_class()._meta.verbose_name
        # eg 'member attribute' -> 'attribute'
        content_type = content_type.replace('member ', '')

        return content_type

    actor = UserSerializer(read_only=True)

    timestamp = serializers.SerializerMethodField()

    def get_timestamp(self, obj):
        timestamp = timezone.localtime(obj.timestamp)
        timestamp = defaultfilters.date(
            timestamp, "N j, Y, P"
        )

        return timestamp

    def _get_lookup_values(self, CHOICES, old, new):
        try:
            old_int = int(old)
        except ValueError:
            old_int = None

        try:
            new_int = int(new)
        except ValueError:
            new_int = None

        if old in CHOICES:
            old = CHOICES[old]
        elif old_int and old_int in CHOICES:
            old = CHOICES[old_int]

        if new in CHOICES:
            new = CHOICES[new]
        elif new_int and new_int in CHOICES:
            new = CHOICES[new_int]

        return old, new

    def _check_lookup_values(self, obj, field, old, new):
        # I don't like this but it works...
        model_class = obj.content_type.model_class()
        lookup = None
        person_models = [
            clients_models.Person,
            clients_models.Client,
            clients_models.Dependent
        ]
        order_models = [
            inventory_models.Order,
            inventory_models.ShoeOrder,
            inventory_models.CoverageOrder,
            inventory_models.AdjustmentOrder
        ]
        if model_class in person_models:
            if field == 'gender':
                lookup = dict(clients_models.Client.GENDERS)

        if model_class == clients_models.Dependent:
            if field == 'relationship':
                lookup = dict(clients_models.Dependent.RELATIONSHIPS)
        elif model_class == clients_models.Insurance:
            if field == 'category':
                lookup = dict(clients_models.Insurance.BENEFITS)
        elif model_class == clients_models.Coverage:
            if field == 'coverage_type':
                lookup = dict(clients_models.Coverage.COVERAGE_TYPES)
            elif field == 'period':
                lookup = dict(clients_models.Coverage.PERIODS)
        elif model_class == inventory_models.Shoe:
            if field == 'category':
                lookup = dict(inventory_models.Shoe.CATEGORIES)
            elif field == 'availability':
                lookup = dict(inventory_models.Shoe.AVAILABILITIES)
        elif model_class == inventory_models.ShoeAttributes:
            if field == 'size':
                lookup = dict(inventory_models.ShoeAttributes.SIZES)

        if model_class in order_models:
            if field == 'order_type':
                lookup = dict(inventory_models.Order.ORDER_TYPES)

        if lookup:
            return self._get_lookup_values(lookup, old, new)
        else:
            return old, new

    # this is from django-audilog but changed to exclude some fields
    def _changes_str(
        self,
        obj,
        colon=': ',
        arrow=encoding.smart_text(' \u2192 '),
        separator='<br>'
    ):
        substrings = []
        changes_dict = {
            k: v for k, v in obj.changes_dict.items()
            if k not in ['id', 'person_ptr', 'order_ptr']
        }
        for field, values in changes_dict.items():
            old = values[0]
            new = values[1]
            if (not old or old == 'None') and (not new or new == 'None'):
                # json turns None into str
                # this could be tripped up on values that are actually 'None'
                continue

            # json turns True/False into str
            # this could be tripped up on values that are actually
            # 'True'/'False'
            if old == 'True':
                old = 'Yes'
            elif old == 'False':
                old = 'No'

            if new == 'True':
                new = 'Yes'
            elif new == 'False':
                new = 'No'

            if field in ['created', 'submitted_datetime']:
                old = dateparse.parse_datetime(old)
                old = defaultfilters.date(old, "N j, Y, P")
                new = dateparse.parse_datetime(new)
                new = defaultfilters.date(new, "N j, Y, P")

            old, new = self._check_lookup_values(obj, field, old, new)

            substring = encoding.smart_text(
                '{field_name:s}{colon:s}{old:s}{arrow:s}{new:s}'
            ).format(
                field_name=defaultfilters.capfirst(field).replace('_', ' '),
                colon=colon,
                old=old,
                arrow=arrow,
                new=new,
            )
            substrings.append(substring)

        return separator.join(substrings)

    changes = serializers.SerializerMethodField()

    def get_changes(self, obj):
        # if obj.action == auditlog_models.LogEntry.Action.DELETE:
        #     return ''

        return self._changes_str(obj)


class HistoryMixin:
    def get_history_aliases(self):
        if not hasattr(self, 'history_aliases'):
            raise Exception('Define history_aliases or get_history_aliases')

        return self.history_aliases

    def get_content_type(self):
        if not hasattr(self, 'content_type'):
            return ct_models.ContentType.objects.get_for_model(
                self.queryset.model
            )

        return self.content_type

    @decorators.detail_route(methods=['get'])
    def history(self, request, pk=None):
        obj = self.get_object()

        # this Mixin is almost generic enough, the following additional_data
        # filter is not
        alias_filter = db_models.Q()
        aliases = self.get_history_aliases()
        for alias in aliases:
            # auditlog uses django-jsonfield and does not support key lookup
            alias_filter = alias_filter | db_models.Q(
                # str pl
                additional_data__contains={'{}_id'.format(alias): str(obj.pk)}
            ) | db_models.Q(
                # int pk
                additional_data__contains={'{}_id'.format(alias): obj.pk}
            )
        ct = self.get_content_type()
        history = auditlog_models.LogEntry.objects.filter(
            (
                db_models.Q(content_type_id=ct.pk) &
                db_models.Q(object_id=obj.pk)
            ) |
            alias_filter
        )

        serializer = LogEntrySerializer(history, many=True)

        data = {'history': serializer.data, 'obj_str': str(obj)}

        return response.Response(data)
