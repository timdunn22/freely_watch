# from common_methods import flatten
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'movies.settings'
# os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = '1'
import django
django.setup()
from scripts.data_to_db import DataToDb

from movies.models import (MovieAka, Crew, MovieCrew, MovieRating, Link, Genre, Region, Certificate,
                           MovieCountry, MovieGenre, Country, MovieKeyword, Language, Keyword,
                           MovieCertificate, MovieVideo, Movie, MovieBoxOfficeOpening)


# class AddMovieTypeData(DataToDb):
#     def __init__(self, import_file_path, model_name):
#         self.foreign_models = [{"movie": "tconst"}]
#         super().__init__(model_name, import_file_path, foreign_models=self.foreign_models)


class AddMovieTitle(DataToDb):

    def __init__(self, import_file_path):
        self.foreign_models = [{"language": "name"}]
        super().__init__(model_class=Movie, file_path=import_file_path,
                         foreign_models=self.foreign_models, identity=['tconst'])


class AddMovieAka(DataToDb):

    def __init__(self, import_file_path):
        self.foreign_models = [{"movie": "tconst"}, {"language": "name"}, {"region": "name"}]
        super().__init__(MovieAka, import_file_path, identity=['movie', 'ordering'],
                         foreign_models=self.foreign_models)


class AddCrewData(DataToDb):

    def __init__(self, import_file_path):
        super().__init__(Crew, import_file_path, identity=['nconst'])


class AddMovieCrew(DataToDb):

    def __init__(self, import_file_path):
        self.foreign_models = [{"crew": "nconst"}, {"movie": "tconst"}]
        super().__init__(MovieCrew, import_file_path, foreign_models=self.foreign_models,
                         identity=['movie', 'crew'])


class AddMovieRating(DataToDb):

    def __init__(self, import_file_path):
        self.foreign_models = [{"movie": "tconst"}]
        super().__init__(MovieRating, import_file_path, foreign_models=self.foreign_models,
                         identity=['movie', 'num_votes'])


class AddMovieKeyword(DataToDb):

    def __init__(self, import_file_path):
        self.foreign_models = [{"movie": "tconst"}, {"keyword": "name"}]
        super().__init__(MovieKeyword, import_file_path, foreign_models=self.foreign_models,
                         identity=['movie', 'keyword'])


class AddMovieGenre(DataToDb):

    def __init__(self, import_file_path):
        self.foreign_models = [{"movie": "tconst"}, {"genre": "name"}]
        super().__init__(MovieGenre, import_file_path, foreign_models=self.foreign_models, 
                         identity=['movie', 'genre'])


class AddMovieVideo(DataToDb):

    def __init__(self, import_file_path):
        self.foreign_models = [{"movie": "tconst"}]
        super().__init__(MovieVideo, import_file_path, foreign_models=self.foreign_models,
                         identity=['movie', 'video_url'])


class AddCountry(DataToDb):

    def __init__(self, import_file_path):
        super().__init__(Country, import_file_path, identity=['name'])


class AddLanguage(DataToDb):

    def __init__(self, import_file_path):
        super().__init__(Language, import_file_path, identity=['name'])


class AddKeyword(DataToDb):

    def __init__(self, import_file_path):
        super().__init__(Keyword, import_file_path, identity=['name'])


class AddGenre(DataToDb):

    def __init__(self, import_file_path):
        super().__init__(Genre, import_file_path, identity=['name'])


class AddRegion(DataToDb):

    def __init__(self, import_file_path):
        super().__init__(Region, import_file_path, identity=['name'])


class AddCertificate(DataToDb):

    def __init__(self, import_file_path):
        super().__init__(Certificate, import_file_path, identity=['name'])


class AddMovieCountry(DataToDb):

    def __init__(self, import_file_path):
        self.foreign_models = [{"movie": "tconst"}, {"country": "name"}]
        super().__init__(MovieCountry, import_file_path, foreign_models=self.foreign_models,
                         identity=['movie', 'country'])


class AddMovieCertificate(DataToDb):

    def __init__(self, import_file_path):
        self.foreign_models = [{"movie": "tconst"}, {"certificate": "name"}, {"country": "name"}]
        super().__init__(MovieCertificate, import_file_path, foreign_models=self.foreign_models,
                         identity=['movie', 'certificate'])


class AddLink(DataToDb):

    def __init__(self, import_file_path):
        self.foreign_models = [{"movie": "tconst"}, {"audio_language": "name"}]
        super().__init__(Link, import_file_path, foreign_models=self.foreign_models, identity=['link_url'])


class AddBoxOffice(DataToDb):

    def __init__(self, import_file_path):
        self.foreign_models = [{"movie": "tconst"}, {"country": "name"}]
        super().__init__(MovieBoxOfficeOpening, import_file_path, foreign_models=self.foreign_models,
                         identity=[], all_update=True)


class AddSoundmix(DataToDb):

    def __init__(self, import_file_path):
        self.foreign_models = [{"movie": "tconst"}]
        super().__init__(MovieBoxOfficeOpening, import_file_path, foreign_models=self.foreign_models,
                         identity=[], all_update=True)

