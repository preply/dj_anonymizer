import mock
import pytest
from django.core import management


class TestAnonymizeDB():
    @pytest.mark.parametrize(
        '''action, check_only, anonymize_called, clean_called''', [
            (None, None, True, True),
            ('anonymize', False, True, False),
            ('clean', False, False, True),
            (None, True, False, False),
        ]
    )
    def test_base(self, mocker, action, check_only,
                  anonymize_called, clean_called):
        anonymize_mock = mock.Mock()
        clean_mock = mock.Mock()
        mocker.patch(
            'dj_anonymizer.anonymizer.Anonymizer.anonymize', anonymize_mock)
        mocker.patch(
            'dj_anonymizer.anonymizer.Anonymizer.clean', clean_mock)

        management.call_command(
            'anonymize_db',
            soft_mode=True,
            action=action,
            check_only=check_only
        )

        assert anonymize_mock.called is anonymize_called
        assert clean_mock.called is clean_called
