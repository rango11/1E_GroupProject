# Generated by Django 2.2.28 on 2023-03-21 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WhiteMarket', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bids',
            options={'verbose_name_plural': 'Bids'},
        ),
        migrations.AlterModelOptions(
            name='items',
            options={'verbose_name_plural': 'Items'},
        ),
        migrations.AlterModelOptions(
            name='sellers',
            options={'verbose_name_plural': 'Sellers'},
        ),
        migrations.AlterModelOptions(
            name='stores',
            options={'verbose_name_plural': 'Stores'},
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name_plural': 'UserProfiles'},
        ),
    ]
