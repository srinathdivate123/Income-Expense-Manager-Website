# Generated by Django 4.1.1 on 2022-09-21 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userpreferences', '0003_rename_showtouser_sharepreference'),
    ]

    operations = [
        migrations.AddField(
            model_name='sharepreference',
            name='SeeingFrom',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
