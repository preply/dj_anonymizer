import datetime
import types

import pytest
from django.contrib.auth.models import Group, Permission, User
from django.db.models.query import QuerySet

from dj_anonymizer import fields, register_models
from dj_anonymizer.anonymizer import Anonymizer


@pytest.mark.django_db
def test_register_anonym():
    class UserAnonym(register_models.AnonymBase):
        email = fields.string('test_email_{seq}@preply.com',
                              seq_callback=datetime.datetime.now)
        username = fields.string('test_username_{seq}@preply.com',
                                 seq_callback=datetime.datetime.now)
        first_name = fields.string('first name {seq}')
        last_name = fields.string('last name {seq}')
        password = fields.password('password')
        is_staff = fields.function(lambda: False)

        class Meta:
            exclude_fields = ['is_active', 'is_superuser',
                              'last_login', 'date_joined']
    register_models.register_anonym([
        (User, UserAnonym)
    ])

    assert len(Anonymizer.clean_models) == 0
    assert len(Anonymizer.skip_models) == 0
    assert len(Anonymizer.anonym_models) == 1

    assert 'django.contrib.auth.models.User' in \
        Anonymizer.anonym_models.keys()

    assert isinstance(
        Anonymizer.anonym_models[
            'django.contrib.auth.models.User'
        ].Meta.queryset,
        QuerySet
    )

    Anonymizer.anonym_models[
        'django.contrib.auth.models.User'
    ].Meta.queryset.model is User

    assert Anonymizer.anonym_models[
        'django.contrib.auth.models.User'
    ].Meta.exclude_fields == [
        'is_active', 'is_superuser', 'last_login', 'date_joined'
    ]

    assert isinstance(
        Anonymizer.anonym_models['django.contrib.auth.models.User'].email,
        types.GeneratorType
    )
    assert isinstance(
        Anonymizer.anonym_models['django.contrib.auth.models.User'].username,
        types.GeneratorType
    )
    assert isinstance(
        Anonymizer.anonym_models['django.contrib.auth.models.User'].first_name,
        types.GeneratorType
    )
    assert isinstance(
        Anonymizer.anonym_models['django.contrib.auth.models.User'].last_name,
        types.GeneratorType
    )
    assert isinstance(
        Anonymizer.anonym_models['django.contrib.auth.models.User'].password,
        types.GeneratorType
    )
    assert isinstance(
        Anonymizer.anonym_models['django.contrib.auth.models.User'].is_staff,
        types.GeneratorType
    )

    assert next(
        Anonymizer.anonym_models['django.contrib.auth.models.User'].first_name
    ) == 'first name 0'
    assert next(
        Anonymizer.anonym_models['django.contrib.auth.models.User'].is_staff
    ) is False


@pytest.mark.django_db
def test_register_anonym_no_exclude():
    class UserAnonym(register_models.AnonymBase):
        email = fields.string('test_email_{seq}@preply.com',
                              seq_callback=datetime.datetime.now)
        username = fields.string('test_username_{seq}@preply.com',
                                 seq_callback=datetime.datetime.now)
        first_name = fields.string('first name {seq}')
        last_name = fields.string('last name {seq}')
        password = fields.password('password')
        is_staff = fields.function(lambda: False)

    register_models.register_anonym([
        (User, UserAnonym)
    ])

    assert len(Anonymizer.clean_models) == 0
    assert len(Anonymizer.skip_models) == 0
    assert len(Anonymizer.anonym_models) == 1

    assert 'django.contrib.auth.models.User' in \
        Anonymizer.anonym_models.keys()

    assert isinstance(
        Anonymizer.anonym_models[
            'django.contrib.auth.models.User'
        ].Meta.queryset,
        QuerySet
    )

    Anonymizer.anonym_models[
        'django.contrib.auth.models.User'
    ].Meta.queryset.model is User

    assert isinstance(
        Anonymizer.anonym_models['django.contrib.auth.models.User'].email,
        types.GeneratorType
    )
    assert isinstance(
        Anonymizer.anonym_models['django.contrib.auth.models.User'].username,
        types.GeneratorType
    )
    assert isinstance(
        Anonymizer.anonym_models['django.contrib.auth.models.User'].first_name,
        types.GeneratorType
    )
    assert isinstance(
        Anonymizer.anonym_models['django.contrib.auth.models.User'].last_name,
        types.GeneratorType
    )
    assert isinstance(
        Anonymizer.anonym_models['django.contrib.auth.models.User'].password,
        types.GeneratorType
    )
    assert isinstance(
        Anonymizer.anonym_models['django.contrib.auth.models.User'].is_staff,
        types.GeneratorType
    )

    assert next(
        Anonymizer.anonym_models['django.contrib.auth.models.User'].first_name
    ) == 'first name 0'
    assert next(
        Anonymizer.anonym_models['django.contrib.auth.models.User'].is_staff
    ) is False


@pytest.mark.django_db
def test_register_anonym_duplicate():
    class UserAnonym(register_models.AnonymBase):
        email = fields.string('test_email_{seq}@preply.com',
                              seq_callback=datetime.datetime.now)
        username = fields.string('test_username_{seq}@preply.com',
                                 seq_callback=datetime.datetime.now)
        first_name = fields.string('first name {seq}')
        last_name = fields.string('last name {seq}')
        password = fields.password('password')
        is_staff = fields.function(lambda: False)

        class Meta:
            exclude_fields = ['is_active', 'is_superuser',
                              'last_login', 'date_joined']

    with pytest.raises(ValueError):
        register_models.register_anonym([
            (User, UserAnonym),
            (User, UserAnonym),
        ])


@pytest.mark.django_db
def test_register_clean():
    register_models.register_clean([
        (User, register_models.AnonymBase),
        (Permission, register_models.AnonymBase(truncate=True)),
        (Group, register_models.AnonymBase())
    ])

    assert len(Anonymizer.clean_models) == 3
    assert len(Anonymizer.skip_models) == 0
    assert len(Anonymizer.anonym_models) == 0

    assert 'django.contrib.auth.models.User' in \
        Anonymizer.clean_models.keys()
    assert 'django.contrib.auth.models.Permission' in \
        Anonymizer.clean_models.keys()
    assert 'django.contrib.auth.models.Group' in \
        Anonymizer.clean_models.keys()

    assert isinstance(
        Anonymizer.clean_models['django.contrib.auth.models.User'],
        QuerySet
    )
    assert isinstance(
        Anonymizer.clean_models['django.contrib.auth.models.Permission'],
        QuerySet
    )
    assert isinstance(
        Anonymizer.clean_models['django.contrib.auth.models.Group'],
        QuerySet
    )

    assert Anonymizer.clean_models[
        "django.contrib.auth.models.User"
    ].model is User
    assert Anonymizer.clean_models[
        "django.contrib.auth.models.Permission"
    ].model is Permission
    assert Anonymizer.clean_models[
        "django.contrib.auth.models.Group"
    ].model is Group


@pytest.mark.django_db
def test_register_clean_duplicate():
    with pytest.raises(ValueError):
        register_models.register_clean([
            (User, register_models.AnonymBase),
            (User, register_models.AnonymBase),
            (Permission, register_models.AnonymBase(truncate=True)),
            (Group, register_models.AnonymBase())
        ])


@pytest.mark.django_db
def test_register_clean_mixed_args():
    with pytest.raises(TypeError):
        register_models.register_clean([
            (User, register_models.AnonymBase),
            (register_models.AnonymBase, Permission)
        ])


@pytest.mark.django_db
def test_register_clean_none():
    with pytest.raises(TypeError):
        register_models.register_clean([
            (User, register_models.AnonymBase),
            (Permission, None)
        ])


@pytest.mark.django_db
def test_register_skip():
    register_models.register_skip([User, Permission, Group])

    assert len(Anonymizer.clean_models) == 0
    assert len(Anonymizer.skip_models) == 3
    assert len(Anonymizer.anonym_models) == 0

    assert 'django.contrib.auth.models.User' in Anonymizer.skip_models
    assert 'django.contrib.auth.models.Permission' in Anonymizer.skip_models
    assert 'django.contrib.auth.models.Group' in Anonymizer.skip_models


@pytest.mark.django_db
def test_register_skip_duplicate():
    with pytest.raises(ValueError):
        register_models.register_skip([User, Permission, Group, Group])
