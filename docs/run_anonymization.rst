Run anonymization
=================

Base command to run anonymization and clean models::

    $ manage.py anonymize_db

**soft_mode** - exception will not be raised if not all project models are registered::

    $ manage.py anonymize_db --soft_mode


``anonymize_db`` also supports the possibility of separate actions.


Run only table cleaning::

    $ manage.py anonymize_db --action clean

Run only anonymization::

    $ manage.py anonymize_db --action anonymize
