from django.contrib import admin
from .models import Artesano


@admin.register(Artesano)
class ArtesanoAdmin(admin.ModelAdmin):

    list_display = ("nombre", "region", "tecnica", "destacado", "activo")

    prepopulated_fields = {"slug": ("nombre",)}

    list_editable = ("destacado", "activo")