
"""
Command to process and import and data
"""
import os
from django.core.management import BaseCommand
from scripts.import_all_data import ImportAllData
from movie_project.all_processes import RunAllProcesses
class Command(BaseCommand): 
    """Django command to import and process data""" 
    def handle(self, *args, **options): 
        yaml_file = os.environ.get('YAML_FILE')
        self.stdout.write("Processing data") 
        RunAllProcesses(yaml_file).run_everything()
        self.stdout.write("Importing data") 
        ImportAllData(yaml_file).import_data()