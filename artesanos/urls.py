from django.urls import path
from . import views

urlpatterns = [
    path("artesanos/", views.artesanos_lista, name="artesanos_lista"),
    path("artesanos/<slug:slug>/", views.artesano_detalle, name="artesano_detalle"),
]