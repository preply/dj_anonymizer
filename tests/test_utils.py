from unittest import mock

import pytest
from django.contrib.auth.models import User
from django.db import DEFAULT_DB_ALIAS
from django.test.utils import override_settings

from dj_anonymizer.utils import import_if_exist, truncate_table


@pytest.mark.parametrize('path, expected', [
    ('hello', False),
    ('base', True),
])
def test_import_if_exist(mocker, path, expected):
    with override_settings(
        ANONYMIZER_MODEL_DEFINITION_DIR='example/anonymizer'
    ):
        mocked_import = mock.MagicMock()
        mocker.patch('importlib.util.spec_from_file_location', mocked_import)
        import_if_exist(path)
        assert mocked_import.called is expected


@mock.patch('dj_anonymizer.utils.connections')
def test_truncate_table(mock_connections):
    mock_cursor = mock_connections.\
        __getitem__(DEFAULT_DB_ALIAS).\
        cursor.return_value.__enter__.return_value
    mock_connections.__getitem__(DEFAULT_DB_ALIAS).vendor = 'sqlite'

    truncate_table(User)
    mock_cursor.execute.assert_called_once_with('DELETE FROM "auth_user"')

    mock_connections.__getitem__(DEFAULT_DB_ALIAS).vendor = 'dummy'

    with pytest.raises(NotImplementedError):
        truncate_table(User)


@mock.patch('dj_anonymizer.utils.connections')
def test_truncate_table_with_cascade(mock_connections):
    mock_cursor = mock_connections.\
        __getitem__(DEFAULT_DB_ALIAS).\
        cursor.return_value.__enter__.return_value
    mock_connections.__getitem__(DEFAULT_DB_ALIAS).vendor = 'postgresql'

    truncate_table(User, True)
    mock_cursor.execute.assert_called_once_with('TRUNCATE TABLE "auth_user" CASCADE')

    mock_connections.__getitem__(DEFAULT_DB_ALIAS).vendor = 'sqlite'

    with pytest.raises(NotImplementedError):
        truncate_table(User, True)

