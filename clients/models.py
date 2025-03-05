from django.db import models

# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=128, verbose_name=(u'Nombre'))
    last_name = models.CharField(max_length=128, verbose_name=(u'Apellido'))
    national_id = models.CharField(max_length=15, verbose_name=(u'Cédula'))
    active = models.BooleanField(default=True, verbose_name=('Habilitado'))

    def __str__(self):
        return f"{self.name} - ${self.last_name}"