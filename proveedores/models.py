from django.db import models


class Proveedor(models.Model):
    nombre = models.CharField(max_length=200)
    contacto = models.CharField(max_length=150, blank=True)
    telefono = models.CharField(max_length=50, blank=True)
    whatsapp = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    ciudad = models.CharField(max_length=150, blank=True)
    pais = models.CharField(max_length=150, blank=True)
    tiempo_entrega_dias = models.PositiveIntegerField(default=0)
    notas = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre