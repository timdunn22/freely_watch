from django.contrib import admin

from movies.models import (
    Language, Region, Genre, MovieGenre, Movie, MovieAka, MovieCrew,
    MovieVideo, MovieRating, Crew, Country, Certificate, Link, MovieCountry,
    MovieCertificate, MovieKeyword, MovieSoundMix, MovieBoxOfficeOpening, Keyword
)

models_to_register = [Language, Region, Genre, MovieGenre, Movie, MovieAka, MovieCrew,
                      MovieVideo, MovieRating, Crew, Country, Certificate, Link, MovieCountry,
                      MovieCertificate, MovieKeyword, MovieSoundMix, MovieBoxOfficeOpening, Keyword]

for model in models_to_register:
    admin.site.register(model)
