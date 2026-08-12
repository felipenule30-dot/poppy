from django.db import models


class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    telefono = models.CharField(max_length=50, blank=True)
    whatsapp = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    documento = models.CharField(max_length=100, blank=True)
    ciudad = models.CharField(max_length=150, blank=True)
    instagram = models.CharField(max_length=150, blank=True)
    notas = models.TextField(blank=True)
    recurrente = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class DireccionCliente(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="direcciones"
    )
    nombre = models.CharField(max_length=150, default="Principal")
    direccion = models.CharField(max_length=255)
    barrio = models.CharField(max_length=150, blank=True)
    ciudad = models.CharField(max_length=150, blank=True)
    referencia = models.CharField(max_length=255, blank=True)
    principal = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.cliente.nombre} - {self.nombre}"