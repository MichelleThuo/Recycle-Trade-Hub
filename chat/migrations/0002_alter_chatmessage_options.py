# Generated by Django 5.0.1 on 2024-01-10 09:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chatmessage',
            options={'ordering': ['date'], 'verbose_name_plural': 'Message'},
        ),
    ]