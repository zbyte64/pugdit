from django.core.management.base import BaseCommand, CommandError
from pugdit.postoffice.mailtruck import put_advertisement, drive_route, explore_new_routes, publish_manifest, trucking_pool


class Command(BaseCommand):
    help = 'Retrieve and deliver posts'

    def add_arguments(self, parser):
        parser.add_argument(
            '--skip-publish',
            action='store_false',
            dest='publish',
            default=True,
            help='Skip publishing manifest',
        )
        parser.add_argument(
            '--skip-explore',
            action='store_false',
            dest='explore',
            default=True,
            help='Skip exploring new routes',
        )
        parser.add_argument(
            '--skip-route',
            action='store_false',
            dest='route',
            default=True,
            help='Skip previous routes',
        )

    def handle(self, *args, **options):
        put_advertisement()
        if options['publish']:
            publish_manifest()
        if options['route']:
            drive_route()
        if options['explore']:
            explore_new_routes()
        trucking_pool.waitall()
        #self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))
