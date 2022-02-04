import django

from dj_anonymizer.conf import settings
from dj_anonymizer.utils import import_if_exist, truncate_table


class Anonymizer:
    anonym_models = {}
    clean_models = {}
    skip_models = []

    def __init__(self, soft_mode=True, only=None):
        models_set = set()

        # this for django.contrib.*.models or can be used
        # as single file for defining models for anonymizing
        import_if_exist('base')

        for app in django.apps.apps.get_app_configs():
            models_set.update(
                Anonymizer.key(model)
                for model in app.get_models()
            )
            import_if_exist(app.name)

        all_models = set(
            self.skip_models +
            list(self.anonym_models.keys()) +
            list(self.clean_models.keys())
        )

        if only is not None and only not in all_models:
            raise LookupError(
                f'Model specified at --only attibute({only}) can\'t '
                f'be found at list of registered models'
            )

        if not soft_mode and not models_set.issubset(all_models):
            raise LookupError(
                f'You did not set those models to any list: '
                f'{list(models_set.difference(all_models))}'
            )

    @staticmethod
    def key(model):
        """
        Keys that used for referencing Django models in Anonymizer
        """
        return f'{model.__module__}.{model.__name__}'

    def anonymize(self, only=None):
        anon_list = self.anonym_models.values() if only is None \
            else [self.anonym_models[only]]
        for anonym_cls in anon_list:

            if not anonym_cls.get_fields_names():
                continue

            queryset = anonym_cls.Meta.queryset.only(
                *anonym_cls.get_fields_names()
            )

            print(f'Anonymizing model {self.key(queryset.model)}')

            i = 0
            total = queryset.count()
            for j in list(range(0, total,
                          settings.ANONYMIZER_SELECT_BATCH_SIZE)) + [None]:
                subset = queryset.order_by('pk')[i:j]
                for obj in subset:
                    i += 1

                    for name in anonym_cls.get_fields_names():
                        setattr(obj, name, next(
                            getattr(anonym_cls, name))
                        )
                subset.model.objects.bulk_update(
                    subset,
                    anonym_cls.get_fields_names(),
                    batch_size=settings.ANONYMIZER_UPDATE_BATCH_SIZE,
                )

    def clean(self, only=None):
        clean_list = self.clean_models.values() if only is None \
            else [self.clean_models[only]]
        for queryset in clean_list:
            print(f'Cleaning {self.key(queryset.model)}')
            if getattr(queryset, 'truncate') is True:
                truncate_table(queryset.model)
            else:
                queryset.delete()
