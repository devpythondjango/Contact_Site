# Generated by Django 4.2.7 on 2023-12-09 16:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_profile_bg_avatar'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'Profile', 'verbose_name_plural': 'Profiles'},
        ),
    ]