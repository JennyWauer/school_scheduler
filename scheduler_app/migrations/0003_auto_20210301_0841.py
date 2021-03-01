# Generated by Django 2.2 on 2021-03-01 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler_app', '0002_auto_20210228_1053'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=45)),
                ('description', models.TextField()),
                ('due_date', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RenameModel(
            old_name='subjects',
            new_name='Subject',
        ),
        migrations.DeleteModel(
            name='assignments',
        ),
        migrations.AddField(
            model_name='assignment',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject_assignments', to='scheduler_app.Subject'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posted_assignment', to='scheduler_app.Users'),
        ),
    ]
