# Generated by Django 3.2 on 2022-06-24 11:57

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import images.models
import images.validators
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Image",
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
                    "name",
                    models.CharField(
                        max_length=255,
                        unique=True,
                        validators=[
                            django.core.validators.MinLengthValidator(
                                3, "The field must contain at least 3 characters"
                            )
                        ],
                    ),
                ),
                ("file_uuid", models.UUIDField(default=uuid.uuid4, editable=False)),
                (
                    "image",
                    models.ImageField(
                        upload_to=images.models.content_file_name,
                        validators=[
                            images.validators.FileValidator(
                                content_types=("image/jpeg", "image/png"),
                                max_size=2073600,
                            )
                        ],
                    ),
                ),
                (
                    "original_image_link",
                    models.CharField(
                        blank=True, default="", max_length=2500, null=True
                    ),
                ),
                ("thumbnails_links", models.JSONField(blank=True, null=True)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
