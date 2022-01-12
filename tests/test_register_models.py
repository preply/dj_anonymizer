from unittest import mock

from django.contrib.auth.models import Group, Permission, User
from django.db.models.query import QuerySet

from dj_anonymizer import register_models


def test_register_clean(mocker):
    clean_mock = mock.MagicMock()
    mocker.patch(
        'dj_anonymizer.anonymizer.Anonymizer.clean_models',
        clean_mock
    )
    register_models.register_clean([
        (User, register_models.AnonymBase),
        (Permission, register_models.AnonymBase(truncate=True)),
        (Group, register_models.AnonymBase())
    ])

    assert clean_mock._mock_mock_calls[0][1][0] == \
        'django.contrib.auth.models.User'
    assert isinstance(clean_mock._mock_mock_calls[0][1][1], QuerySet)
    assert clean_mock._mock_mock_calls[0][1][1].truncate is False
    assert clean_mock._mock_mock_calls[1][1][0] == \
        'django.contrib.auth.models.Permission'
    assert isinstance(clean_mock._mock_mock_calls[1][1][1], QuerySet)
    assert clean_mock._mock_mock_calls[1][1][1].truncate is True
    assert clean_mock._mock_mock_calls[2][1][1].truncate is False
    assert clean_mock._mock_mock_calls[2][1][0] == \
        'django.contrib.auth.models.Group'
    assert isinstance(clean_mock._mock_mock_calls[2][1][1], QuerySet)


def test_register_skip(mocker):
    skip_mock = mock.MagicMock()
    mocker.patch('dj_anonymizer.anonymizer.Anonymizer.skip_models', skip_mock)
    register_models.register_skip([User, Permission, Group])
    skip_mock.method_calls[0][1] == 'django.contrib.auth.models.User'
    skip_mock.method_calls[1][1] == 'django.contrib.auth.models.Permission'
    skip_mock.method_calls[2][1] == 'django.contrib.auth.models.Group'
