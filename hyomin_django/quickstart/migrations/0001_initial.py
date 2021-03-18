# Generated by Django 3.1.7 on 2021-03-18 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KrWeather',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('w_area', models.CharField(max_length=100)),
                ('w_curr', models.CharField(max_length=100)),
                ('w_cute', models.CharField(max_length=100)),
                ('w_pcute', models.CharField(max_length=100)),
                ('w_rain', models.CharField(max_length=100)),
                ('w_snow', models.CharField(max_length=100)),
                ('w_humi', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'kr_weather',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MyKrWeather',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('w_area', models.TextField()),
                ('w_curr', models.TextField()),
                ('w_cute', models.TextField()),
                ('w_pcute', models.TextField()),
                ('w_rain', models.TextField()),
                ('w_snow', models.TextField()),
                ('w_humi', models.TextField()),
            ],
            options={
                'db_table': 'my_kr_weather',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MyPit',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('iname', models.TextField()),
                ('iprice', models.TextField()),
                ('ireview', models.TextField()),
            ],
            options={
                'db_table': 'my_pit',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Pit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iname', models.CharField(max_length=100)),
                ('iprice', models.CharField(max_length=100)),
                ('ireview', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'pit',
                'managed': False,
            },
        ),
    ]
