import csv
from django.core.management.base import BaseCommand
from iris_app.models import Iris

class Command(BaseCommand):
    help = 'Import Iris dataset from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']
        
        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                iris = Iris(
                    sepal_length=row['sepal_length'],
                    sepal_width=row['sepal_width'],
                    petal_length=row['petal_length'],
                    petal_width=row['petal_width'],
                    species=row['species']
                )
                iris.save()

        self.stdout.write(self.style.SUCCESS('Successfully imported Iris dataset'))
