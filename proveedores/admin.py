from django.contrib import admin
from .models import Proveedor


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "contacto", "telefono", "email", "ciudad", "pais", "tiempo_entrega_dias", "activo")
    list_editable = ("activo",)
    search_fields = ("nombre", "contacto", "telefono", "whatsapp", "email", "ciudad", "pais")
    list_filter = ("activo", "ciudad", "pais")