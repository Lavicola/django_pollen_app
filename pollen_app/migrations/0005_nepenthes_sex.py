# Generated by Django 3.2.12 on 2022-02-01 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pollen_app', '0004_auto_20220201_2337'),
    ]

    operations = [
        migrations.AddField(
            model_name='nepenthes',
            name='sex',
            field=models.CharField(choices=[('0', 'male '), ('1', 'female'), ('2', 'unkown')], default='2', max_length=2),
        ),
    ]
