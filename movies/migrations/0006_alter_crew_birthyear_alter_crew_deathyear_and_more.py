# Generated by Django 4.1.7 on 2023-03-23 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movies", "0005_alter_link_movie"),
    ]

    operations = [
        migrations.AlterField(
            model_name="crew",
            name="birthYear",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="crew",
            name="deathYear",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="link",
            name="audio_language_probability",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="link",
            name="data_source",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="link",
            name="description",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="link",
            name="duration",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="link",
            name="fps",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="link",
            name="fulltitle",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="link",
            name="image_url",
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name="link",
            name="link_url",
            field=models.URLField(null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="link",
            name="quality",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="link",
            name="resolution",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="link",
            name="subtitles",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="link",
            name="year",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="movie",
            name="bottom_100_rank",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="movie",
            name="box_office_budget",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="movie",
            name="box_office_cumulative_worldwide_gross",
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name="movie",
            name="color",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="movie",
            name="end_year",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="movie",
            name="is_adult",
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name="movie",
            name="original_air_date",
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name="movie",
            name="plot_outline",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="movie",
            name="poster",
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name="movie",
            name="production_status",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="movie",
            name="runtime_minutes",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="movie",
            name="start_year",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="movie",
            name="top_250_rank",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="movieaka",
            name="attributes",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="movieaka",
            name="is_original_title",
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name="movieaka",
            name="ordering",
            field=models.IntegerField(default=True, null=True),
        ),
        migrations.AlterField(
            model_name="moviecrew",
            name="category",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="moviecrew",
            name="characters",
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name="moviecrew",
            name="job",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
