# Generated by Django 4.0.6 on 2023-01-27 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djapp', '0027_rename_is_verified_user_is_bussiness'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_verfied',
            field=models.BooleanField(default=False),
        ),
    ]
