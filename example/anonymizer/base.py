from __future__ import absolute_import

import datetime

from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session

from dj_anonymizer import anonym_field
from dj_anonymizer.register_models import (
    AnonymBase,
    register_anonym,
    register_skip
)


class UserAnonym(AnonymBase):
    email = anonym_field.string('test_email_{seq}@preply.com',
                                seq_callback=datetime.datetime.now)
    username = anonym_field.string('test_username_{seq}@preply.com',
                                   seq_callback=datetime.datetime.now)
    first_name = anonym_field.string('first name {seq}')
    last_name = anonym_field.string('last name {seq}')
    password = anonym_field.password('password')
    is_staff = anonym_field.function(lambda: False)

    class Meta:
        exclude_fields = ['is_active', 'is_superuser',
                          'last_login', 'date_joined']


register_anonym([
    (User, UserAnonym),
])

register_skip([
    ContentType,
    Group,
    Permission,
    LogEntry,
    Session,
])
