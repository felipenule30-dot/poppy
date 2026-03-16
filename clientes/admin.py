from django.contrib import admin
from .models import Cliente, DireccionCliente


class DireccionClienteInline(admin.TabularInline):
    model = DireccionCliente
    extra = 0


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "telefono", "whatsapp", "email", "ciudad", "recurrente", "activo")
    list_editable = ("recurrente", "activo")
    search_fields = ("nombre", "telefono", "whatsapp", "email", "documento", "instagram")
    list_filter = ("recurrente", "activo", "ciudad")
    inlines = [DireccionClienteInline]


@admin.register(DireccionCliente)
class DireccionClienteAdmin(admin.ModelAdmin):
    list_display = ("cliente", "nombre", "ciudad", "principal")
    list_filter = ("principal", "ciudad")
    search_fields = ("cliente__nombre", "direccion", "barrio", "ciudad")