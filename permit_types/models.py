from django.db import models
from django.utils import timezone

# Create your models here.
class PermitTypes(models.Model):
    name = models.CharField(max_length=128, verbose_name=(u'Nombre'))
    price = models.DecimalField(max_digits=10, default=0.0, decimal_places=2, verbose_name=(u'Precio'))
    active = models.BooleanField(default=True, verbose_name=('Habilitado'))
    creation_date = models.DateField(default=timezone.now, verbose_name=(u'Fecha Creación'))

    def __str__(self):
        return f"{self.name} - ${self.price}"