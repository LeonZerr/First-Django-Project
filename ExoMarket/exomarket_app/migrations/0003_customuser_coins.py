# Generated by Django 5.1.3 on 2024-12-17 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("exomarket_app", "0002_alter_item_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="coins",
            field=models.IntegerField(default=500),
        ),
    ]