# Generated by Django 5.0.2 on 2024-03-09 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0007_alter_employer_emp_email_alter_employer_help_line_no_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Login',
            fields=[
                ('login_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=20, unique=True)),
                ('password', models.CharField(max_length=20)),
                ('logindate', models.DateTimeField(auto_now_add=True)),
                ('logoutdate', models.DateTimeField()),
            ],
        ),
    ]
