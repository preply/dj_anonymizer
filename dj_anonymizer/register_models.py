import inspect

from django.db.models.fields import Field
from django.db.models.fields.related import ManyToManyField, OneToOneField, ForeignKey

from anonymizer import Anonymizer


class AnonymBase:
    @classmethod
    def _get_fields_names(cls):
        return [attr_name for attr_name in dir(cls) if inspect.isgenerator(getattr(cls, attr_name))]

    @classmethod
    def _init_meta(cls, model):
        class Meta:
            pass

        if not hasattr(cls, 'Meta'):
            setattr(cls, 'Meta', Meta)

        if hasattr(cls.Meta, 'queryset'):
            if cls.Meta.queryset.model is not model:
                raise TypeError
        else:
            setattr(cls.Meta, 'queryset', model.objects.all())

        if not hasattr(cls.Meta, 'exclude_fields'):
            setattr(cls.Meta, 'exclude_fields', [])

        cls.Meta.exclude_fields = list(set(cls.Meta.exclude_fields + [model._meta.pk.name] + [field.name for field in model._meta.get_fields() if isinstance(field, ManyToManyField) or isinstance(field, OneToOneField) or isinstance(field, ForeignKey)]))

        if not hasattr(cls.Meta, 'fill_empty'):
            setattr(cls.Meta, 'fill_empty', False)


def register_anonym(model, cls_anonym):
    cls_anonym._init_meta(model)

    exclude_fields = set(cls_anonym.Meta.exclude_fields)

    model_fields = set(field.name for field in model._meta.get_fields() if isinstance(field, Field))
    anonym_fields = set(cls_anonym._get_fields_names())

    if exclude_fields & anonym_fields:
        print 'Fields are in anonymization list and in the excluded list:'
        print list(exclude_fields & anonym_fields)
        raise LookupError

    if exclude_fields | anonym_fields != model_fields:
        if exclude_fields | anonym_fields <= model_fields:
            print 'Fields were not registered in {} class for {} model:'.format(cls_anonym.__name__, model.__name__)
            print list(model_fields - exclude_fields - anonym_fields)
        else:
            print 'Fields are present in {} class but not exist do not in {} model'.format(cls_anonym.__name__, model.__name__)
            print list((exclude_fields | anonym_fields) - model_fields)
        raise LookupError

    Anonymizer.anonym_models[model.__module__ + '.' + model.__name__] = cls_anonym


def register_clean(model, cls_anonym=None):
    if cls_anonym:
        cls_anonym._init_meta(model)
        queryset = cls_anonym.Meta.queryset
    else:
        queryset = model.objects.all()
    Anonymizer.clean_models[model.__module__ + '.' + model.__name__] = queryset


def register_skip(*args):
    for model in args:
        Anonymizer.skip_models.append(model.__module__ + '.' + model.__name__)
