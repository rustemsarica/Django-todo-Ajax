# Generated by Django 3.2 on 2022-07-20 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='working_hours',
            field=models.CharField(choices=[('half', '0.5'), ('full', '1')], max_length=5),
        ),
    ]
