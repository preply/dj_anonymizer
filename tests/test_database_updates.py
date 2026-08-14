import pytest
from django.contrib.auth.models import User
from django.db.models import CharField, F, Value
from django.db.models.functions import Cast, Concat
from django.test import override_settings

from dj_anonymizer import fields, register_models
from dj_anonymizer.anonymizer import Anonymizer


USER_EXCLUDE_FIELDS = [
    'password',
    'last_name',
    'is_staff',
    'is_active',
    'is_superuser',
    'last_login',
    'date_joined',
]


def user_value(prefix):
    return Concat(
        Value(prefix),
        Cast(F('pk'), output_field=CharField()),
    )


@pytest.mark.django_db
@override_settings(ANONYMIZER_DATABASE_UPDATE_BATCH_SIZE=1)
def test_database_updates_are_batched_and_can_mix_with_generators():
    first = User.objects.create(username='first')
    second = User.objects.create(username=f'user-{first.pk}')

    class UserAnonym(register_models.AnonymBase):
        first_name = fields.string('name-{seq}')

        @classmethod
        def get_pre_update_phases(cls, queryset):
            return [{'username': user_value('temporary-user-')}]

        class Meta:
            update_values = {
                'username': user_value('user-'),
                'email': Concat(
                    user_value('user-'),
                    Value('@preply.com'),
                ),
            }
            exclude_fields = USER_EXCLUDE_FIELDS

    register_models.register_anonym([(User, UserAnonym)])
    key = Anonymizer.key(User)
    Anonymizer(only=key).anonymize(only=key)

    first.refresh_from_db()
    second.refresh_from_db()
    assert first.username == f'user-{first.pk}'
    assert second.username == f'user-{second.pk}'
    assert first.email == f'user-{first.pk}@preply.com'
    assert second.email == f'user-{second.pk}@preply.com'
    assert {first.first_name, second.first_name} == {'name-0', 'name-1'}


@pytest.mark.django_db
def test_generator_only_anonymization_skips_database_updates():
    user = User.objects.create(username='first')

    class UserAnonym(register_models.AnonymBase):
        first_name = fields.string('name-{seq}')

        class Meta:
            exclude_fields = USER_EXCLUDE_FIELDS + ['username', 'email']

    register_models.register_anonym([(User, UserAnonym)])
    key = Anonymizer.key(User)
    Anonymizer(only=key).anonymize(only=key)

    user.refresh_from_db()
    assert user.first_name == 'name-0'


@pytest.mark.django_db
def test_database_update_and_generator_cannot_target_the_same_field():
    class UserAnonym(register_models.AnonymBase):
        email = fields.string('user-{seq}@preply.com')

        class Meta:
            update_values = {'email': Value('anonymous@preply.com')}

    with pytest.raises(
        LookupError, match='both generator and database updates'
    ):
        register_models.register_anonym([(User, UserAnonym)])


@pytest.mark.django_db
def test_pre_update_phase_cannot_target_an_unregistered_field():
    User.objects.create(username='first')

    class UserAnonym(register_models.AnonymBase):
        @classmethod
        def get_pre_update_phases(cls, queryset):
            return [{'email': Value('temporary@preply.com')}]

        class Meta:
            update_values = {'username': user_value('user-')}

    register_models.register_anonym([(User, UserAnonym)])
    key = Anonymizer.key(User)
    with pytest.raises(LookupError, match='not present in Meta.update_values'):
        Anonymizer(only=key).anonymize(only=key)


@pytest.mark.django_db
def test_database_update_preserves_custom_queryset():
    included = User.objects.create(username='included')
    excluded = User.objects.create(username='excluded')

    class UserAnonym(register_models.AnonymBase):
        class Meta:
            queryset = User.objects.exclude(pk=excluded.pk)
            update_values = {'username': user_value('user-')}

    register_models.register_anonym([(User, UserAnonym)])
    key = Anonymizer.key(User)
    Anonymizer(only=key).anonymize(only=key)

    included.refresh_from_db()
    excluded.refresh_from_db()
    assert included.username == f'user-{included.pk}'
    assert excluded.username == 'excluded'


@pytest.mark.django_db
@override_settings(ANONYMIZER_DATABASE_UPDATE_BATCH_SIZE=0)
def test_database_update_batch_size_must_be_positive():
    User.objects.create(username='first')

    class UserAnonym(register_models.AnonymBase):
        class Meta:
            update_values = {'username': user_value('user-')}

    register_models.register_anonym([(User, UserAnonym)])
    key = Anonymizer.key(User)
    with pytest.raises(ValueError, match='must be greater than 0'):
        Anonymizer(only=key).anonymize(only=key)
