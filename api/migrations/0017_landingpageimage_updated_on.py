# Generated by Django 4.2.9 on 2024-02-27 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0016_alter_menulistitem_menu_list"),
    ]

    operations = [
        migrations.AddField(
            model_name="landingpageimage",
            name="updated_on",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
