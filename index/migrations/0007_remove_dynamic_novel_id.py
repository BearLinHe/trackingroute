# Generated by Django 4.2.3 on 2023-07-29 05:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0006_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dynamic',
            name='novel_id',
        ),
    ]
