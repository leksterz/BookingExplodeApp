# Generated by Django 4.1.7 on 2023-06-17 12:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_engineer_contact_info_engineer_studio'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
