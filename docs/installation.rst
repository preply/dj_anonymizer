Installation
============

Getting the code
----------------

The recommended way to install dj_anonymizer is via pip_::

    $ pip install dj_anonymizer

.. _pip: https://pip.pypa.io/

**Note** For compatibility with Django < 2.2 also need to be installed `django-bulk-update`. It can be done manually or via command below::

    $ pip install dj-anonymizer[bulk]

Register the application
------------------------

Add `dj_anonymizer` to ``INSTALLED_APPS`` in settings::

    INSTALLED_APPS = [
        # ...
        "dj_anonymizer",
        # ...
    ]
