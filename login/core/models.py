from django.db import models

class Empleado(models.Model):
    username = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    contrasena = models.CharField(max_length=255)
    cargo = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    certificados = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'empleados'

class Servicio(models.Model):
    servicios_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255)
    tipo_servicio = models.CharField(max_length=255)
    fecha = models.DateField()
    hora = models.TimeField()
    producto = models.CharField(max_length=255)
    cantidad_producto = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'servicios'

class Cita(models.Model):
    cliente_nombre = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    fecha = models.DateField()
    hora = models.TimeField()
    tipo_servicio = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'citas'
