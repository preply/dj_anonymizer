import mock
from django.contrib.auth.models import Group, Permission, User

from dj_anonymizer import register_models


def test_register_skip(mocker):
    skip_mock = mock.MagicMock()
    mocker.patch('dj_anonymizer.anonymizer.Anonymizer.skip_models', skip_mock)
    register_models.register_skip([User, Permission, Group])
    skip_mock.method_calls[0][1] == 'django.contrib.auth.models.User'
    skip_mock.method_calls[1][1] == 'django.contrib.auth.models.Permission'
    skip_mock.method_calls[2][1] == 'django.contrib.auth.models.Group'
