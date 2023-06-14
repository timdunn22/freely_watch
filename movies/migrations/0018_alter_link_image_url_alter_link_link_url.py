# Generated by Django 4.1.7 on 2023-03-29 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movies", "0017_alter_movie_aspect_ratio_alter_movie_color_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="link",
            name="image_url",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="link",
            name="link_url",
            field=models.URLField(max_length=400, null=True, unique=True),
        ),
    ]