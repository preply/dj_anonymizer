import inspect

from django.db.models.fields import Field
from django.db.models.fields.related import (
    ForeignKey,
    ManyToManyField,
    OneToOneField
)

from dj_anonymizer.anonymizer import Anonymizer


class AnonymBase:
    truncate = False

    def __init__(self, truncate=False):
        self.truncate = truncate

    @classmethod
    def get_fields_names(cls):
        return [
            attr_name for attr_name in dir(cls)
            if inspect.isgenerator(getattr(cls, attr_name))
        ]

    @classmethod
    def get_relation_fields(cls, model):
        relation_fields = [field.name for field in model._meta.get_fields()
                           if isinstance(field, (ManyToManyField,
                                                 OneToOneField,
                                                 ForeignKey))
                           ]
        relation_fields.append(model._meta.pk.name)
        return relation_fields

    @classmethod
    def init_meta(cls, model):
        if hasattr(cls.Meta, 'queryset'):
            if cls.Meta.queryset.model != model:
                raise TypeError(
                    f'Class {Anonymizer.key(cls.Meta.queryset.model)} does '
                    f'not belong to the allowed {Anonymizer.key(AnonymBase)}'
                )
        else:
            setattr(cls.Meta, 'queryset', model.objects.all())

    class Meta:
        pass


def register_anonym(models):
    for model, cls_anonym in models:
        cls_anonym.init_meta(model)

        anonym_fields = set(cls_anonym.get_fields_names())
        model_fields = set(
            field.name for field in model._meta.get_fields()
            if isinstance(field, Field)
        )

        if hasattr(cls_anonym.Meta, 'exclude_fields'):
            exclude_fields = set(cls_anonym.Meta.exclude_fields)
        else:
            exclude_fields = model_fields - anonym_fields

        exclude_fields.update(cls_anonym.get_relation_fields(model))

        if exclude_fields & anonym_fields:
            raise LookupError(
                f'Fields {list(exclude_fields & anonym_fields)} of model '
                f'{Anonymizer.key(model)} are present in both anonymization '
                f'and excluded lists'
            )

        specified_fields = exclude_fields | anonym_fields

        if specified_fields < model_fields:
            raise LookupError(
                f'Fields {list(model_fields - specified_fields)} were not '
                f'registered in {Anonymizer.key(cls_anonym)} class for '
                f'{Anonymizer.key(model)} model'
            )
        if specified_fields > model_fields:
            raise LookupError(
                f'Fields {list(specified_fields - model_fields)} present in '
                f'{Anonymizer.key(cls_anonym)} class, but does not exist in '
                f'{Anonymizer.key(model)} model'''
            )
        if specified_fields != model_fields:
            raise LookupError(
                f'Fields in {Anonymizer.key(cls_anonym)} are not '
                f'the same as in {Anonymizer.key(model)} Check spelling'
            )

        if Anonymizer.key(model) in Anonymizer.anonym_models.keys():
            raise ValueError(
                f'Model {Anonymizer.key(model)} '
                f'is already declared in register_anonym'
            )
        Anonymizer.anonym_models[Anonymizer.key(model)] = cls_anonym


def register_clean(models):
    for model, cls_anonym in models:
        if not (cls_anonym == AnonymBase
                or isinstance(cls_anonym, AnonymBase)):
            raise TypeError(
                f'Class used for cleaning model {Anonymizer.key(model)} does '
                f'not belong to the allowed {Anonymizer.key(AnonymBase)}'
            )
        queryset = model.objects.all()
        queryset.truncate = cls_anonym.truncate
        if Anonymizer.key(model) in Anonymizer.clean_models.keys():
            raise ValueError(
                f'Model {Anonymizer.key(model)} '
                f'is already declared in register_clean'
            )
        Anonymizer.clean_models[Anonymizer.key(model)] = queryset


def register_skip(models):
    for model in models:
        if Anonymizer.key(model) in Anonymizer.skip_models:
            raise ValueError(
                f'Model {Anonymizer.key(model)} '
                f'is already declared in register_skip'
            )
        Anonymizer.skip_models.append(Anonymizer.key(model))
