# Generated by Django 2.0.7 on 2018-08-02 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0003_auto_20180802_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
