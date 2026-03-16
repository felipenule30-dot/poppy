from django.contrib import admin
from .models import (
    ContactoInfo,
    HistoriaPagina,
    HeroHome,
    HomeContenido,
    HomeColeccion,
)


@admin.register(ContactoInfo)
class ContactoInfoAdmin(admin.ModelAdmin):
    list_display = ("telefono", "whatsapp", "email")


@admin.register(HistoriaPagina)
class HistoriaPaginaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "activa", "created_at")


@admin.register(HeroHome)
class HeroHomeAdmin(admin.ModelAdmin):
    list_display = ("titulo", "activo", "created_at")


@admin.register(HomeContenido)
class HomeContenidoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activa", "created_at")


@admin.register(HomeColeccion)
class HomeColeccionAdmin(admin.ModelAdmin):
    list_display = ("nombre", "coleccion_catalogo", "orden", "activa", "created_at")
    list_editable = ("orden", "activa")