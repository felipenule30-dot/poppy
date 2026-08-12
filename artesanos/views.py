from django.shortcuts import render, get_object_or_404
from .models import Artesano


def artesanos_lista(request):
    artesanos = Artesano.objects.filter(activo=True).order_by("-destacado", "nombre")
    return render(request, "artesanos/lista.html", {
        "artesanos": artesanos,
    })


def artesano_detalle(request, slug):
    artesano = get_object_or_404(Artesano, slug=slug, activo=True)
    return render(request, "artesanos/detalle.html", {
        "artesano": artesano,
    })