from django.urls import path
from . import views

urlpatterns = [
    path("carrito/", views.carrito, name="carrito"),
    path("carrito/agregar/<int:producto_id>/", views.add_to_cart, name="add_to_cart"),
    path("carrito/quitar/<int:producto_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("carrito/restar/<int:producto_id>/", views.decrease_cart_item, name="decrease_cart_item"),
    path("carrito/vaciar/", views.clear_cart, name="clear_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("checkout/exito/<int:pedido_id>/", views.checkout_exito, name="checkout_exito"),
]