from django.db import models
from django.utils import timezone
from clients.models import Client
from permit_types.models import PermitType
from django.contrib.auth.models import User
from datetime import date

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
        verbose_name=(u'Modo Permiso')
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
    creation_date = models.DateField(verbose_name=(u'Fecha Creación'))
    permit_code = models.IntegerField(verbose_name=(u'Código Permiso'))

    permit_file = models.FileField(blank=True, upload_to='pdfs/', verbose_name=(u'Permiso'))
    vehicle_brand = models.CharField(blank=True, max_length=128, verbose_name=(u'Marca Vehículo'))
    license_plate = models.CharField(blank=True, max_length=128, verbose_name=(u'Placa Vehículo'))
    has_fire_extinguisher = models.BooleanField(blank=True, null=True, verbose_name=('Extintor'))
    capacity = models.IntegerField(blank=True, null=True, verbose_name=(u'Capacidad'))
    company_name = models.CharField(blank=True, null=True, max_length=512, verbose_name=(u'Razón Social'))


    def save(self, *args, **kwargs):
        self.expiration_date = date(date.today().year, 12, 31)
        self.issue_date = date.today()
        if self.user:
            self.user = self.user 

        latest_permit = Permit.objects.filter(permit_mode=self.permit_mode).order_by('-permit_code').first()
        self.permit_code = (latest_permit.permit_code + 1) if latest_permit else 1

        super().save(*args, **kwargs)