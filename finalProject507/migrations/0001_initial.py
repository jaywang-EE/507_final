# Generated by Django 3.0.3 on 2020-04-28 05:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='County',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fip', models.IntegerField()),
                ('countyName', models.CharField(max_length=100)),
                ('stateName', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stateName', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=1000)),
                ('url', models.CharField(max_length=1000)),
                ('date', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CountyCase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cases', models.IntegerField()),
                ('deaths', models.IntegerField()),
                ('date', models.DateField()),
                ('county', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finalProject507.County')),
            ],
        ),
    ]