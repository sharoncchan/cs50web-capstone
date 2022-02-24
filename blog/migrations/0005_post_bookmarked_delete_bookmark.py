# Generated by Django 4.0 on 2022-02-07 11:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_category_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='bookmarked',
            field=models.ManyToManyField(related_name='bookmarks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Bookmark',
        ),
    ]