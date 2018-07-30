from django.conf import settings

ANONYMIZER_SELECT_BATCH_SIZE = getattr(
    settings, 'ANONYMIZER_SELECT_BATCH_SIZE', 20000
)

ANONYMIZER_UPDATE_BATCH_SIZE = getattr(
    settings, 'ANONYMIZER_UPDATE_BATCH_SIZE', 500
)
