# Generated by Django 5.1.6 on 2025-03-05 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permits', '0003_alter_permit_permit_mode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permit',
            name='capacity',
            field=models.IntegerField(blank=True, null=True, verbose_name='Capacidad'),
        ),
        migrations.AlterField(
            model_name='permit',
            name='company_name',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Razón Social'),
        ),
        migrations.AlterField(
            model_name='permit',
            name='creation_date',
            field=models.DateField(verbose_name='Fecha Creación'),
        ),
        migrations.AlterField(
            model_name='permit',
            name='has_fire_extinguisher',
            field=models.BooleanField(blank=True, null=True, verbose_name='Extintor'),
        ),
        migrations.AlterField(
            model_name='permit',
            name='permit_file',
            field=models.FileField(blank=True, upload_to='pdfs/', verbose_name='Permiso'),
        ),
    ]
