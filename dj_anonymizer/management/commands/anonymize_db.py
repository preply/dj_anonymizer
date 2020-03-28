import time

from django.core.management.base import BaseCommand

from dj_anonymizer.anonymizer import Anonymizer


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-a', '--action',
                            help='"anonymize" models or "clean" models '
                                 '(default: both actions will be applied)')
        parser.add_argument('-s', '--soft_mode', action='store_true',
                            help='Exception will not be raised if not all '
                                 'project models are registered')
        parser.add_argument('-c', '--check_only', action='store_true',
                            help='Check that all models are registered '
                                 'correctly')

    def handle(self, *args, **options):
        start = time.time()
        anonymizer = Anonymizer(soft_mode=options['soft_mode'])
        print('Check pass successfully')
        if options['check_only'] is True:
            return
        if options['action'] is None or options['action'] == 'anonymize':
            anonymizer.anonymize()
        if options['action'] is None or options['action'] == 'clean':
            anonymizer.clean()
        end = time.time()
        print('=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
        print('Total time (sec.): {}'.format(end - start))
