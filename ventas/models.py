from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError


class Venta(models.Model):
    CANALES = [
        ("tienda", "Tienda"),
        ("instagram", "Instagram"),
        ("whatsapp", "WhatsApp"),
        ("manual", "Manual"),
    ]

    cliente = models.ForeignKey(
        "clientes.Cliente",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ventas"
    )
    canal = models.CharField(max_length=30, choices=CANALES, default="tienda")
    notas = models.TextField(blank=True)

    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    descuento_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    descuento_valor = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def recalcular_total(self):
        subtotal = sum((item.subtotal for item in self.items.all()), Decimal("0.00"))
        self.subtotal = subtotal

        descuento_pct = self.descuento_porcentaje or Decimal("0.00")
        self.descuento_valor = (subtotal * descuento_pct) / Decimal("100")

        self.total = subtotal - self.descuento_valor
        if self.total < 0:
            self.total = Decimal("0.00")

        self.save(update_fields=["subtotal", "descuento_valor", "total"])

    def revertir_inventario(self):
        for item in self.items.select_related("producto__inventario").all():
            if hasattr(item.producto, "inventario"):
                inventario = item.producto.inventario
                inventario.stock_actual += item.cantidad
                inventario.save(update_fields=["stock_actual"])

    def __str__(self):
        return f"Venta #{self.id} - {self.canal} - {self.total}"


class VentaItem(models.Model):
    venta = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        related_name="items"
    )
    producto = models.ForeignKey(
        "catalogo.Producto",
        on_delete=models.PROTECT,
        related_name="venta_items"
    )
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def clean(self):
        if self.cantidad <= 0:
            raise ValidationError("La cantidad debe ser mayor que cero.")

        if not hasattr(self.producto, "inventario"):
            raise ValidationError("Este producto no tiene inventario asociado.")

        inventario = self.producto.inventario

        if self.pk is None:
            if inventario.stock_actual < self.cantidad:
                raise ValidationError(
                    f"No hay suficiente stock para esta venta. Disponible: {inventario.stock_actual}"
                )

    def save(self, *args, **kwargs):
        es_nuevo = self.pk is None

        if not self.precio_unitario:
            self.precio_unitario = self.producto.precio or Decimal("0.00")

        self.subtotal = Decimal(self.cantidad) * self.precio_unitario
        self.full_clean()

        if es_nuevo:
            inventario = self.producto.inventario
            inventario.stock_actual -= self.cantidad
            inventario.save(update_fields=["stock_actual"])

        super().save(*args, **kwargs)

        self.venta.recalcular_total()

        if self.venta.cliente and self.venta.cliente.ventas.count() >= 1:
            if not self.venta.cliente.recurrente:
                self.venta.cliente.recurrente = True
                self.venta.cliente.save(update_fields=["recurrente"])

    def delete(self, *args, **kwargs):
        if hasattr(self.producto, "inventario"):
            inventario = self.producto.inventario
            inventario.stock_actual += self.cantidad
            inventario.save(update_fields=["stock_actual"])

        venta = self.venta
        super().delete(*args, **kwargs)
        venta.recalcular_total()

    def __str__(self):
        return f"{self.producto.nombre} x {self.cantidad}"