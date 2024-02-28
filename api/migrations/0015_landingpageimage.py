# Generated by Django 4.2.9 on 2024-02-20 15:38

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0014_alter_productimage_thumbnail"),
    ]

    operations = [
        migrations.CreateModel(
            name="LandingPageImage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "image",
                    api.models.CloudFrontImageField(
                        help_text="upload your image here", upload_to=api.models.LowercaseRename("")
                    ),
                ),
                (
                    "thumbnail",
                    api.models.CloudFrontImageField(
                        blank=True,
                        default=None,
                        help_text="thumbnail of image",
                        null=True,
                        upload_to=api.models.LowercaseRename(""),
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["created_on"],
            },
        ),
    ]