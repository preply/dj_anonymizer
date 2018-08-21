from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import models

from dj_anonymizer.register_models import register_skip

register_skip([
    ContentType,
    models.Group,
    models.User,
    models.Permission,
])
