# Generated by Django 5.0.4 on 2024-04-24 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('redirect_links', '0006_alter_sesions_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companies',
            name='link',
            field=models.URLField(max_length=500),
        ),
    ]
