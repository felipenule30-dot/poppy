from decimal import Decimal
from django.shortcuts import get_object_or_404, redirect, render
from catalogo.models import Producto
from .models import Pedido, PedidoItem


def _get_cart(session):
    return session.get("cart", {})


def _save_cart(session, cart):
    session["cart"] = cart
    session.modified = True


def cart_item_count(request):
    cart = _get_cart(request.session)
    total_items = sum(item["cantidad"] for item in cart.values())
    return {"cart_item_count": total_items}


def add_to_cart(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, activo=True)

    cart = _get_cart(request.session)
    key = str(producto.id)

    if key in cart:
        cart[key]["cantidad"] += 1
    else:
        cart[key] = {
            "producto_id": producto.id,
            "nombre": producto.nombre,
            "precio": str(producto.precio or 0),
            "slug": producto.slug,
            "cantidad": 1,
        }

    _save_cart(request.session, cart)
    return redirect("carrito")


def remove_from_cart(request, producto_id):
    cart = _get_cart(request.session)
    key = str(producto_id)

    if key in cart:
        del cart[key]

    _save_cart(request.session, cart)
    return redirect("carrito")


def decrease_cart_item(request, producto_id):
    cart = _get_cart(request.session)
    key = str(producto_id)

    if key in cart:
        cart[key]["cantidad"] -= 1
        if cart[key]["cantidad"] <= 0:
            del cart[key]

    _save_cart(request.session, cart)
    return redirect("carrito")


def clear_cart(request):
    _save_cart(request.session, {})
    return redirect("carrito")


def carrito(request):
    cart = _get_cart(request.session)
    items = []
    total = Decimal("0.00")

    for key, item in cart.items():
        precio = Decimal(item["precio"])
        cantidad = int(item["cantidad"])
        subtotal = precio * cantidad
        total += subtotal

        items.append({
            "producto_id": item["producto_id"],
            "nombre": item["nombre"],
            "slug": item["slug"],
            "precio": precio,
            "cantidad": cantidad,
            "subtotal": subtotal,
        })

    return render(request, "pedidos/carrito.html", {
        "items": items,
        "total": total,
    })


def checkout(request):
    cart = _get_cart(request.session)
    items = []
    total = Decimal("0.00")

    for key, item in cart.items():
        precio = Decimal(item["precio"])
        cantidad = int(item["cantidad"])
        subtotal = precio * cantidad
        total += subtotal

        items.append({
            "producto_id": item["producto_id"],
            "nombre": item["nombre"],
            "slug": item["slug"],
            "precio": precio,
            "cantidad": cantidad,
            "subtotal": subtotal,
        })

    if not items:
        return redirect("carrito")

    if request.method == "POST":
        nombre_cliente = request.POST.get("nombre_cliente", "").strip()
        email = request.POST.get("email", "").strip()
        telefono = request.POST.get("telefono", "").strip()
        direccion = request.POST.get("direccion", "").strip()
        ciudad = request.POST.get("ciudad", "").strip()
        notas = request.POST.get("notas", "").strip()

        pedido = Pedido.objects.create(
            nombre_cliente=nombre_cliente,
            email=email,
            telefono=telefono,
            direccion=direccion,
            ciudad=ciudad,
            notas=notas,
            subtotal=total,
            total=total,
            estado="pendiente",
        )

        for item in items:
            PedidoItem.objects.create(
                pedido=pedido,
                producto_id=item["producto_id"],
                nombre_producto=item["nombre"],
                precio_unitario=item["precio"],
                cantidad=item["cantidad"],
                subtotal=item["subtotal"],
            )

        _save_cart(request.session, {})
        return redirect("checkout_exito", pedido_id=pedido.id)

    return render(request, "pedidos/checkout.html", {
        "items": items,
        "total": total,
    })


def checkout_exito(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, "pedidos/checkout_exito.html", {
        "pedido": pedido,
    })