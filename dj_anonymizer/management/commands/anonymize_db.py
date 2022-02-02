import time

from django.core.management.base import BaseCommand

from dj_anonymizer.anonymizer import Anonymizer


class Command(BaseCommand):
    help = "Anonymize database according to provided patterns."

    def add_arguments(self, parser):
        parser.add_argument('-a', '--action',
                            help='"anonymize" models or "clean" models '
                                 '(default: both actions will be applied)')
        parser.add_argument('-c', '--check_only', action='store_true',
                            help='Check that all models are registered '
                                 'correctly')
        parser.add_argument('-o', '--only',
                            help='Execute specified for dj_anonymizer action '
                                 'only on specified model')
        parser.add_argument('-s', '--soft_mode', action='store_true',
                            help='Exception will not be raised if not all '
                                 'project models are registered')

    def handle(self, *args, **options):
        self.action = options['action']
        self.check_only = options['check_only']
        self.only = options['only']
        self.soft_mode = options['soft_mode']
        start = time.time()
        anonymizer = Anonymizer(
            soft_mode=self.soft_mode,
            only=self.only
        )
        self.stdout.write('Check pass successfully')
        self.stdout.write(f'{"=-" * 25}=')
        if self.check_only is True:
            return
        if self.action is None or self.action == 'anonymize':
            if (
                (self.only is None)
                or (self.only is not None
                    and self.only in Anonymizer.anonym_models)
            ) and len(anonymizer.anonym_models) > 0:
                self.stdout.write('Anonymizing started')
                anonymizer.anonymize(only=self.only)
                self.stdout.write('Anonymizing finished')
        if self.action is None or self.action == 'clean':
            if (
                (self.only is None)
                or (self.only is not None
                    and self.only in Anonymizer.clean_models)
            ) and len(anonymizer.clean_models) > 0:
                self.stdout.write('Cleaning started')
                anonymizer.clean(only=self.only)
                self.stdout.write('Cleaning finished')
        end = time.time() - start
        self.stdout.write(f'{"=-" * 25}=')
        self.stdout.write(f'Total time (sec.): {end:.2f}')
