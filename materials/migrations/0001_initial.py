# Generated by Django 5.1.3 on 2024-11-12 09:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=150, verbose_name="название")),
                (
                    "picture",
                    models.ImageField(upload_to="images/", verbose_name="превью(картинка)"),
                ),
                (
                    "description",
                    models.TextField(max_length=350, verbose_name="название"),
                ),
            ],
            options={
                "verbose_name": "курс",
                "verbose_name_plural": "курсы",
                "ordering": ["title"],
            },
        ),
        migrations.CreateModel(
            name="Lesson",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=150, verbose_name="название")),
                (
                    "description",
                    models.TextField(max_length=500, verbose_name="название"),
                ),
                (
                    "picture",
                    models.ImageField(upload_to="images/", verbose_name="превью(картинка)"),
                ),
                ("video_link", models.URLField()),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lessons",
                        to="materials.course",
                    ),
                ),
            ],
        ),
    ]
