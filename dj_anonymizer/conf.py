from appconf import AppConf
from django.conf import settings  # noqa


class MyAppConf(AppConf):
    # Size of chunks what will be used to select data from table.
    SELECT_BATCH_SIZE = 20000

    # Size of chunks what will be used to update data in table.
    UPDATE_BATCH_SIZE = 500

    # Default folder with model definitions
    MODEL_DEFINITION_DIR = 'anonymizer'

    class Meta:
        prefix = 'anonymizer'
