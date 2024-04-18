from __future__ import absolute_import

from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.utils import timezone

from dj_anonymizer import fields
from dj_anonymizer.register_models import (
    AnonymBase,
    register_anonym,
    register_clean,
    register_skip
)


class UserAnonym(AnonymBase):
    email = fields.string('test_email_{seq}@preply.com',
                          seq_callback=timezone.now)
    username = fields.string('test_username_{seq}@preply.com',
                             seq_callback=timezone.now)
    first_name = fields.string('first name {seq}')
    last_name = fields.string('last name {seq}')
    password = fields.password('password')
    is_staff = fields.function(lambda: False)

    class Meta:
        exclude_fields = ['is_active', 'is_superuser',
                          'last_login', 'date_joined']


class GroupAnonym(AnonymBase):
    name = fields.string('group_{seq}')

    class Meta:
        pass


register_anonym([
    (User, UserAnonym),
    (Group, GroupAnonym),
])


register_clean([
    (Session, AnonymBase),
    (LogEntry, AnonymBase(truncate=True)),
])

register_skip([
    ContentType,
    Permission,
    Session,
])
