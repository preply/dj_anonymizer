Run anonymization
=================

Base command to run anonymization and clean models::

    $ python manage.py anonymize_db

**soft_mode** - exception will not be raised if not all project models are registered::

    $ python manage.py anonymize_db --soft_mode


``anonymize_db`` also supports the possibility of separate actions:


- Run only check that all models are registered::

    $ python manage.py anonymize_db --check_only

- Run only table cleaning::

    $ python manage.py anonymize_db --action clean

- Run only anonymization::

    $ python manage.py anonymize_db --action anonymize

For more info, take a look at the built-in help::

    $ python manage.py anonymize_db -h
    usage: manage.py anonymize_db [-h] [-a ACTION] [-c] [-o ONLY] [-s] [--version]
                                  [-v {0,1,2,3}] [--settings SETTINGS]
                                  [--pythonpath PYTHONPATH] [--traceback]
                                  [--no-color] [--force-color]

    Anonymize database according to provided patterns.

    optional arguments:
      -h, --help            show this help message and exit
      -a ACTION, --action ACTION
                            "anonymize" models or "clean" models
                            (default: both actions will be applied)
      -c, --check_only      Check that all models are registered correctly
      -o ONLY, --only ONLY  Execute specified for dj_anonymizer action only on
                            specified model
      -s, --soft_mode       Exception will not be raised if not all project models
                             are registered
      --version             show program's version number and exit
      -v {0,1,2,3}, --verbosity {0,1,2,3}
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=verbose output, 3=very verbose output
      --settings SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this isn't provided,
                            the DJANGO_SETTINGS_MODULE environment variable
                            will be used.
      --pythonpath PYTHONPATH
                            A directory to add to the Python path,
                            e.g. "/home/djangoprojects/myproject".
      --traceback           Raise on CommandError exceptions
      --no-color            Don't colorize the command output.
      --force-color         Force colorization of the command output.
