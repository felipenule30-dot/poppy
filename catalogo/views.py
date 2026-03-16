from django.shortcuts import render, get_object_or_404
from .models import Coleccion, Producto


def colecciones_lista(request):
    colecciones = Coleccion.objects.filter(activa=True).order_by("orden", "nombre")
    return render(request, "catalogo/colecciones_lista.html", {
        "colecciones": colecciones,
    })


def coleccion_detalle(request, slug):
    coleccion = get_object_or_404(Coleccion, slug=slug, activa=True)
    productos = coleccion.productos.filter(activo=True).order_by("-destacado", "nombre")

    return render(request, "catalogo/coleccion_detalle.html", {
        "coleccion": coleccion,
        "productos": productos,
    })


def producto_detalle(request, slug):
    producto = get_object_or_404(Producto, slug=slug, activo=True)

    return render(request, "catalogo/producto_detalle.html", {
        "producto": producto,
    })