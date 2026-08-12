from django.contrib import admin
from .models import InventarioItem, MovimientoInventario


class MovimientoInventarioInline(admin.TabularInline):
    model = MovimientoInventario
    extra = 0


@admin.register(InventarioItem)
class InventarioItemAdmin(admin.ModelAdmin):
    list_display = ("producto", "sku_interno", "stock_actual", "stock_minimo", "ubicacion", "activo")
    list_editable = ("stock_actual", "stock_minimo", "ubicacion", "activo")
    search_fields = ("producto__nombre", "sku_interno")
    inlines = [MovimientoInventarioInline]


@admin.register(MovimientoInventario)
class MovimientoInventarioAdmin(admin.ModelAdmin):
    list_display = ("item", "tipo", "cantidad", "created_at")
    list_filter = ("tipo", "created_at")
    search_fields = ("item__producto__nombre", "nota")