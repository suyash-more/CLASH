# Generated by Django 3.1 on 2021-01-28 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0043_register_permit'),
    ]

    operations = [
        migrations.AddField(
            model_name='register',
            name='tab',
            field=models.IntegerField(default=2),
        ),
    ]
