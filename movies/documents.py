# import os

# os.environ['DJANGO_SETTINGS_MODULE'] = 'movies.settings'
# os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = '1'

# import django
# django.setup()
from django_elasticsearch_dsl import (Document, fields, Index)
from django_elasticsearch_dsl.registries import registry
from .models import *
import json

# movie = Index('movies')
# movie.settings(
#     number_of_shards=1,
#     number_of_replicas=0
# )

@registry.register_document
# @movie.document
class MovieDocument(Document):
    language = fields.KeywordField(attr='language_value')
    links = fields.ObjectField(attr="get_links", properties={
        "fulltitle": fields.TextField(),
        "link_url": fields.TextField(),
        "fps": fields.IntegerField(),
        "quality": fields.TextField(),
        "audio_language": fields.KeywordField(attr="audio_language_value")
    })
    certificates = fields.ObjectField(attr="get_certificates", properties={
        "certificate": fields.TextField(attr="get_certificate"),
        "country": fields.TextField(attr="get_country"),
        "version": fields.TextField()
    })
    num_votes = fields.IntegerField(attr='num_votes_value')
    rating = fields.FloatField(attr='rating_value')
    videos = fields.ListField(fields.TextField())
    genres = fields.ListField(fields.KeywordField())
    keywords = fields.ListField(fields.TextField())
    akas = fields.ListField(fields.TextField())
    akas_suggest = fields.ListField(fields.CompletionField(attr='get_akas'))
    primary_title = fields.TextField(fields={'raw': fields.TextField(), 
                                             'suggest': fields.CompletionField(), 'keyword': fields.KeywordField()})
    title_type = fields.KeywordField()
    color = fields.KeywordField()
    best_quality = fields.KeywordField(attr="best_quality_value")
    best_embeded_links = fields.ObjectField(attr="embeded_link_value")
    crew = fields.ObjectField(attr="get_movie_crew", properties={
        "ordering": fields.IntegerField(),
        "category": fields.TextField(),
        "job": fields.TextField(),
        "characters": fields.ListField(fields.TextField(attr='get_characters')),
        "basic_info": fields.ObjectField(
            attr="get_crew",
            properties={
                "nconst": fields.TextField(),
                "primary_name": fields.TextField(fields={'raw': fields.TextField(), 
                                                         "keyword": fields.KeywordField(), 
                                                         "suggest": fields.CompletionField()}),
                "primary_profession": fields.TextField(),
                "birth_year": fields.IntegerField(),
                "death_year": fields.IntegerField()
            }
        )
    })

    def prepare_akas(self, instance):
        return [aka.title for aka in instance.movieaka_set.distinct('title')]
    
    def prepare_keywords(self, instance):
        return [movie_keyword.keyword.name for movie_keyword in instance.moviekeyword_set.distinct('keyword_id')]
    
    def prepare_genres(self, instance):
        return [movie_genre.genre.name for movie_genre in instance.moviegenre_set.distinct('genre_id')]
    
    def prepare_videos(self, instance):
        return [video.video_url for video in instance.movievideo_set.distinct('video_url')]

    def prepare_color(self, instance):
        full_color = str(instance.color).lower()
        if 'color' in full_color:
            return 'color'
        elif 'black' in full_color:
            return 'black and white'
        return None

    def get_instances_from_related(self, related_instance):
        return self

    class Index:
        name = 'movies'

    class Django:
        model = Movie
        fields = [field for field in Movie.local_attributes() if field not in ['primary_title', 'title_type', 'color']]
        related_models = [Language, MovieAka, MovieCrew, MovieRating, MovieGenre, 
                          Link, MovieKeyword, MovieBoxOfficeOpening, MovieCertificate, 
                          MovieCountry, MovieSoundMix, MovieVideo]
        
        def get_queryset(self):
            return Movie.main_movies