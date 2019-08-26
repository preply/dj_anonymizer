import itertools

from django.contrib.auth.hashers import make_password
from django.template.defaultfilters import slugify


def function(callback, *args, **kwargs):
    for _ in itertools.count():
        yield callback(*args, **kwargs)


def password(password, *args, **kwargs):
    for _ in itertools.count():
        yield make_password(password, *args, **kwargs)


def string(field_value, seq_start=0, seq_step=1, seq_callback=None,
           seq_args=(), seq_kwargs=None, seq_slugify=True):
    if seq_kwargs is None:
        seq_kwargs = {}

    for i in itertools.count(seq_start, seq_step):
        if seq_callback:
            seq = seq_callback(*seq_args, **seq_kwargs)
            if seq_slugify:
                seq = slugify(seq)
        else:
            seq = i

        yield field_value.format(seq=seq)
