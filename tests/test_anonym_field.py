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
        ("username_{seq}", 0, 1, None,
         True, "username_0", "username_1"),
        ("username_{seq}", 5, 10, None,
         True, "username_5", "username_15"),
        ("username_{seq}", 5, 10, lambda: "val",
         True, "username_val", "username_val"),
        ("username_{seq}", 5, 10, lambda: "va l",
         True, "username_va-l", "username_va-l"),
        ("username_{seq}", 5, 10, lambda: "va l",
         False, "username_va l", "username_va l"),
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


@pytest.mark.parametrize(
    '''password, salt, hasher, expected_1, expected_2''', [
        ('password', '111', 'md5',
         'md5$111$d7fe5ea5ff97cc7c2c79e2df5eb7cf93',
         'md5$111$d7fe5ea5ff97cc7c2c79e2df5eb7cf93'),
        ('password', None, 'unsalted_md5',
         '5f4dcc3b5aa765d61d8327deb882cf99',
         '5f4dcc3b5aa765d61d8327deb882cf99'),
    ]
)
def test_password(password, salt, hasher, expected_1, expected_2):
    password_field = anonym_field.password(password, salt=salt, hasher=hasher)
    assert next(password_field) == expected_1
    assert next(password_field) == expected_2
