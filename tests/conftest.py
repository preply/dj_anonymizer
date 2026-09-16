import pytest

from dj_anonymizer.anonymizer import Anonymizer
from dj_anonymizer.utils import reset_import_cache


@pytest.fixture(autouse=True, scope="function")
def clean_anonymizer_state():
    Anonymizer.anonym_models = {}
    Anonymizer.clean_models = {}
    Anonymizer.skip_models = []
    reset_import_cache()
