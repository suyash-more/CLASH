# Generated by Django 3.1 on 2020-10-18 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0016_auto_20201018_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='freezetimestart',
            field=models.TimeField(blank=True, null=True),
        ),
    ]