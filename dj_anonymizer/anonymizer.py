import math
from collections import OrderedDict
from operator import attrgetter
from sys import stdout

from bulk_update.helper import bulk_update
from django.apps import apps
from django.conf import settings
from django.db import models

from .defaults import ANONYMIZER_SELECT_BATCH_SIZE, ANONYMIZER_UPDATE_BATCH_SIZE


class Anonymizer:
    anonym_models = OrderedDict()
    clean_models = OrderedDict()
    skip_models = []

    def __init__(self, soft_mode=True):
        for module in settings.ANONYMIZER_IMPORTS:
            __import__(module)

        models_set = set()
        for app in apps.get_app_configs():
            if app.name not in settings.ANONYMIZER_SKIP_APPS:
                models_set.update(model.__module__ + '.' + model.__name__ for model in app.get_models())

        if not soft_mode and not models_set.issubset(set(self.skip_models + self.anonym_models.keys() + self.clean_models.keys())):
            print 'You did not set models to any list:'
            print list(models_set.difference(set(self.skip_models + self.anonym_models.keys() + self.clean_models.keys())))
            raise LookupError

    def anonymize(self):
        print 'Updating started'
        for anonym_cls in self.anonym_models.values():
            if not anonym_cls._get_fields_names():
                continue

            queryset = anonym_cls.Meta.queryset.only(*anonym_cls._get_fields_names())
            print '\nGenerating fake values for model "{}"'.format(queryset.model.__name__)
            i = 0
            total = queryset.count()
            for j in range(0, total, ANONYMIZER_SELECT_BATCH_SIZE) + [None]:
                sub_set = queryset.order_by('pk')[i:j]
                for model in sub_set:
                    i += 1
                    stdout.write('\rProgress: {}%'.format(int(math.floor((i / float(total) * 100)))))
                    stdout.flush()

                    for name in anonym_cls._get_fields_names():
                        if getattr(model, name) or anonym_cls.Meta.fill_empty:
                            setattr(model, name, next(getattr(anonym_cls, name)))

                bulk_update(sub_set, batch_size=ANONYMIZER_UPDATE_BATCH_SIZE, update_fields=anonym_cls._get_fields_names())
        print '\n\nUpdating finished'

    def clean(self):
        print '\nCleaning started\n'

        warning_models = []
        for model_name, queryset in self.clean_models.items():
            for field in queryset.model._meta.fields:
                try:
                    on_delete = attrgetter('rel.on_delete')(field)
                except AttributeError:
                    continue
                if on_delete is models.CASCADE:
                    warning_models.append(model_name)

        print 'WARNING: Next models have ForeignKey fields with cascade delete option'
        print warning_models

        for queryset in self.clean_models.values():
            print 'Cleaning "{}" ...'.format(queryset.model.__name__)
            queryset.delete()

        print '\nCleaning finished'
