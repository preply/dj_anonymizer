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

# Absolute paths of definition files already imported in this process.
# Definition files run register_* at module level, and register_* raises on a
# duplicate. Because Anonymizer imports these files on every construction, a
# second construction used to re-run those calls and fail with "already
# declared". We therefore load each file at most once per process, mirroring
# how a normal `import` behaves.
_imported_files = set()


def reset_import_cache():
    """
    Forget which definition files have been imported. Only meant for tests,
    which reset the registry between cases and need import_if_exist to load
    files again for the next case.
    """
    _imported_files.clear()


def import_if_exist(filename):
    """
    Check if file exist in appropriate path and import it, at most once per
    process (see _imported_files).
    """
    model_devinition_dir = getattr(
        settings,
        'ANONYMIZER_MODEL_DEFINITION_DIR',
        'anonymizer'
    )
    filepath = os.path.join(model_devinition_dir, filename)
    full_filepath = os.path.abspath(filepath + '.py')

    if full_filepath in _imported_files:
        return

    if os.path.isfile(full_filepath):
        spec = importlib.util.spec_from_file_location(filename, full_filepath)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _imported_files.add(full_filepath)


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
