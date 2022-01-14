import pytest

from dj_anonymizer.anonymizer import Anonymizer


@pytest.fixture(autouse=True, scope="function")
def clean_anonymizer_state():
    Anonymizer.anonym_models = {}
    Anonymizer.clean_models = {}
    Anonymizer.skip_models = []
