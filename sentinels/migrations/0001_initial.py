# Generated by Django 3.2.9 on 2021-12-07 04:03

import uuid

import django_extensions.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Sentinel",
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
                ("title", models.CharField(max_length=50)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="SentinelSlugged",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                (
                    "slug",
                    django_extensions.db.fields.AutoSlugField(
                        blank=True, editable=False, populate_from=["title"]
                    ),
                ),
                ("title", models.CharField(max_length=50)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
