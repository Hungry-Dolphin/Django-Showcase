# Generated by Django 3.1.1 on 2020-10-07 18:38

from django.db import migrations, models
import library.models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial_squashed_0004_auto_20201007_2016'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comments',
            options={'verbose_name': 'Comments'},
        ),
        migrations.AlterField(
            model_name='book',
            name='pdf',
            field=models.FileField(upload_to=library.models.upload, validators=[library.models.check_extension, library.models.check_size]),
        ),
    ]