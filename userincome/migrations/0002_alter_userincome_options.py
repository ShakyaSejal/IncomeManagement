# Generated by Django 5.0.1 on 2024-02-05 11:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userincome', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userincome',
            options={'ordering': ['-date']},
        ),
    ]