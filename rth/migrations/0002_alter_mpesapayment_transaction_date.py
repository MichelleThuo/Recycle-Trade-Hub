# Generated by Django 5.0.1 on 2024-03-11 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mpesapayment',
            name='transaction_date',
            field=models.CharField(max_length=100),
        ),
    ]