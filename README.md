dj_anonymizer
==================================
dj_anonymizer requires Django 1.8 or greater and Python 2.7 (not support Python 3).
This project helps anonymize production database with fake data of any kind.

dj_anonymizer uses [django-bulk-update](https://github.com/aykut/django-bulk-update) lib to be able to process huge massive of data.

Installation        
==================================
`$ pip install dj_anonymizer`

Add `dj_anonymizer` to `INSTALLED_APPS` in settings:

```
INSTALLED_APPS = [
    # ...
    "dj_anonymizer",
    # ...
]
```

Basic example
==================================
For example you have django project with app `my_app` and `models.py` file:
```
class Author(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField(blank=True, null=True)


class Book(models.Model):
    name = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
```
You want to anonymize authors' names.
So you can set all names as "Jon Dou (n)".

To anonymize your models go through the following steps:

* Create file e.g. `anonymization.py` in `my_app`.
* Add `ANONYMIZER_IMPORTS` to project settings and set path to `anonymization.py` file:
```
ANONYMIZER_IMPORTS = [
    "my_app.anonymization"
]
```
* In `anonymization.py` file:
```
from dj_anonymizer import register_anonym, register_skip, AnonymBase, anonym_field
from my_app import Author, Book


class AuthorAnonym(AnonymBase):
   name = anonym_field.string("Jon Dou {seq}")
   
   class Meta:
       exclude_fields = ["birth_date"]


register_anonym(Author, AuthorAnonym)

register_skip(Book)
```

* Run `$ manage.py anonymize_db`

Usage
===============
You must specify all models and all their fields in dj_anonymizer. This helps you to avoid the situation when something has changed in your project models (e.g. some fields with sensitive data were added) and you forget to clean or fake them.

## Model registration
`from dj_anonymizer import register_anonym, register_skip, register_clean`
* `register_anonym(model, cls_anonym)` - register models for anonymization
    * `model` - model class
    * `cls_anonym` - anonymization class, inherited form `AnonymBase`
* `register_clean(models)` - register models which should be cleaned
    * `models` - list of models, all models data will be deleted.
* `register_clean_with_rules(model, cls_anonym)` - register models which should be cleaned
    * `model` - model class
    * `cls_anonym` - anonymization class, specified queryset of data which must be deleted.
* `register_skip(models)` - list of models which dj_anonymizer will skip.

## Data anonymization
Anonymization class must be inherited from AnonymBase. Anonymization class contains attributes mapped to model fields. Also anonymization class may contain `class Meta` where you can specify queryset and excluded fields.

Example:
 ```
from datetime import datetime

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from dj_anonymizer import register_anonym, AnonymBase, anonym_field
from faker import Factory


# using faker lib for generating nice names
fake = Factory.create()


# create anonymizer class
class UserAnonym(AnonymBase):
    last_name = anonym_field.function(fake.last_name)
    first_name = anonym_field.function(fake.first_name)
    email = anonym_field.string("test_email_{seq}@preply.com", seq_callback=datetime.now)
    username = anonym_field.string("user_name{seq}")
    is_staff = False
    password = make_password("some_test_password", hasher="sha1")

    class Meta:
        queryset = User.objects.exclude(id=1)  # queryset, anonymize all users except the first one
        exclude_fields = ["groups", "user_permissions", "is_active", "is_superuser",
                          "last_login", "date_joined"]  # list of fields which will not be changed


register_anonym(User, UserAnonym)
```

In `class Meta` you can specify `queryset` and `exclude_fields`:
 * `queryset` - model queryset to which anonymization will be applied. If you don't specify this attribute, anonymization will be applied to all rows of model (like `MyModel.objects.all()`)
 * `exclude_fields` - list of model fields which should not be anonymized

dj_anonymizer provides certain helpful field types for anonymization classes:
 
* `anonym_field.function(callback, args=(), kwargs=None)` - result of execution of `callback` function will be set to the model field. `callback` function will be called for every record of your model.
    * `callback` - function which will generate data for the model
    * `args` - tuple of args for `callback`
    * `kwargs` - dict of args for `callback`

* `anonym_field.string(field_value, seq_start=0, seq_step=1, seq_callback=None, seq_args=(), seq_kwargs=None, seq_slugify=True)` - generate string for every record of the model.
    * `field_value` - string which will be set to field. It may contain `{seq}` parameter which will be replaced by sequence value (e.g. `"username_{seq}"` will generate username_1, username_2 etc.)
    * `seq_start` - value of sequence start
    * `seq_step` - step of sequence
    * `seq_callback` - function which will generate data for `{seq}` parameter in string (e.g. `("test_email_{seq}@preply.com", seq_callback=datetime.now)`)
    * `seq_args` - tuple of args for `seq_callback`
    * `seq_kwargs` - dict of kwargs for `seq_callback`
    * `seq_slugify` - flag, slugify or not result of execution of `seq_callback`

## Clean data
Register your model with `register_clean`.

**Example 1** - delete all data from model `User`
```
from django.contrib.auth.models import User

from dj_anonymizer import register_clean


register_clean(User)
```

**Example 2** - delete all data from model `User`, except user with id=1:
```
from django.contrib.auth.models import User

from dj_anonymizer import AnonymBase, register_clean


class UserAnonym(AnonymBase):
    class Meta:
        queryset = User.objects.exclude(id=1)


register_clean(User, UserAnonym)

```

# Run dj_anonymizer
* `$ manage.py anonymize_db`

    run anonymization and clean models which have been registered.

* `$ manage.py anonymize_db --soft_mode`

    run anonymization and clean models. Exception (not all project models are registered) will not be raised that. 

* `$ manage.py anonymize_db --action clean`

    run only delete data

* `$ manage.py anonymize_db --action anonymize`

    run only anonymization data

# Settings

* `ANONYMIZER_IMPORTS` - list of path to *.py files where you register models for anomymization.

* `ANONYMIZER_SKIP_APPS` - list of apps of your django project that you don't want to anonymize.

* `ANONYMIZER_SELECT_BATCH_SIZE` - default value is 20000. 

* `ANONYMIZER_UPDATE_BATCH_SIZE` - default value is 500.
