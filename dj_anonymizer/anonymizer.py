import django

from dj_anonymizer.conf import settings
from dj_anonymizer.utils import import_if_exist


if django.__version__ <= '2.2':
    try:
        from django_bulk_update.helper import bulk_update
    except ModuleNotFoundError:
        raise ModuleNotFoundError(
            "Django %s does not have native support for bulk_update and "
            "django_bulk_update is not installed""" % django.__version__
        )


class Anonymizer:
    anonym_models = {}
    clean_models = {}
    skip_models = []

    def __init__(self, soft_mode=True):
        models_set = set()

        # this for django contrib.auth.models or can be used
        # as single file for defining all models to anonymize
        import_if_exist('base')

        for app in django.apps.apps.get_app_configs():
            models_set.update(
                model.__module__ + '.' + model.__name__
                for model in app.get_models()
            )
            import_if_exist(app.name)

        all_models = set(
            self.skip_models +
            list(self.anonym_models.keys()) +
            list(self.clean_models.keys())
        )

        if not soft_mode and not models_set.issubset(all_models):
            raise LookupError(
                'You did not set those models to any list: {}'.format(
                    list(models_set.difference(all_models))))

    def anonymize(self):
        print('Updating started')
        for anonym_cls in list(self.anonym_models.values()):

            if not anonym_cls.get_fields_names():
                continue

            queryset = anonym_cls.Meta.queryset.only(
                *anonym_cls.get_fields_names()
            )

            print('\nGenerating fake values for model "{}"'.format(
                queryset.model.__name__
            ))

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

                if django.__version__ <= '2.2':
                    bulk_update(
                        subset,
                        batch_size=settings.ANONYMIZER_UPDATE_BATCH_SIZE,
                        update_fields=anonym_cls.get_fields_names()
                    )
                else:
                    subset.model.objects.bulk_update(
                        subset,
                        anonym_cls.get_fields_names(),
                        batch_size=settings.ANONYMIZER_UPDATE_BATCH_SIZE,
                    )
        print('\n\nUpdating finished')

    def clean(self):
        print('\nCleaning started\n')
        for queryset in self.clean_models.values():
            print('Cleaning "{}" ...'.format(queryset.model.__name__))
            queryset.delete()
        print('\nCleaning finished')
