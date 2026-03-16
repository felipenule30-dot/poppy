from django.contrib import admin
from .models import Pedido, PedidoItem


class PedidoItemInline(admin.TabularInline):
    model = PedidoItem
    extra = 0


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre_cliente", "estado", "total", "created_at")
    list_filter = ("estado", "created_at")
    search_fields = ("nombre_cliente", "email", "telefono")
    inlines = [PedidoItemInline]


@admin.register(PedidoItem)
class PedidoItemAdmin(admin.ModelAdmin):
    list_display = ("pedido", "nombre_producto", "cantidad", "precio_unitario", "subtotal")
    search_fields = ("nombre_producto",)