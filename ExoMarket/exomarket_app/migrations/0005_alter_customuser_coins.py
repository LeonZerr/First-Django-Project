# Generated by Django 5.1.3 on 2024-12-18 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("exomarket_app", "0004_transaction"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="coins",
            field=models.IntegerField(default=1000),
        ),
    ]