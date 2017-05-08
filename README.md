dj_anonymizer
==================================
This project helps you to anonymize your production database with any fake data as you want.

dj_generating uses [django-bulk-update](https://github.com/aykut/django-bulk-update) lib to be able to prcess huge massive of data.

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
And for example you want to anonymize authors' names.
So you can set all names as "Jon Dou (n)".

For anonymize your models go through the next steps:

* Create file e.g. `anonymization.py` in `my_app`.
* Add `ANONYMIZER_IMPORTS` to project settings and set path to _anonymization.py_ file:
```
ANONYMIZER_IMPORTS = [
    "my_app.anonymization"
]
```
* in `anonymization.py`
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

* Run `manage.py anonymize_db`

Usage
===============
You must specify all models and all thier fields in dj_anonymizer. This helps you to avoid the situation when something has changed in your project models (e.g. some fields with sensitive data were added) and you forget to clean or fake them.

## Model registrations
`from dj_anonymizer import register_anonym, register_skip, register_clean`
* `register_anonym(model, cls_anonym)` - register models for anonymization
    * `model` - model class
    * `cls_anonym` - aninymizations class, inherited form AnonymBase
* `register_clean(model, cls_anonym=None)` - register models witch should be cleaned
    * `model` - model class
    * `cls_anonym` - aninymizations class, specified queryset of data witch must be deleted. if `cls_anonym=None` all data from model will be deleted.
* `register_skip(*args)` - list of models witch dj_anonymizer will skip.

## Anonymize data
Anonymization class must be inherited from AnonymBase. Anonymization class contains class attributes witch mapped to model fields. Also anonymization class could contains `class Meta` where you can specified queryset and excluded fields.

Example:
 ```angular2html
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
                          "last_login", "date_joined"]  # list of fields witch will not be changed


register_anonym(User, UserAnonym)
```

In `class Meta` you can specify `queryset` and `exclude_fields`:
 * `queryset` - model queryset to witch will be applied anonymization. If you don't specified this attribute anonymizations will be applied to all rows of model (like `MyModel.objects.all()`)
 * `exclude_fields` - list of model fields witch should't be anonymized

dj_anonymizer provides some helpful field types for anonymization classes:
 
* `anonym_field.function(callback, args=(), kwargs=None)` - result of callback function will be set to the model field. callback function will be called for every record of your model.
    * `callback` - function witch will generate data for model
    * `args` - tuple of args for `callback`
    * `kwargs` - dict of args for `callback`

* `anonym_field.string(field_value, seq_start=0, seq_step=1, seq_callback=None, seq_args=(), seq_kwargs=None, seq_slugify=True)` - generate string for every record of the model.
    * `field_value` - string witc will be set to field. It could contain `{seq}` parameter inside witch replaced to sequence value (e.g. `"username_{seq}"` will generate username_1, username_2 etc.)
    * `seq_start` - value of sequence state
    * `seq_step` - step of sequence
    * `seq_callback` - function witch will generate data for `{seq}` parameter in string (e.g. `("test_email_{seq}@preply.com", seq_callback=datetime.now)`)
    * `seq_args` - tuple of args for `seq_callback`
    * `seq_kwargs` - dict of args for `seq_callback`
    * `seq_slugify` - flag, slugify or not result of `seq_callback`

##Clean data
Just register your model with `register_clean`.

**Example 1** - delete all data from model User
```
from django.contrib.auth.models import User

from dj_anonymizer import register_clean


register_clean(User)
```

**Example 2** - delete all data from model User, except user with id=1:
```
from django.contrib.auth.models import User

from dj_anonymizer import AnonymBase, register_clean


class UserAnonym(AnonymBase):
    class Meta:
        queryset = User.objects.exclude(id=1)


register_clean(User, UserAnonym)

```

#Run dj_anonymizer
`$ manage.py dj_anonymizer`

run anonymize and clean models witch you have been registered.

`$ manage.py dj_anonymizer --soft_mode`

run anonymize and clean models and will not raise exception that not all project models are registered. 



`$ manage.py dj_anonymizer --action clean`

will run only delete data (will not anonymize data)

`$ manage.py dj_anonymizer --action anonymize`
will run only anonymize data (will not delete data)

# Setting

* `ANONYMIZER_IMPORTS` - list of path to *.py files where you register models for anomymization.

* `ANONYMIZER_SKIP_APPS` - list of apps of your django project that you don't want to anonymize.

* `ANONYMIZER_SELECT_BATCH_SIZE` - default value is 20000. 

* `ANONYMIZER_UPDATE_BATCH_SIZE` - default value is 500.