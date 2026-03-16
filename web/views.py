from django.shortcuts import render
from .models import (
    ContactoInfo,
    HistoriaPagina,
    HeroHome,
    HomeContenido,
    HomeColeccion,
)
from catalogo.models import Producto


def home(request):
    hero = HeroHome.objects.filter(activo=True).order_by("-created_at").first()
    contacto = ContactoInfo.objects.order_by("-created_at").first()
    home_contenido = HomeContenido.objects.filter(activa=True).order_by("-created_at").first()
    colecciones_home = HomeColeccion.objects.filter(activa=True).order_by("orden", "id")
    productos_destacados = Producto.objects.filter(activo=True, destacado=True).order_by("nombre")[:4]

    return render(request, "public/home.html", {
        "hero": hero,
        "contacto": contacto,
        "home_contenido": home_contenido,
        "colecciones_home": colecciones_home,
        "productos_destacados": productos_destacados,
    })


def historia(request):
    pagina = HistoriaPagina.objects.filter(activa=True).order_by("-created_at").first()
    return render(request, "public/historia.html", {
        "pagina": pagina,
    })


def contacto(request):
    contacto_info = ContactoInfo.objects.order_by("-created_at").first()
    return render(request, "public/contacto.html", {"contacto": contacto_info})


def ubicacion(request):
    contacto_info = ContactoInfo.objects.order_by("-created_at").first()
    return render(request, "public/ubicacion.html", {"contacto": contacto_info})


def instagram(request):
    contacto_info = ContactoInfo.objects.order_by("-created_at").first()
    return render(request, "public/instagram.html", {"contacto": contacto_info})