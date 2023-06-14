from rest_framework import routers
from django.urls import include, path
from movies.views import MovieViewSet

from movies import elastic_views


app_name = 'movies'

router = routers.DefaultRouter()
# router.register(r'^movies/_search/', views.ApiIndexView, basename='index')
router.register(r'movies', MovieViewSet, basename='movie')
urlpatterns = [
    path('', include(router.urls)),
]
