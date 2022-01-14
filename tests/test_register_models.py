import pytest
from django.contrib.auth.models import Group, Permission, User
from django.db.models.query import QuerySet

from dj_anonymizer import register_models
from dj_anonymizer.anonymizer import Anonymizer


@pytest.mark.django_db
def test_register_clean(mocker):
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
def test_register_clean_duplicate(mocker):
    with pytest.raises(ValueError):
        register_models.register_clean([
            (User, register_models.AnonymBase),
            (User, register_models.AnonymBase),
            (Permission, register_models.AnonymBase(truncate=True)),
            (Group, register_models.AnonymBase())
        ])


@pytest.mark.django_db
def test_register_skip(mocker):
    register_models.register_skip([User, Permission, Group])

    assert len(Anonymizer.clean_models) == 0
    assert len(Anonymizer.skip_models) == 3
    assert len(Anonymizer.anonym_models) == 0

    assert 'django.contrib.auth.models.User' in Anonymizer.skip_models
    assert 'django.contrib.auth.models.Permission' in Anonymizer.skip_models
    assert 'django.contrib.auth.models.Group' in Anonymizer.skip_models


@pytest.mark.django_db
def test_register_skip_duplicate(mocker):
    with pytest.raises(ValueError):
        register_models.register_skip([User, Permission, Group, Group])
