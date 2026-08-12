from django.urls import path
from . import views

urlpatterns = [
    path("colecciones/", views.colecciones_lista, name="colecciones_lista"),
    path("colecciones/<slug:slug>/", views.coleccion_detalle, name="coleccion_detalle"),
    path("producto/<slug:slug>/", views.producto_detalle, name="producto_detalle"),
]