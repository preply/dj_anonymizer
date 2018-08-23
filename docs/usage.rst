Usage
=====

You must specify all models and all their fields in dj_anonymizer. This helps you to avoid the situation when something has changed in your project models (e.g. some fields with sensitive data were added) and you forget to clean or fake them.

Model registration
------------------

.. function:: register_anonym(models)

    Register models for anonymization

    * `models` - list of tuples `(model, cls_anonym)`, where `model` is a model class and `cls_anonym` - anonymization class, inherited form `AnonymBase`.

.. function:: register_clean(models)

    Register models which should be cleaned

    * `models` - list of models, all models data will be deleted.

.. function:: register_clean_with_rules(model, cls_anonym)

    Register model which should be cleaned with usage of some rules

    * `model` - model class
    * `cls_anonym` - anonymization class, specified queryset of data which must be deleted.

.. function:: register_skip(models)

    List of models which dj_anonymizer will skip.

Data anonymization
------------------

Anonymization class must be inherited from AnonymBase.
Anonymization class contains attributes mapped to model fields.
Also anonymization class may contain **class Meta** where you can specify queryset and excluded fields.

Example::

    from datetime import datetime

    from django.contrib.auth.models import User
    from django.contrib.auth.hashers import make_password

    from dj_anonymizer.register_models import (
        AnonymBase,
        register_anonym
    )
    from dj_anonymizer import anonym_field

    from faker import Factory


    # using faker lib for generating nice names
    fake = Factory.create()


    # create anonymizer class
    class UserAnonym(AnonymBase):
        last_name = anonym_field.function(fake.last_name)
        first_name = anonym_field.function(fake.first_name)
        email = anonym_field.string("test_email_{seq}@preply.com",
                                    seq_callback=datetime.now)
        username = anonym_field.string("user_name{seq}")
        is_staff = anonym_field.function(lambda: False)
        password = make_password("some_test_password", hasher="sha1")

        class Meta:
            # anonymize all users except the first one
            queryset = User.objects.exclude(id=1)
            # list of fields which will not be changed
            exclude_fields = [
                "groups", "user_permissions", "is_active",
                "is_superuser", "last_login", "date_joined"
            ]


    register_anonym([
        (User, UserAnonym),
        (SomeClass, SomeClassAnonym)
    ])

In `class Meta` you can specify `queryset` and `exclude_fields`:
 * `queryset` - model queryset to which anonymization will be applied. If you don't specify this attribute, anonymization will be applied to all rows of model (like `MyModel.objects.all()`)
 * `exclude_fields` - list of model fields which should not be anonymized

dj_anonymizer provides certain helpful field types for anonymization classes:

.. function:: anonym_field.function(callback, *arg, **kwargs)

    Result of execution of `callback` function will be set to the model field. `callback` function will be called for every record of your model.

    * `callback` - function which will generate data for the model
    * `*args` - tuple of args for `callback`
    * `**kwargs` - dict of args for `callback`

.. function:: anonym_field.string(field_value, seq_start=0, seq_step=1, seq_callback=None, seq_args=(), seq_kwargs=None, seq_slugify=True)

    Generate string for every record of the model.

    * `field_value` - string which will be set to field. It may contain `{seq}` parameter which will be replaced by sequence value (e.g. `"username_{seq}"` will generate username_1, username_2 etc.)
    * `seq_start` - value of sequence start
    * `seq_step` - step of sequence
    * `seq_callback` - function which will generate data for `{seq}` parameter in string (e.g. `("test_email_{seq}@preply.com", seq_callback=datetime.now)`)
    * `seq_args` - tuple of args for `seq_callback`
    * `seq_kwargs` - dict of kwargs for `seq_callback`
    * `seq_slugify` - flag, slugify or not result of execution of `seq_callback`

Clean data
----------

Register your model with **register_clean**.

Example 1 - delete all data from model `User`::

    from django.contrib.auth.models import User

    from dj_anonymizer.register_models import register_clean


    register_clean(User)

Example 2 - delete all data from model `User`, except user with id=1::

    from django.contrib.auth.models import User

    from dj_anonymizer.register_models import AnonymBase
    from dj_anonymizer.register_models import register_clean


    class UserAnonym(AnonymBase):
        class Meta:
            queryset = User.objects.exclude(id=1)


    register_clean(User, UserAnonym)
