from django.contrib import admin
from .models import Coleccion, Producto, ProductoImagen


class ProductoImagenInline(admin.TabularInline):
    model = ProductoImagen
    extra = 1


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "coleccion", "artesano", "destacado", "activo")
    prepopulated_fields = {"slug": ("nombre",)}
    inlines = [ProductoImagenInline]


@admin.register(Coleccion)
class ColeccionAdmin(admin.ModelAdmin):
    list_display = ("nombre", "orden", "activa")
    prepopulated_fields = {"slug": ("nombre",)}


admin.site.register(ProductoImagen)