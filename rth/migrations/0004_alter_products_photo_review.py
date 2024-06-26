# Generated by Django 5.0.1 on 2024-03-24 19:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rth', '0003_alter_products_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='photo',
            field=models.ImageField(upload_to='product/2024-03-24'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('body', models.TextField()),
                ('stars', models.IntegerField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rth.products')),
            ],
        ),
    ]
