# Generated by Django 3.2.12 on 2022-02-26 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0002_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
