# Generated by Django 2.2 on 2021-03-08 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='lecture_date',
            field=models.DateTimeField(null=True),
        ),
    ]
