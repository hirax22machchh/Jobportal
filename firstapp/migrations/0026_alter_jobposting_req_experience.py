# Generated by Django 5.0.2 on 2024-03-13 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0025_alter_jobposting_req_experience'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobposting',
            name='req_experience',
            field=models.CharField(default='Fresher', max_length=40),
        ),
    ]
