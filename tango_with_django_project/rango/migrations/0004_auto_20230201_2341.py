# Generated by Django 2.2.28 on 2023-02-01 23:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0003_choice_question'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]
