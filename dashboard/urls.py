from django.urls import path
from . import views

urlpatterns = [
    path("panel/dashboard/", views.panel_dashboard, name="panel_dashboard"),

    path("panel/inventario/", views.panel_inventario, name="panel_inventario"),
    path("panel/inventario/nuevo/", views.panel_inventario_nuevo, name="panel_inventario_nuevo"),
    path("panel/inventario/<int:item_id>/editar/", views.panel_inventario_editar, name="panel_inventario_editar"),
    path("panel/inventario/<int:item_id>/movimiento/", views.panel_inventario_movimiento, name="panel_inventario_movimiento"),

    path("panel/clientes/", views.panel_clientes, name="panel_clientes"),
    path("panel/clientes/nuevo/", views.panel_cliente_nuevo, name="panel_cliente_nuevo"),
    path("panel/clientes/<int:cliente_id>/editar/", views.panel_cliente_editar, name="panel_cliente_editar"),

    path("panel/pedidos/", views.panel_pedidos, name="panel_pedidos"),
    path("panel/pedidos/<int:pedido_id>/", views.panel_pedido_detalle, name="panel_pedido_detalle"),
    path("panel/pedidos/<int:pedido_id>/estado/", views.panel_pedido_estado, name="panel_pedido_estado"),

    path("panel/ventas/", views.panel_ventas, name="panel_ventas"),
    path("panel/ventas/nueva/", views.panel_venta_nueva, name="panel_venta_nueva"),
    path("panel/ventas/<int:venta_id>/", views.panel_venta_detalle, name="panel_venta_detalle"),
    path("panel/ventas/<int:venta_id>/eliminar/", views.panel_venta_eliminar, name="panel_venta_eliminar"),
    

    path("panel/productos/", views.panel_productos, name="panel_productos"),
    path("panel/productos/nuevo/", views.panel_producto_nuevo, name="panel_producto_nuevo"),
    path("panel/productos/<int:producto_id>/editar/", views.panel_producto_editar, name="panel_producto_editar"),
    path("panel/proveedores/", views.panel_proveedores, name="panel_proveedores"),
    path("panel/proveedores/nuevo/", views.panel_proveedor_nuevo, name="panel_proveedor_nuevo"),
    path("panel/proveedores/<int:proveedor_id>/editar/", views.panel_proveedor_editar, name="panel_proveedor_editar"),
    path("panel/compras/", views.panel_compras, name="panel_compras"),
    path("panel/productos/<int:producto_id>/imagenes/", views.panel_producto_imagenes, name="panel_producto_imagenes"),
    path("panel/productos/<int:producto_id>/eliminar/", views.panel_producto_eliminar, name="panel_producto_eliminar"),
]
