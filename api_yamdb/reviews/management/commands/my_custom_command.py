from django.core.management.base import BaseCommand
from django.db.models import loading
# from django.db.models import get_app, get_models
# from django.apps import apps as django_apps
# from django.apps import apps
# from apps import loading, get_model

import csv


class Command(BaseCommand):
    help = 'Creating model objects according the file path specified'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str, help="file path")
        parser.add_argument('--model_name', type=str, help="model name")
        parser.add_argument(
            '--app_name', type=str,
            help="django app name that the model is connected to")

    def handle(self, *args, **options):
        file_path = options['path']
        _model = loading.get_model(options['app_name'], options['model_name'])
        with open(file_path, 'rb') as csv_file:
            reader = csv.reader(csv_file, delimiter=',', quotechar='|')
            header = reader.next()
            for row in reader:
                _object_dict = {key: value for key, value in zip(header, row)}
                _model.objects.create(**_object_dict)
