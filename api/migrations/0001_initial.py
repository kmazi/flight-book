# Generated by Django 2.2.3 on 2021-12-12 09:20

import datetime
from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('origin', models.CharField(max_length=100)),
                ('destination', models.CharField(max_length=100)),
                ('departure_date', models.DateField(default=datetime.date(2021, 12, 13))),
                ('plane_type', models.CharField(choices=[('economic', 'econimic class'), ('business', 'business class'), ('first_class', 'first class')], default='economic', max_length=100)),
                ('capacity', models.IntegerField(default=100)),
            ],
            managers=[
                ('records', django.db.models.manager.Manager()),
            ],
        ),
    ]
