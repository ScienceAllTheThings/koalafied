# Generated by Django 2.2.8 on 2019-12-13 02:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_turbine'),
    ]

    operations = [
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('value', models.FloatField()),
                ('turbine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Turbine')),
            ],
        ),
    ]