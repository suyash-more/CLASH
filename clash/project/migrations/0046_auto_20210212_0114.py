# Generated by Django 3.1 on 2021-02-11 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0045_auto_20210212_0011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='question',
            field=models.CharField(blank=True, max_length=5000),
        ),
        migrations.AlterField(
            model_name='register',
            name='tab',
            field=models.IntegerField(default=100),
        ),
    ]
