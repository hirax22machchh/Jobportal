# Generated by Django 5.0.2 on 2024-03-30 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0027_alter_jobposting_req_experience'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='message',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
