# Generated by Django 5.0.1 on 2024-03-12 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='profile.jpg', upload_to='user_profile'),
        ),
    ]
