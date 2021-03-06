# Generated by Django 3.2.12 on 2022-02-26 20:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import sqlalchemy.sql.expression


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('communities', '0004_auto_20220226_2000'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='goal',
            name='members',
            field=models.ManyToManyField(blank=sqlalchemy.sql.expression.true, related_name='members', to=settings.AUTH_USER_MODEL),
        ),
    ]
