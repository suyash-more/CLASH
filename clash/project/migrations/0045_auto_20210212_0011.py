# Generated by Django 3.1 on 2021-02-11 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0044_register_tab'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='question',
            field=models.TextField(blank=True),
        ),
    ]
