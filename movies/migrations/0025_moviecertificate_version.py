# Generated by Django 4.1.7 on 2023-04-03 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movies", "0024_moviekeyword_ordering_alter_movievideo_ordering"),
    ]

    operations = [
        migrations.AddField(
            model_name="moviecertificate",
            name="version",
            field=models.TextField(null=True),
        ),
    ]
