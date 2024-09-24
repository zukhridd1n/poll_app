# Generated by Django 5.1.1 on 2024-09-11 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="account",
            name="interests",
        ),
        migrations.AddField(
            model_name="accountprofile",
            name="interests",
            field=models.ManyToManyField(
                related_name="accounts", to="account.interest"
            ),
        ),
    ]
