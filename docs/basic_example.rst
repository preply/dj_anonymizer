Basic example
=============

For example you have django project with app `my_app` and **models.py** file::

    class Author(models.Model):
        name = models.CharField(max_length=100)
        birth_date = models.DateField(blank=True, null=True)


    class Book(models.Model):
        name = models.CharField(max_length=100)
        authors = models.ManyToManyField(Author)

You want to anonymize authors' names.
So you can set all names as "John Doe (n)".

To anonymize your models go through the following steps:

* Create folder `anonymizer` and file `my_app.py` in it.
* In `my_app.py` file::

    from dj_anonymizer.register_models import (
        AnonymBase,
        register_anonym,
        register_skip
    )
    from dj_anonymizer import anonym_field
    from my_app import Author, Book


    class AuthorAnonym(AnonymBase):
       name = anonym_field.string("John Doe {seq}")

       class Meta:
           exclude_fields = ["birth_date"]


    register_anonym([(Author, AuthorAnonym)])

    register_skip(Book)

* Run::

    $ manage.py anonymize_db --soft_mode

**Note** soft_mode here means that you no need to register all models before anonymization.
