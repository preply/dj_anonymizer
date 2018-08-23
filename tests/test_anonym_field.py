import pytest

from dj_anonymizer import anonym_field


def test_function():
    def base_func(value=0, *args, **kwargs):
        result = value + sum(args)
        if 'addition' in kwargs:
            result += kwargs['addition']
        return result

    function_field = anonym_field.function(base_func)
    assert next(function_field) == 0

    function_field = anonym_field.function(base_func, 1)
    assert next(function_field) == 1

    function_field = anonym_field.function(base_func, 1, 2)
    assert next(function_field) == 3

    function_field = anonym_field.function(base_func, 1, 2, addition=3)
    assert next(function_field) == 6


@pytest.mark.parametrize(
    '''field_value, seq_start, seq_step, seq_callback, seq_slugify,
       expeted_1, expeted_2''', [
        ("username_{seq}", 0, 1, None, True, "username_0", "username_1"),
        ("username_{seq}", 5, 10, None, True, "username_5", "username_15"),
    ]
)
def test_string(field_value, seq_start, seq_step, seq_callback, seq_slugify,
                expeted_1, expeted_2):
    username_field = anonym_field.string(
        field_value=field_value,
        seq_start=seq_start,
        seq_step=seq_step,
        seq_callback=seq_callback,
        seq_slugify=seq_slugify
    )
    assert next(username_field) == expeted_1
    assert next(username_field) == expeted_2
