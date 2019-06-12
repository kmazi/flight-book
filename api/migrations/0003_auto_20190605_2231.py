# Generated by Django 2.2.2 on 2019-06-05 22:31

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_flight_departure_date'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='flight',
            managers=[
                ('records', django.db.models.manager.Manager()),
            ],
        ),
        migrations.RemoveField(
            model_name='flight',
            name='departure_time',
        ),
        migrations.RemoveField(
            model_name='flight',
            name='number',
        ),
        migrations.AddField(
            model_name='flight',
            name='plane_type',
            field=models.CharField(choices=[('economic', 'econimic class'), ('business', 'business class'), ('first_class', 'first class')], default='economic', max_length=100),
        ),
        migrations.AddField(
            model_name='flight',
            name='return_date',
            field=models.DateField(null=True),
        ),
    ]