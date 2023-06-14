import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'movies.settings'

import django
django.setup()
from all_processes.convert_all_data import ConvertAllData
from import_all_data import ImportAllData


class ConvertImportData:

    def __init__(self, configuration_file, force_update=False):
        self.configuration_file = configuration_file
        self.force_update = force_update

    def import_data(self):
        ImportAllData(self.configuration_file).import_data()

    def convert_all_data(self):
        ConvertAllData(self.configuration_file, force_update=self.force_update).convert_data()

    def convert_and_import(self):
        self.convert_all_data()
        self.import_data()


def main():
    ConvertImportData(os.environ.get('YAML_FILE'), force_update=True).convert_and_import()


if __name__ == '__main__':
    main()
