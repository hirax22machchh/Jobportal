# Generated by Django 5.0.2 on 2024-02-26 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0006_remove_jobseeker_resume_addr_jobseeker_resume'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employer',
            name='emp_email',
            field=models.EmailField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='employer',
            name='help_line_no',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='employer',
            name='username',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='jobseeker',
            name='js_email',
            field=models.EmailField(max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='jobseeker',
            name='mobileno',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='jobseeker',
            name='username',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
