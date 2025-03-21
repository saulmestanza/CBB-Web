# Generated by Django 5.1.6 on 2025-03-05 10:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0002_rename_clients_client'),
        ('permit_types', '0003_rename_permittypes_permittype'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Permit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permit_mode', models.CharField(choices=[('TR', 'Transporte'), ('OC', 'Ocasional'), ('CN', 'Construcción'), ('FN', 'Funcionamiento')], default='TR', max_length=2)),
                ('description', models.CharField(max_length=128, verbose_name='Descripción')),
                ('address', models.CharField(max_length=512, verbose_name='Direción')),
                ('deposit_number', models.BigIntegerField(max_length=128, verbose_name='Número Depósito')),
                ('deleted', models.BooleanField(default=False, verbose_name='Activo')),
                ('issue_date', models.DateField(verbose_name='Fecha Emisión')),
                ('expiration_date', models.DateField(verbose_name='Fecha Expiración')),
                ('creation_date', models.DateField(verbose_name='Fecha Emisión')),
                ('permit_code', models.IntegerField(verbose_name='Código Permiso')),
                ('permit_file', models.FileField(upload_to='pdfs/', verbose_name='Permiso')),
                ('vehicle_brand', models.CharField(blank=True, max_length=128, verbose_name='Marca Vehículo')),
                ('license_plate', models.CharField(blank=True, max_length=128, verbose_name='Placa Vehículo')),
                ('has_fire_extinguisher', models.BooleanField(blank=True, verbose_name='Extintor')),
                ('capacity', models.IntegerField(blank=True, max_length=100, verbose_name='Capacidad')),
                ('company_name', models.CharField(blank=True, max_length=512, verbose_name='Razón Social')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clients.client', verbose_name='Cliente')),
                ('permit_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='permit_types.permittype', verbose_name='Tipo de Permiso')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
        ),
    ]
