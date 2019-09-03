import importlib
import os

from django.db import connections, router

from dj_anonymizer.conf import settings


VENDOR_TO_TRUNCATE = {
    'postgresql': 'TRUNCATE TABLE',
    'mysql': 'TRUNCATE TABLE',
    'sqlite': 'DELETE FROM',
    'oracle': 'TRUNCATE TABLE',
}


def import_if_exist(filename):
    """
    Check if file exist in appropriate path and import it
    """
    filepath = os.path.join(settings.ANONYMIZER_MODEL_DEFINITION_DIR, filename)

    if os.path.isfile(os.path.abspath(filepath + '.py')):
        importlib.import_module(filepath.replace('/', '.'))


def truncate_table(model):
    """
    Generate and execute via Django ORM proper SQL to truncate table
    """
    db = router.db_for_write(model)
    connection = connections[db]
    vendor = connection.vendor

    try:
        operation = VENDOR_TO_TRUNCATE[vendor]
    except KeyError:
        raise NotImplementedError(
            "Database vendor %s is not supported" % vendor
        )

    dbtable = '"{}"'.format(model._meta.db_table)

    sql = '{operation} {dbtable}'.format(
        operation=operation,
        dbtable=dbtable,
    )
    with connection.cursor() as c:
        c.execute(sql)
