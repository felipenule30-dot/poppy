from django.db import models
from django.core.exceptions import ValidationError


class InventarioItem(models.Model):
    producto = models.OneToOneField(
        "catalogo.Producto",
        on_delete=models.CASCADE,
        related_name="inventario"
    )
    sku_interno = models.CharField(max_length=100, blank=True)
    stock_actual = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=0)
    costo_unitario = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    ubicacion = models.CharField(max_length=150, blank=True)
    activo = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.producto.nombre} - stock {self.stock_actual}"


class MovimientoInventario(models.Model):
    TIPOS = [
        ("entrada", "Entrada"),
        ("salida", "Salida"),
        ("ajuste", "Ajuste"),
    ]

    item = models.ForeignKey(
        InventarioItem,
        on_delete=models.CASCADE,
        related_name="movimientos"
    )
    tipo = models.CharField(max_length=20, choices=TIPOS)
    cantidad = models.IntegerField()
    nota = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.cantidad == 0:
            raise ValidationError("La cantidad no puede ser 0.")

        if self.tipo in ["entrada", "salida"] and self.cantidad < 0:
            raise ValidationError("Para entrada o salida, la cantidad debe ser positiva.")

        if self.tipo == "salida" and self.pk is None:
            if self.item.stock_actual < self.cantidad:
                raise ValidationError("No hay suficiente stock para registrar esta salida.")

    def save(self, *args, **kwargs):
        es_nuevo = self.pk is None

        self.full_clean()

        if es_nuevo:
            if self.tipo == "entrada":
                self.item.stock_actual += self.cantidad

            elif self.tipo == "salida":
                self.item.stock_actual -= self.cantidad

            elif self.tipo == "ajuste":
                self.item.stock_actual += self.cantidad

            self.item.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item.producto.nombre} - {self.tipo} - {self.cantidad}"