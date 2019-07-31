# Generated by Django 2.1.7 on 2019-07-31 06:25

from django.db import migrations, models
import django.db.models.deletion
import main.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('car_id', models.AutoField(primary_key=True, serialize=False)),
                ('url', models.TextField()),
                ('title', models.TextField()),
                ('price', models.IntegerField()),
                ('location', models.CharField(max_length=100)),
                ('model', models.TextField()),
                ('mileage', models.IntegerField()),
                ('fuel', models.CharField(max_length=20)),
                ('engine', models.CharField(max_length=20)),
                ('transmission', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('image_id', models.AutoField(primary_key=True, serialize=False)),
                ('url', models.TextField()),
                ('car_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Car')),
            ],
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('keyword_id', models.AutoField(primary_key=True, serialize=False)),
                ('unique_id', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('keyword', models.TextField()),
                ('expiryTime', models.DateTimeField(default=main.models.setExpiryTime)),
            ],
        ),
        migrations.CreateModel(
            name='KeywordCar',
            fields=[
                ('keywordCar_id', models.AutoField(primary_key=True, serialize=False)),
                ('car_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Car')),
                ('keyword_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Keyword')),
            ],
        ),
    ]
