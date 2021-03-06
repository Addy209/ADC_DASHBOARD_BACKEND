# Generated by Django 3.2.5 on 2021-07-31 19:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('constants', '0003_auto_20210731_1305'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=511)),
                ('description', models.TextField()),
                ('requestedby', models.CharField(max_length=255)),
                ('dev_complete_date', models.DateField()),
                ('dev_completed', models.BooleanField()),
                ('test_start_date', models.DateField()),
                ('test_complete_date', models.DateField()),
                ('test_completed', models.BooleanField()),
                ('signoff', models.BooleanField()),
                ('livedate', models.DateField()),
                ('live', models.BooleanField()),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='constants.module')),
                ('priority', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='constants.priority')),
            ],
        ),
        migrations.CreateModel(
            name='uploadedDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('document', models.FileField(upload_to='projects/')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.project')),
            ],
        ),
    ]
