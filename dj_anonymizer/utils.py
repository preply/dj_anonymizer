import os

from dj_anonymizer.conf import settings


def import_if_exist(filename):
    """
    Check if file exist in appropriate path and import it
    """
    path_to_base_file = os.path.join(
        settings.ANONYMIZER_MODEL_DEFINITION_DIR, filename + '.py')

    if os.path.isfile(os.path.abspath(path_to_base_file)):
        __import__(
            settings.ANONYMIZER_MODEL_DEFINITION_DIR + '.' + filename
        )
