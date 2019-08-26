import mock
import pytest
from django.test.utils import override_settings

from dj_anonymizer.utils import import_if_exist


@pytest.mark.parametrize('path, expected', [
    ('hello', False),
    ('base', True),
])
def test_import_if_exist(mocker, path, expected):
    with override_settings(
        ANONYMIZER_MODEL_DEFINITION_DIR='example/anonymizer'
    ):
        mocked_import = mock.MagicMock()
        mocker.patch('importlib.import_module', mocked_import)
        import_if_exist(path)
        assert mocked_import.called is expected
