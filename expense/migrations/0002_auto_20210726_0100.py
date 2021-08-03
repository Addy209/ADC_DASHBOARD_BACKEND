# Generated by Django 3.2.5 on 2021-07-25 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenditure',
            name='fin_cost',
            field=models.PositiveBigIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='expenditure',
            name='nonfin_cost',
            field=models.PositiveBigIntegerField(default=0),
            preserve_default=False,
        ),
    ]
