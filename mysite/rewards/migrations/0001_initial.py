# Generated by Django 5.1.6 on 2025-03-06 14:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appname', models.CharField(max_length=255)),
                ('link', models.URLField()),
                ('logo', models.ImageField(upload_to='app_logos/')),
                ('category', models.CharField(max_length=255)),
                ('subcategory', models.CharField(max_length=255)),
                ('points', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Screenshot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('srnshot', models.ImageField(upload_to='screenshots/')),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rewards.app')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.useraccount')),
            ],
        ),
    ]
