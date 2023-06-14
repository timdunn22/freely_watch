from django.db import models
from django.db.models import F, OuterRef, Func
from django_elasticsearch_dsl_drf.wrappers import dict_to_obj
import json
import numpy as np
from movies.languages import *

def flatten(*args):
    return [item for sublist in [convert_list(arg) for arg in args] for item in sublist]

def convert_list(arg):
    if type(arg) == list:
        return arg
    return [arg]

def is_related(field):
    return 'related' in str(field.__class__).split('models.fields')[-1]

def embedded_link_urls():
    return ["https://youtube.com", "https://archive.org", "https://ok.ru/video"]

def possible_qualities():
    return ['1080p', '4K', '720p', 'CAM', 'DH', 'DVD', 'DVD Rip', 'Dvd Scr', 'HD', 
            'HD CAM', 'HD RIP', 'HDRip', 'SD', 'TC', 'TS', 'WebRip', 'cam', 'hd']

def hd_qualities():
    return [quality for quality in possible_qualities() if '1080' in quality or 'hd' in quality.lower()]

def cam_qualities():
    return [quality for quality in possible_qualities() if 'cam' in quality.lower()]

def sd_qualities():
    return [quality for quality in possible_qualities() if (quality not in 
                                                            flatten(hd_qualities(), cam_qualities(), '4K', '720p'))]

def quality_filtering_args():
    return ["4K", hd_qualities(), "720p", sd_qualities(), 
            {"quality__isnull": True}, cam_qualities()]

class AddMethods(models.Model):

    @classmethod
    def local_attributes(cls):
        return [field.attname for field in cls._meta.local_fields if not is_related(field)]

    class Meta:
        abstract = True


class NameModel(AddMethods):
    name = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True



class Language(NameModel):
    code = models.CharField(max_length=10, null=True)

    @classmethod
    def cleanup(cls):
        for language in cls.objects.all():
            code = TO_LANGUAGE_CODE.get(language.name.lower())
            language.code = code
            if code is not None:
                language.save
            
        unique_languages = [language.get('name').lower() for language in cls.objects.values('name')]
        cls.objects.bulk_create([cls(**{"name": language.capitalize(), "code": TO_LANGUAGE_CODE.get(language)})
                                 for language in TO_LANGUAGE_CODE.keys() 
                                 if language not in unique_languages])
        for link in Link.objects.filter(audio_language__name__in=list(LANGUAGES.keys())):
            link.audio_language = Language.objects.get(name=LANGUAGES.get(link.audio_language.name.lower()).capitalize())
            link.save
        cls.objects.filter(name__in=list(LANGUAGES.keys())).delete()



class Region(NameModel):
    pass


class Genre(NameModel):
    pass

class MainMovieManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(title_type__in=['movie', 'tvMovie', 'video'], 
                                             link__isnull=False).distinct(
            'tconst').order_by('tconst').select_related()

class Movie(AddMethods):
    TITLE_TYPES = [
        ('movie', 'movie'),
        ('tvMovie', 'tvMovie'),
        ('video', 'video')
    ]
    tconst = models.CharField(unique=True, max_length=10)
    title_type = models.CharField(choices=TITLE_TYPES, max_length=255)
    primary_title = models.TextField()
    original_title = models.TextField()
    is_adult = models.BooleanField(null=True, default=False)
    start_year = models.IntegerField(null=True, default=0)
    end_year = models.IntegerField(null=True, default=0)
    runtime_minutes = models.IntegerField(null=True, default=0)
    aspect_ratio = models.TextField(null=True)
    bottom_100_rank = models.IntegerField(null=True, default=0)
    top_250_rank = models.IntegerField(null=True, default=0)
    top_indian_rank = models.IntegerField(null=True, default=0)
    top_popular_rank = models.IntegerField(null=True, default=0)
    box_office_budget = models.CharField(max_length=255, null=True)
    box_office_cumulative_worldwide_gross = models.CharField(max_length=255, null=True)
    color = models.TextField(null=True)
    original_air_date = models.CharField(max_length=255, null=True)
    plot_outline = models.TextField(null=True)
    poster = models.URLField(null=True, max_length=400)
    production_status = models.CharField(max_length=255, null=True)
    production_status_updated = models.CharField(max_length=255, null=True)
    score = models.FloatField(default=0, null=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True)
    main_movies = MainMovieManager()

    class Meta:
        ordering = ["-box_office_budget"]

    def __str__(self):
        return self.primary_title

    def language_value(self):
        try:
            return str(self.language.name)
        except:
            return None

    def rating_value(self):
        try:
            return self.movierating_set.order_by('-num_votes')[0].average_rating
        except:
            return None
    
    def num_votes_value(self):
        try:
            return self.movierating_set.order_by('-num_votes')[0].num_votes
        except:
            return None

    def best_quality_value(self):
        try:
            qualities =  np.unique(self.link_set.only('quality'))
            if "4K" in qualities:
                return "4K"
            elif "HD" in qualities:
                return "HD"
            elif "720p" in qualities:
                return "720p"
            elif "CAM" in qualities:
                return "CAM"
            else:
                return "SD"
        except:
            return None

    def embeded_language_link_value(self, language, language_object):
        return self.embeded_link_general_language({'audio_language': language}, language_object, language.name)

    def embeded_link_general_language(self, language_argument, language_object, language_key):
        for filtering_arg in quality_filtering_args():
            args = {"quality": filtering_arg}
            if type(filtering_arg) == dict:
                args = filtering_arg
            args.update(language_argument)
            links = self.link_set.filter(**args)
            if len(links) > 0:
                for link_type in embedded_link_urls():
                    link_type_links = links.filter(link_url__startswith=link_type)
                    if ( len(link_type_links) > 0 ) and not language_object.get(language_key):
                        return link_type_links[0].link_url


    def embeded_link_value(self):
        language_object = dict()
        languages_available = [link.audio_language for link in self.link_set.filter(audio_language__isnull=False)]
        for language in languages_available:
            language_object[language.name] = self.embeded_language_link_value(language, language_object)

        null_language = self.embeded_link_general_language({"audio_language__isnull": True}, 
                                                           language_object, 'null_language')
        language_object['null_language'] = null_language
        return language_object

    def best_link_value(self):
        best_link = self.link_set.filter(quality_isnull=False)
        for filtering_arg in quality_filtering_args():
            args = {"quality": filtering_arg}
            if type(filtering_arg) == dict:
                args = filtering_arg
            args.update(language_argument)
            links = self.link_set.filter(**args)
            if len(links) > 0:
                if ( len(links) > 0 ) and not language_object.get(language_key):
                    return link_type_links[0].link_url




    def get_akas(self):
        return [aka.title for aka in self.movieaka_set.distinct('title')]
    
    def get_genres(self):
        return [movie_genre.genre.name for movie_genre in self.moviegenre_set.distinct('genre_id')]

    def get_keywords(self):
        return [movie_keyword.keyword.name for movie_keyword in self.moviekeyword_set.distinct('keyword_id')]

    def get_videos(self):
        return [video.video_url for video in self.movievideo_set.distinct('video_url')]

    def get_movie_crew(self):
        return [movie_crew for movie_crew in self.moviecrew_set.all()]

    def get_ratings(self):
        return [rating for rating in self.movierating_set.all()]
    
    def get_links(self):
        return [link for link in self.link_set.all()]
    
    def get_certificates(self):
        return [certificate for certificate in self.moviecertificate_set.all()]



class HasMovieModel(AddMethods):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class MovieGenre(HasMovieModel):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    ordering = models.IntegerField()
    top_50_rank = models.IntegerField(default=0, null=True)


class MovieSoundMix(HasMovieModel, NameModel):
    pass


class MovieAka(HasMovieModel):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True)
    is_original_title = models.BooleanField(null=True)
    ordering = models.IntegerField(default=True, null=True)
    types = models.CharField(max_length=255)
    attributes = models.TextField(max_length=255, null=True)
    title = models.TextField(max_length=255)

    def __str__(self):
        return self.title


class HasMovieAka(AddMethods):
    movie_aka = models.ForeignKey(MovieAka, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Crew(AddMethods):
    nconst = models.CharField(max_length=10)
    primary_name = models.TextField(default='unknown')
    primary_profession = models.CharField(max_length=255, default='unknown', null=True)
    birth_year = models.IntegerField(null=True)
    death_year = models.IntegerField(null=True)



class HasCrewModel(AddMethods):
    crew = models.ForeignKey(Crew, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class MovieCrew(HasMovieModel, HasCrewModel):
    ordering = models.IntegerField()
    category = models.TextField(null=True)
    job = models.TextField(null=True)
    characters = models.JSONField(null=True)
    
    def get_crew(self):
        return self.crew

    def get_characters(self):
        try:
            return json.loads(self.characters)
        except:
            return list()


class MovieRating(HasMovieModel):
    average_rating = models.FloatField()
    num_votes = models.IntegerField()


class Link(AddMethods):
    movie = models.ForeignKey(Movie, null=True, on_delete=models.CASCADE)
    attributes = models.JSONField(null=True)
    data_source = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    link_url = models.URLField(unique=True, null=True, max_length=400)
    duration = models.IntegerField(null=True)
    year = models.IntegerField(null=True)
    fps = models.IntegerField(null=True)
    image_url = models.TextField(null=True)
    quality = models.CharField(max_length=255, null=True)
    resolution = models.CharField(max_length=255, null=True)
    fulltitle = models.TextField(null=True)
    audio_language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True)
    audio_language_probability = models.FloatField(null=True)
    subtitles = models.TextField(null=True)
    
    def audio_language_value(self):
        try:
            return str(self.audio_language.name)
        except:
            return None


class IsPrimaryModel(AddMethods):
    is_primary = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Country(NameModel):
    code = models.CharField(max_length=255)


class MovieBoxOfficeOpening(HasMovieModel):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    amount = models.CharField(max_length=255)


class MovieCountry(HasMovieAka, IsPrimaryModel):
    country = models.ForeignKey(Country, default='None', on_delete=models.CASCADE)


class Certificate(NameModel):
    pass


class Keyword(NameModel):
    pass


class MovieKeyword(HasMovieModel):
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    ordering = models.IntegerField(default=1)


class MovieCertificate(HasMovieModel):
    certificate = models.ForeignKey(Certificate, on_delete=models.CASCADE, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    version = models.TextField(null=True)

    def get_certificate(self):
        try:
            return self.certificate.name
        except:
            return None

    def get_country(self):
        try:
            return self.country.name
        except:
            return None


class MovieVideo(HasMovieModel):
    video_url = models.URLField()
    ordering = models.IntegerField(default=1)
