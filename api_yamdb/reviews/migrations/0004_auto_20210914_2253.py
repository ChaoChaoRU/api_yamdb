# Generated by Django 2.2.16 on 2021-09-14 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20210914_1933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(blank=True, db_index=True, to='reviews.Genre'),
        ),
        migrations.AlterField(
            model_name='title',
            name='name',
            field=models.CharField(db_index=True, max_length=256, unique=True, verbose_name='Название'),
        ),
    ]
