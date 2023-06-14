import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'movies.settings'
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = '1'
import django
django.setup()
from scripts.add_movie_data import *
from scripts.load_yaml_vars import LoadYamlVars


class ImportAllData(LoadYamlVars):

    def __init__(self, configuration_file):
        super().__init__(configuration_file)
        self.current_import_object = None

    def import_data(self):
        for import_class in self.class_dict_sorted_keys():
            print(f'Importing data from the import class {import_class}')
            self.current_import_object = import_class(self.import_class_dict().get(import_class))
            self.current_import_object.process_in_chunks()

    def import_class_dict(self):
        return {
            AddMovieTitle: self.merged_movie_title_path,
            AddMovieAka: self.get_path_from_config('aka.csv'),
            AddCrewData: self.get_path_from_config('crew.csv'),
            AddMovieCrew: self.get_path_from_config('movie_crew.csv'),
            AddMovieRating: self.get_path_from_config('ratings.csv'),
            AddMovieKeyword: self.get_path_from_config('keywords.csv'),
            AddMovieGenre: self.get_path_from_config('genres.csv'),
            AddMovieVideo: self.get_path_from_config('videos.csv'),
            AddMovieCountry: self.get_path_from_config('country.csv'),
            AddMovieCertificate: self.get_path_from_config('certificate.csv'),
            AddLink: self.get_path_from_config('merged_imdb_links.csv'),
            AddBoxOffice: self.get_path_from_config('box_office.csv'),
            AddCountry: self.get_path_from_config('country.csv'),
            AddSoundmix: self.get_path_from_config('soundmix.csv'),
            AddLanguage: self.get_path_from_config('single_language.csv'),
            AddGenre: self.get_path_from_config('single_genre.csv'),
            AddRegion: self.get_path_from_config('single_region.csv'),
            AddCertificate: self.get_path_from_config('single_certificate.csv'),
            AddKeyword: self.get_path_from_config('single_keyword.csv'),
        }

    def class_dict_sorted_keys(self):
        return [
            AddLanguage, AddMovieTitle, AddGenre, AddMovieGenre, AddRegion, AddMovieAka,
            AddCrewData, AddMovieCrew, AddMovieRating, AddLink, AddCountry, AddCertificate,
            AddKeyword, AddMovieKeyword, AddMovieCertificate, AddMovieVideo
        ]

    def get_path_from_config(self, file_name):
        return f'{self.output_data_directory}{file_name}'

def main():
    ImportAllData(os.environ.get('YAML_FILE')).import_data()


if __name__ == '__main__':
    main()

