# Generated by Django 5.2 on 2025-07-10 01:29

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Diseases_For_Ai",
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
                (
                    "disease_name",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("topic", models.TextField(blank=True, null=True)),
                ("symptoms", models.TextField(blank=True, null=True)),
            ],
        ),
    ]
