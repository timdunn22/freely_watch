
"""
Command to import all data from converted data directory
"""
import os
from django.core.management import BaseCommand
from scripts.import_all_data import ImportAllData
class Command(BaseCommand): 
    """Django command to import data""" 
    def handle(self, *args, **options): 
        self.stdout.write("Importing data") 
        ImportAllData(os.environ.get('YAML_FILE')).import_data()