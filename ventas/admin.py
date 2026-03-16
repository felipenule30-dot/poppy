from django.contrib import admin
from .models import Venta, VentaItem


class VentaItemInline(admin.TabularInline):
    model = VentaItem
    extra = 1


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "canal", "total", "created_at")
    list_filter = ("canal", "created_at")
    search_fields = ("cliente__nombre", "notas")
    inlines = [VentaItemInline]


@admin.register(VentaItem)
class VentaItemAdmin(admin.ModelAdmin):
    list_display = ("venta", "producto", "cantidad", "precio_unitario", "subtotal")
    search_fields = ("producto__nombre",)