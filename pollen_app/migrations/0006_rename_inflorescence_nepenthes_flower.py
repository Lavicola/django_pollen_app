# Generated by Django 3.2.12 on 2022-02-02 00:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pollen_app', '0005_nepenthes_sex'),
    ]

    operations = [
        migrations.RenameField(
            model_name='nepenthes',
            old_name='inflorescence',
            new_name='flower',
        ),
    ]
