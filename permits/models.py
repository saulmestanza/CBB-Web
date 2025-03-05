from django.db import models
from django.utils import timezone
from clients.models import Client
from permit_types.models import PermitType
from django.contrib.auth.models import User

# Create your models here.
class Permit(models.Model):
    PERMIT_MODE_CHOICES = {
        "TR": "Transporte",
        "OC": "Ocasional",
        "CN": "Construcción",
        "FN": "Funcionamiento",
    }
    permit_mode = models.CharField(
        max_length=2,
        choices=PERMIT_MODE_CHOICES,
        default="TR",
    )
    description = models.CharField(max_length=128, verbose_name=(u'Descripción'))
    address = models.CharField(max_length=512, verbose_name=(u'Direción'))
    deposit_number = models.BigIntegerField(verbose_name=(u'Número Depósito'))
    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name=(u'Cliente'))
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=(u'Usuario'))
    permit_type = models.ForeignKey(PermitType, on_delete=models.PROTECT, verbose_name=(u'Tipo de Permiso'))
    deleted = models.BooleanField(default=False, verbose_name=('Activo'))
    issue_date = models.DateField(verbose_name=(u'Fecha Emisión'))
    expiration_date = models.DateField(verbose_name=(u'Fecha Expiración'))
    creation_date = models.DateField(verbose_name=(u'Fecha Emisión'))
    permit_code = models.IntegerField(verbose_name=(u'Código Permiso'))
    permit_file = models.FileField(upload_to='pdfs/', verbose_name=(u'Permiso'))

    vehicle_brand = models.CharField(blank=True, max_length=128, verbose_name=(u'Marca Vehículo'))
    license_plate = models.CharField(blank=True, max_length=128, verbose_name=(u'Placa Vehículo'))
    has_fire_extinguisher = models.BooleanField(blank=True, verbose_name=('Extintor'))
    capacity = models.IntegerField(blank=True, verbose_name=(u'Capacidad'))
    company_name = models.CharField(blank=True, max_length=512, verbose_name=(u'Razón Social'))