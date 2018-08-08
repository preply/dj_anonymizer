from django.conf import settings

from appconf import AppConf


class MyAppConf(AppConf):
    # Size of chunks what will be used to select data from table.
    SELECT_BATCH_SIZE = 20000

    # Size of chunks what will be used to update data in table.
    UPDATE_BATCH_SIZE = 500

    class Meta:
        prefix = 'anonymizer'
