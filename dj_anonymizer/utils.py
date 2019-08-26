import importlib
import os

from dj_anonymizer.conf import settings


def import_if_exist(filename):
    """
    Check if file exist in appropriate path and import it
    """
    filepath = os.path.join(settings.ANONYMIZER_MODEL_DEFINITION_DIR, filename)

    if os.path.isfile(os.path.abspath(filepath + '.py')):
        importlib.import_module(filepath.replace('/', '.'))
