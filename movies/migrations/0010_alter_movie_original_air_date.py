# Generated by Django 4.1.7 on 2023-03-24 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movies", "0009_alter_movie_aspect_ratio_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movie",
            name="original_air_date",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
