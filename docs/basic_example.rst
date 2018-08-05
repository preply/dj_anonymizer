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
So you can set all names as "Jon Dou (n)".

To anonymize your models go through the following steps:

* Create file e.g. `anonymization.py` in `my_app`.
* In `anonymization.py` file::

    from dj_anonymizer import register_anonym, register_skip, \
        AnonymBase, anonym_field
    from my_app import Author, Book


    class AuthorAnonym(AnonymBase):
       name = anonym_field.string("Jon Dou {seq}")

       class Meta:
           exclude_fields = ["birth_date"]


    register_anonym([(Author, AuthorAnonym)])

    register_skip(Book)

* Run::

    $ manage.py anonymize_db
