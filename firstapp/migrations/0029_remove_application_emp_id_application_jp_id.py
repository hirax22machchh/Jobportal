# Generated by Django 5.0.2 on 2024-03-30 09:13

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0028_alter_application_message'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='application',
            name='emp_id',
        ),
    migrations.AddField(
    model_name='application',
    name='jp_id',
    field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='firstapp.jobposting'),  # Change the default value to a valid primary key
    preserve_default=False,
),

    ]
