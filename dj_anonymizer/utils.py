import importlib
import os

from django.conf import settings
from django.db import connections, router


VENDOR_TO_TRUNCATE = {
    'postgresql': 'TRUNCATE TABLE',
    'mysql': 'TRUNCATE TABLE',
    'sqlite': 'DELETE FROM',
    'oracle': 'TRUNCATE TABLE',
}

VENDOR_TO_CASCADE = {
    'postgresql': 'CASCADE',
    'oracle': 'CASCADE',
}


def import_if_exist(filename):
    """
    Check if file exist in appropriate path and import it
    """
    model_devinition_dir = getattr(
        settings,
        'ANONYMIZER_MODEL_DEFINITION_DIR',
        'anonymizer'
    )
    filepath = os.path.join(model_devinition_dir, filename)
    full_filepath = os.path.abspath(filepath + '.py')

    if os.path.isfile(full_filepath):
        spec = importlib.util.spec_from_file_location(filename, full_filepath)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)


def truncate_table(model, cascade=False):
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

    cascade_op = ''
    try:
        if cascade:
            cascade_op = VENDOR_TO_CASCADE[vendor]
    except KeyError:
        raise NotImplementedError(
            "DB vendor %s does not support TRUNCATE with CASCADE" % vendor
        )

    dbtable = '"{}"'.format(model._meta.db_table)

    sql = '{operation} {dbtable} {cascade}'.format(
        operation=operation,
        dbtable=dbtable,
        cascade=cascade_op,
    ).strip()
    with connection.cursor() as c:
        c.execute(sql)
