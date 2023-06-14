# Generated by Django 4.1.7 on 2023-03-28 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movies", "0016_alter_crew_primary_name_alter_movieaka_attributes_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movie",
            name="aspect_ratio",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="movie",
            name="color",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="movie",
            name="poster",
            field=models.URLField(max_length=400, null=True),
        ),
    ]
