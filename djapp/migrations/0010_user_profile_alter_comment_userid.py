# Generated by Django 4.0.6 on 2022-12-14 14:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('djapp', '0009_alter_comment_postid_alter_comment_userid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile',
            field=models.FileField(default=1, upload_to='C:/Users/AKAM/Desktop/React/week2/djangoproject/reactapp/src/uploads/profile'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='userid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='used', to=settings.AUTH_USER_MODEL),
        ),
    ]