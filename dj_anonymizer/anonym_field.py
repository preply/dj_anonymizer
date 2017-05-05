import itertools
from django.template.defaultfilters import slugify


def function(callback, args=(), kwargs=None):
    if kwargs is None:
        kwargs = {}

    for _ in itertools.count():
        yield callback(*args, **kwargs)


def string(field_value, seq_start=0, seq_step=1, seq_callback=None, seq_args=(), seq_kwargs=None, seq_slugify=True):
    if seq_kwargs is None:
        seq_kwargs = {}

    for i in itertools.count(seq_start, seq_step):
        seq = i

        if seq_callback:
            seq = seq_callback(*seq_args, **seq_kwargs)
            if seq_slugify:
                seq = slugify(seq)

        yield field_value.format(seq=seq)
