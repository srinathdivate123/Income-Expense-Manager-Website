# Generated by Django 4.0.5 on 2022-08-23 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userincome', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userincome',
            name='source',
            field=models.TextField(max_length=256),
        ),
    ]
