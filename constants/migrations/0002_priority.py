# Generated by Django 3.2.5 on 2021-07-31 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constants', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Priority',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.PositiveSmallIntegerField()),
                ('priority', models.CharField(max_length=255)),
            ],
        ),
    ]
