# Generated by Django 5.0.3 on 2024-05-16 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cliente_nombre', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255)),
                ('fecha', models.DateTimeField()),
                ('hora', models.TimeField()),
                ('tipo_servicio', models.CharField(max_length=255)),
            ],
        ),
    ]
