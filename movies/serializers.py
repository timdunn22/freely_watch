from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from movies.documents import MovieDocument


class MovieDocumentSerializer(DocumentSerializer):
    class Meta:
        document = MovieDocument
        fields = (
            'tconst',
            'primary_title',
            'original_title',
            'start_year',
            'title_type',
            'is_adult',
            'runtime_minutes',
            'aspect_ratio',
            'top_250_rank',
            'bottom_100_rank',
            'box_office_cumulative_worldwide_groess',
            'box_office_budget',
            'color',
            'plot_outline',
            'score',
            'production_status',
            'production_status_updated',
            'poster',
            'language',
            'akas',
            'keywords',
            'genres',
            'crew',
            'rating',
            'links',
            'certificates',
            'videos',
        )
