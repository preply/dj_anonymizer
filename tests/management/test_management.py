import mock
import pytest
from django.core import management


class TestAnonymizeDB():
    @pytest.mark.parametrize(
        '''action, anonymize_called, clean_called''', [
            (None, True, True),
            ('anonymize', True, False),
            ('clean', False, True),
        ]
    )
    def test_base(self, mocker, action, anonymize_called, clean_called):
        anonymize_mock = mock.Mock()
        clean_mock = mock.Mock()
        mocker.patch(
            'dj_anonymizer.anonymizer.Anonymizer.anonymize', anonymize_mock)
        mocker.patch(
            'dj_anonymizer.anonymizer.Anonymizer.clean', clean_mock)

        management.call_command('anonymize_db', '-s', action=action)

        assert anonymize_mock.called is anonymize_called
        assert clean_mock.called is clean_called
