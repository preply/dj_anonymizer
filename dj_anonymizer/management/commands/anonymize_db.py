import time
from django.core.management.base import BaseCommand
from django.conf import settings

from apollo import settings
from dj_anonymizer.anonymizer import Anonymizer


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--action', help='"anonymize" models or "clean" models (default: both actions will be applied)')
        parser.add_argument('-s', '--soft_mode', action='store_true')

    def handle(self, *args, **options):
        print 'Anonymizer found next DB settings:'
        for db in settings.DATABASES:
            print '{} -- NAME: {}, HOST: {}'.format(db, settings.DATABASES[db]['NAME'], settings.DATABASES[db]['HOST'] or 'localhsot')
        start = time.time()
        anonymizer = Anonymizer(soft_mode=options['soft_mode'])
        if options['action'] is None or options['action'] == 'anonymize':
            anonymizer.anonymize()
        if options['action'] is None or options['action'] == 'clean':
            anonymizer.clean()
        end = time.time()
        print '=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-='
        print 'Total time (sec.): {}'.format(end - start)
