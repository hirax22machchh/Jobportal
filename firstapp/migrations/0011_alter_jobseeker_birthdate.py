# Generated by Django 5.0.2 on 2024-03-10 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0010_alter_login_logouttime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobseeker',
            name='birthdate',
            field=models.DateField(null=True),
        ),
    ]