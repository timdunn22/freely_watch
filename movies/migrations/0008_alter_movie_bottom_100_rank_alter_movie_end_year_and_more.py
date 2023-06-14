# Generated by Django 4.1.7 on 2023-03-24 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movies", "0007_rename_birthyear_crew_birth_year_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="movie",
            name="bottom_100_rank",
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name="movie",
            name="end_year",
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name="movie",
            name="runtime_minutes",
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name="movie",
            name="start_year",
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name="movie",
            name="top_250_rank",
            field=models.IntegerField(default=0, null=True),
        ),
    ]
