from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_RANGE,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
    SUGGESTER_COMPLETION,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    DefaultOrderingFilterBackend,
    FilteringFilterBackend,
    SearchFilterBackend,
    OrderingFilterBackend,
    SuggesterFilterBackend,
    NestedFilteringFilterBackend,
)
from django_elasticsearch_dsl_drf.pagination import LimitOffsetPagination
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from movies.documents import MovieDocument
from movies.serializers import MovieDocumentSerializer
# import requests
from rest_framework import generics, permissions

# class ApiIndexView(generics.ListCreateAPIView):
#     permission_classes = (permissions.AllowAny,)

#     def post(self, request, pk):
#         return requests.post('http://localhost:9200/_search/', data=request.data).text

#     def allowed_methods(self):
#         """
#         Return the list of allowed HTTP methods, uppercased.
#         """
#         self.http_method_names.append("post")
#         return [method.upper() for method in self.http_method_names
#                 if hasattr(self, method)]

class MovieViewSet(DocumentViewSet):
    document = MovieDocument
    serializer_class = MovieDocumentSerializer
#     ordering = 'id'
    lookup_field = 'id'

    filter_backends = [
        DefaultOrderingFilterBackend,
        FilteringFilterBackend,
        SearchFilterBackend,
        # OrderingFilterBackend,
        # NestedFilteringFilterBackend,
        SuggesterFilterBackend,
    ]
    pagination_class = LimitOffsetPagination

    search_fields = ( 
        'primary_title', 
        'keywords', 
        'crew.basic_info.primary_name', 
        'language',
        'genres'
    )

    search_options = {
        "default_operator": "and",
    }

    filter_fields = {
        'id': {
            'field': 'id',
            'lookups': [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
            ],
        },
        'genres': {'field': 'genres'},
        'language': 'language.name',
        'color': 'color',
        'average_rating': {
            'field': 'rating.average_rating.raw',
            'lookups': [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
            ]
        },
        'num_votes':{
            'field': 'rating.num_votes.raw',
            'lookups': [
                LOOKUP_FILTER_RANGE,
                LOOKUP_QUERY_IN,
                LOOKUP_QUERY_GT,
                LOOKUP_QUERY_GTE,
                LOOKUP_QUERY_LT,
                LOOKUP_QUERY_LTE,
            ]
        },
        'quality': 'links.quality.raw',
        'audio_language': 'links.audio_language.raw',
        'certificate': 'certificates.certificate.raw',
        'aspect_ratio': 'aspect_ratio',
        'year': 'start_year',
        'title': 'primary_title',
        'is_adult': 'is_adult',
        'title_type': 'title_type',
        'runtime_minutes': 'runtime_minutes',
        'top_250_rank': 'top_250_rank',
        'bottom_100_rank': 'bottom_100_rank',
        'box_office_cumulative_worldwide_groess': 'box_office_cumulative_worldwide_groess',
        'box_office_budget': 'box_office_budget',
        'score': 'score',
        'alternative_title': 'akas'
    }

    suggester_fields = {
        'name_suggest': {
            'field': 'primary_title.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
    }
