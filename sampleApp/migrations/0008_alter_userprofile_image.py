# Generated by Django 4.1 on 2023-12-21 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sampleApp', '0007_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='profile_images'),
        ),
    ]