import inspect

from django.db.models.fields import Field
from django.db.models.fields.related import (
    ForeignKey,
    ManyToManyField,
    OneToOneField
)

from dj_anonymizer.anonymizer import Anonymizer


class AnonymBase:
    @classmethod
    def get_fields_names(cls):
        return [
            attr_name for attr_name in dir(cls)
            if inspect.isgenerator(getattr(cls, attr_name))
        ]

    @classmethod
    def init_meta(cls, model):
        if hasattr(cls.Meta, 'queryset'):
            if cls.Meta.queryset.model is not model:
                raise TypeError
        else:
            setattr(cls.Meta, 'queryset', model.objects.all())

        if not hasattr(cls.Meta, 'exclude_fields'):
            setattr(cls.Meta, 'exclude_fields', [])

        relation_fields = [field.name for field in model._meta.get_fields()
                           if isinstance(field, (ManyToManyField,
                                                 OneToOneField,
                                                 ForeignKey))
                           ]
        relation_fields.append(model._meta.pk.name)

        cls.Meta.exclude_fields.extend(relation_fields)

    class Meta:
        pass


def register_anonym(models):
    for model, cls_anonym in models:
        cls_anonym.init_meta(model)

        exclude_fields = set(cls_anonym.Meta.exclude_fields)
        anonym_fields = set(cls_anonym.get_fields_names())

        model_fields = set(
            field.name for field in model._meta.get_fields()
            if isinstance(field, Field)
        )

        if exclude_fields & anonym_fields:
            raise LookupError(
                'Fields {} of model {} are present in both' +
                'anonymization and excluded lists'
                .format(list(exclude_fields & anonym_fields), model.__name__)
            )

        specified_fields = exclude_fields | anonym_fields

        if specified_fields < model_fields:
            raise LookupError(
                'Fields {} were not registered in {} class for {} model'
                .format(list(model_fields - specified_fields),
                        cls_anonym.__name__,
                        model.__name__)
            )
        if specified_fields > model_fields:
            raise LookupError(
                'Fields {} present in {} class, but does not exist in {} model'
                .format(list(specified_fields - model_fields),
                        cls_anonym.__name__,
                        model.__name__)
            )
        if specified_fields != model_fields:
            raise LookupError(
                'Fields in {} are not the same as in {}. Check spelling'
                .format(cls_anonym.__name__, model.__name__)
            )

        Anonymizer.anonym_models[model.__module__ +
                                 '.' + model.__name__] = cls_anonym


def register_clean(models):
    for model in models:
        queryset = model.objects.all()
        Anonymizer.clean_models[model.__module__ +
                                '.' + model.__name__] = queryset


def register_clean_with_rules(model, cls_anonym):
    cls_anonym.init_meta(model)
    queryset = cls_anonym.Meta.queryset
    Anonymizer.clean_models[model.__module__ + '.' + model.__name__] = queryset


def register_skip(models):
    for model in models:
        Anonymizer.skip_models.append(model.__module__ + '.' + model.__name__)
