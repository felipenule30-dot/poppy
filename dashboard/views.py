from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, F, ExpressionWrapper, DecimalField
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify

from inventario.models import InventarioItem, MovimientoInventario
from clientes.models import Cliente
from ventas.models import Venta, VentaItem
from catalogo.models import Producto, Coleccion
from pedidos.models import Pedido
from proveedores.models import Proveedor
from catalogo.models import Producto, Coleccion, ProductoImagen

@login_required
def panel_productos(request):
    q = request.GET.get("q", "").strip()
    coleccion_id = request.GET.get("coleccion", "").strip()

    productos = (
        Producto.objects
        .select_related("coleccion", "proveedor")
        .prefetch_related("imagenes")
        .order_by("nombre")
    )

    if q:
        productos = productos.filter(nombre__icontains=q)

    if coleccion_id:
        productos = productos.filter(coleccion_id=coleccion_id)

    colecciones = Coleccion.objects.filter(activa=True).order_by("nombre")

    return render(request, "dashboard/productos.html", {
        "productos": productos,
        "colecciones": colecciones,
        "q": q,
        "coleccion_id": coleccion_id,
    })


@login_required
def panel_producto_nuevo(request):
    colecciones = Coleccion.objects.filter(activa=True).order_by("nombre")
    proveedores = Proveedor.objects.filter(activo=True).order_by("nombre")

    if request.method == "POST":
        nombre = request.POST.get("nombre", "").strip()
        slug = request.POST.get("slug", "").strip()
        coleccion_id = request.POST.get("coleccion")
        proveedor_id = request.POST.get("proveedor") or None
        descripcion = request.POST.get("descripcion", "").strip()
        precio = request.POST.get("precio") or 0
        costo_adquisicion = request.POST.get("costo_adquisicion") or None
        tiempo_adquisicion_dias = request.POST.get("tiempo_adquisicion_dias") or 0
        stock_objetivo = request.POST.get("stock_objetivo") or 0
        notas_internas = request.POST.get("notas_internas", "").strip()
        material = request.POST.get("material", "").strip()
        destacado = request.POST.get("destacado") == "on"
        activo = request.POST.get("activo") == "on"

        if not slug:
            slug = slugify(nombre)

        coleccion = get_object_or_404(Coleccion, id=coleccion_id)

        producto = Producto.objects.create(
            nombre=nombre,
            slug=slug,
            coleccion=coleccion,
            proveedor_id=proveedor_id,
            descripcion=descripcion,
            precio=precio,
            costo_adquisicion=costo_adquisicion,
            tiempo_adquisicion_dias=tiempo_adquisicion_dias,
            stock_objetivo=stock_objetivo,
            notas_internas=notas_internas,
            material=material,
            destacado=destacado,
            activo=activo,
        )

        messages.success(request, f"Producto creado correctamente: {producto.nombre}")
        return redirect("panel_producto_editar", producto_id=producto.id)

    return render(request, "dashboard/producto_nuevo.html", {
        "colecciones": colecciones,
        "proveedores": proveedores,
    })


@login_required
def panel_producto_editar(request, producto_id):
    producto = get_object_or_404(
        Producto.objects.select_related("coleccion", "proveedor").prefetch_related("imagenes"),
        id=producto_id
    )
    colecciones = Coleccion.objects.filter(activa=True).order_by("nombre")
    proveedores = Proveedor.objects.filter(activo=True).order_by("nombre")

    if request.method == "POST":
        producto.nombre = request.POST.get("nombre", "").strip()
        producto.slug = request.POST.get("slug", "").strip() or slugify(producto.nombre)
        producto.coleccion_id = request.POST.get("coleccion")
        producto.proveedor_id = request.POST.get("proveedor") or None
        producto.descripcion = request.POST.get("descripcion", "").strip()
        producto.material = request.POST.get("material", "").strip()
        producto.precio = request.POST.get("precio") or 0
        producto.costo_adquisicion = request.POST.get("costo_adquisicion") or None
        producto.tiempo_adquisicion_dias = request.POST.get("tiempo_adquisicion_dias") or 0
        producto.stock_objetivo = request.POST.get("stock_objetivo") or 0
        producto.notas_internas = request.POST.get("notas_internas", "").strip()
        producto.destacado = request.POST.get("destacado") == "on"
        producto.activo = request.POST.get("activo") == "on"
        producto.save()

        messages.success(request, "Producto actualizado correctamente.")
        return redirect("panel_producto_editar", producto_id=producto.id)

    return render(request, "dashboard/producto_editar.html", {
        "producto": producto,
        "colecciones": colecciones,
        "proveedores": proveedores,
    })


@login_required
def panel_producto_imagenes(request, producto_id):
    producto = get_object_or_404(
        Producto.objects.prefetch_related("imagenes"),
        id=producto_id
    )

    if request.method == "POST":
        archivos = request.FILES.getlist("imagenes")

        for i, archivo in enumerate(archivos):
            ProductoImagen.objects.create(
                producto=producto,
                imagen=archivo,
                orden=producto.imagenes.count() + i
            )

        messages.success(request, "Imágenes subidas correctamente.")
        return redirect("panel_producto_imagenes", producto_id=producto.id)

    return render(request, "dashboard/producto_imagenes.html", {
        "producto": producto,
    })


@login_required
def panel_producto_eliminar(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    if request.method == "POST":
        nombre = producto.nombre
        producto.delete()
        messages.success(request, f"Producto eliminado correctamente: {nombre}")
        return redirect("panel_productos")

    return render(request, "dashboard/producto_eliminar.html", {
        "producto": producto,
    })
  





@login_required
def panel_dashboard(request):
    fecha_inicio = request.GET.get("fecha_inicio", "").strip()
    fecha_fin = request.GET.get("fecha_fin", "").strip()

    ventas_qs = Venta.objects.select_related("cliente").all()
    pedidos_qs = Pedido.objects.all()
    venta_items_qs = VentaItem.objects.select_related("producto", "venta").all()

    if fecha_inicio:
        ventas_qs = ventas_qs.filter(created_at__date__gte=fecha_inicio)
        pedidos_qs = pedidos_qs.filter(created_at__date__gte=fecha_inicio)
        venta_items_qs = venta_items_qs.filter(venta__created_at__date__gte=fecha_inicio)

    if fecha_fin:
        ventas_qs = ventas_qs.filter(created_at__date__lte=fecha_fin)
        pedidos_qs = pedidos_qs.filter(created_at__date__lte=fecha_fin)
        venta_items_qs = venta_items_qs.filter(venta__created_at__date__lte=fecha_fin)

    total_ventas = ventas_qs.count()
    total_pedidos = pedidos_qs.count()
    total_clientes = Cliente.objects.filter(activo=True).count()
    clientes_recurrentes = Cliente.objects.filter(activo=True, recurrente=True).count()
    total_proveedores = Proveedor.objects.filter(activo=True).count()
    total_productos = Producto.objects.filter(activo=True).count()

    total_facturado = ventas_qs.aggregate(total=Sum("total"))["total"] or Decimal("0.00")

    ticket_promedio = Decimal("0.00")
    if total_ventas > 0:
        ticket_promedio = total_facturado / Decimal(total_ventas)

    inventario_items = (
        InventarioItem.objects
        .filter(activo=True)
        .select_related("producto", "producto__proveedor")
    )

    valor_inventario = Decimal("0.00")
    stock_bajo = 0
    agotados = 0
    bajo_objetivo = 0

    productos_bajo_objetivo = []
    productos_agotados = []

    for item in inventario_items:
        costo = item.costo_unitario or item.producto.costo_adquisicion or Decimal("0.00")
        valor_inventario += Decimal(item.stock_actual) * costo

        stock_objetivo = item.producto.stock_objetivo or 0

        if item.stock_actual <= 0:
            agotados += 1
            productos_agotados.append(item)

        if item.stock_actual <= item.stock_minimo:
            stock_bajo += 1

        if stock_objetivo > 0 and item.stock_actual < stock_objetivo:
            item.stock_objetivo_val = stock_objetivo
            item.diferencia_objetivo = item.stock_actual - stock_objetivo
            productos_bajo_objetivo.append(item)
            bajo_objetivo += 1

    productos_bajo_objetivo = sorted(
        productos_bajo_objetivo,
        key=lambda x: x.stock_actual
    )[:10]

    productos_agotados = productos_agotados[:10]

    productos_mas_vendidos = (
        venta_items_qs
        .values("producto__nombre")
        .annotate(total_vendido=Sum("cantidad"))
        .order_by("-total_vendido")[:10]
    )

    canal_ventas = (
        ventas_qs
        .values("canal")
        .annotate(
            total_ventas=Count("id"),
            total_facturado=Sum("total")
        )
        .order_by("-total_ventas")
    )

    productos_con_margen = []
    productos_qs = Producto.objects.filter(
        activo=True,
        precio__isnull=False,
        costo_adquisicion__isnull=False,
        precio__gt=0
    ).select_related("proveedor", "coleccion")

    for producto in productos_qs:
        margen = (producto.precio or Decimal("0.00")) - (producto.costo_adquisicion or Decimal("0.00"))
        if producto.precio and producto.precio > 0:
            margen_pct = (margen * Decimal("100")) / producto.precio
        else:
            margen_pct = Decimal("0.00")

        producto.margen = margen
        producto.margen_pct = margen_pct
        productos_con_margen.append(producto)

    productos_mayor_margen = sorted(
        productos_con_margen,
        key=lambda p: p.margen,
        reverse=True
    )[:10]

    margen_promedio = Decimal("0.00")
    if productos_con_margen:
        margen_promedio = sum((p.margen for p in productos_con_margen), Decimal("0.00")) / Decimal(len(productos_con_margen))

    ventas_recientes = ventas_qs.order_by("-created_at")[:8]
    pedidos_recientes = pedidos_qs.order_by("-created_at")[:8]

    lead_time_promedio = Decimal("0.00")
    proveedores_activos = Proveedor.objects.filter(activo=True)
    if proveedores_activos.exists():
        suma_lead = sum((Decimal(p.tiempo_entrega_dias) for p in proveedores_activos), Decimal("0.00"))
        lead_time_promedio = suma_lead / Decimal(proveedores_activos.count())

    context = {
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,

        "total_ventas": total_ventas,
        "total_pedidos": total_pedidos,
        "total_clientes": total_clientes,
        "clientes_recurrentes": clientes_recurrentes,
        "total_proveedores": total_proveedores,
        "total_productos": total_productos,

        "total_facturado": total_facturado,
        "ticket_promedio": ticket_promedio,
        "valor_inventario": valor_inventario,
        "stock_bajo": stock_bajo,
        "agotados": agotados,
        "bajo_objetivo": bajo_objetivo,
        "lead_time_promedio": lead_time_promedio,

        "productos_bajo_objetivo": productos_bajo_objetivo,
        "productos_agotados": productos_agotados,
        "productos_mas_vendidos": productos_mas_vendidos,
        "productos_mayor_margen": productos_mayor_margen,
        "margen_promedio": margen_promedio,

        "canal_ventas": canal_ventas,
        "ventas_recientes": ventas_recientes,
        "pedidos_recientes": pedidos_recientes,
    }

    return render(request, "dashboard/index.html", context)

@login_required
def panel_inventario(request):
    items_qs = (
        InventarioItem.objects
        .select_related("producto")
        .order_by("producto__nombre")
    )

    items = []
    total_items = 0
    agotados = 0
    stock_bajo = 0
    bajo_objetivo = 0

    for item in items_qs:
        total_items += 1

        stock_objetivo = item.producto.stock_objetivo or 0
        diferencia_objetivo = item.stock_actual - stock_objetivo

        if item.stock_actual <= 0:
            estado_ui = "Agotado"
            estado_color = "#b42318"
            agotados += 1
        elif item.stock_actual <= item.stock_minimo:
            estado_ui = "Stock bajo"
            estado_color = "#c96b16"
            stock_bajo += 1
        elif stock_objetivo > 0 and item.stock_actual < stock_objetivo:
            estado_ui = "Bajo objetivo"
            estado_color = "#7a5c3e"
            bajo_objetivo += 1
        else:
            estado_ui = "Correcto"
            estado_color = "#18794e"

        item.stock_objetivo_val = stock_objetivo
        item.diferencia_objetivo = diferencia_objetivo
        item.estado_ui = estado_ui
        item.estado_color = estado_color

        items.append(item)

    movimientos_recientes = (
        MovimientoInventario.objects
        .select_related("item", "item__producto")
        .order_by("-created_at")[:12]
    )

    return render(request, "dashboard/inventario.html", {
        "items": items,
        "total_items": total_items,
        "agotados": agotados,
        "stock_bajo": stock_bajo,
        "bajo_objetivo": bajo_objetivo,
        "movimientos_recientes": movimientos_recientes,
    })


@login_required
def panel_inventario_editar(request, item_id):
    item = get_object_or_404(
        InventarioItem.objects.select_related("producto"),
        id=item_id
    )

    if request.method == "POST":
        item.sku_interno = request.POST.get("sku_interno", "").strip()
        item.stock_minimo = int(request.POST.get("stock_minimo") or 0)
        item.costo_unitario = request.POST.get("costo_unitario") or None
        item.ubicacion = request.POST.get("ubicacion", "").strip()
        item.activo = request.POST.get("activo") == "on"
        item.save()

        messages.success(request, "Inventario actualizado correctamente.")
        return redirect("panel_inventario")

    return render(request, "dashboard/inventario_editar.html", {
        "item": item,
    })


@login_required
def panel_inventario_movimiento(request, item_id):
    item = get_object_or_404(
        InventarioItem.objects.select_related("producto"),
        id=item_id
    )

    if request.method == "POST":
        tipo = request.POST.get("tipo")
        cantidad = int(request.POST.get("cantidad") or 0)
        nota = request.POST.get("nota", "").strip()

        if tipo == "ajuste":
            movimiento = MovimientoInventario(
                item=item,
                tipo=tipo,
                cantidad=cantidad,
                nota=nota,
            )
        else:
            movimiento = MovimientoInventario(
                item=item,
                tipo=tipo,
                cantidad=abs(cantidad),
                nota=nota,
            )

        try:
            movimiento.save()
            messages.success(request, "Movimiento registrado correctamente.")
            return redirect("panel_inventario")
        except Exception as e:
            messages.error(request, f"No se pudo registrar el movimiento: {e}")

    return render(request, "dashboard/inventario_movimiento.html", {
        "item": item,
    })

@login_required
def panel_inventario_nuevo(request):
    productos_disponibles = (
        Producto.objects
        .filter(activo=True, inventario__isnull=True)
        .order_by("nombre")
    )

    if request.method == "POST":
        producto_id = request.POST.get("producto")
        sku_interno = request.POST.get("sku_interno", "").strip()
        stock_actual = int(request.POST.get("stock_actual") or 0)
        stock_minimo = int(request.POST.get("stock_minimo") or 0)
        costo_unitario = request.POST.get("costo_unitario") or None
        ubicacion = request.POST.get("ubicacion", "").strip()
        activo = request.POST.get("activo") == "on"

        producto = get_object_or_404(
            Producto.objects.filter(activo=True, inventario__isnull=True),
            id=producto_id
        )

        InventarioItem.objects.create(
            producto=producto,
            sku_interno=sku_interno,
            stock_actual=stock_actual,
            stock_minimo=stock_minimo,
            costo_unitario=costo_unitario,
            ubicacion=ubicacion,
            activo=activo,
        )

        messages.success(request, "Inventario creado correctamente.")
        return redirect("panel_inventario")

    return render(request, "dashboard/inventario_nuevo.html", {
        "productos_disponibles": productos_disponibles,
    })

@login_required
def panel_clientes(request):
    q = request.GET.get("q", "").strip()

    clientes_qs = (
        Cliente.objects
        .order_by("nombre")
        .prefetch_related("ventas")
    )

    if q:
        clientes_qs = clientes_qs.filter(nombre__icontains=q)

    clientes = []

    for cliente in clientes_qs:
        ventas_cliente = cliente.ventas.all().order_by("-created_at")
        total_compras = ventas_cliente.count()
        total_gastado = sum((venta.total for venta in ventas_cliente), Decimal("0.00"))
        ultima_compra = ventas_cliente.first()

        cliente.total_compras = total_compras
        cliente.total_gastado = total_gastado
        cliente.ultima_compra = ultima_compra

        clientes.append(cliente)

    return render(request, "dashboard/clientes.html", {
        "clientes": clientes,
        "q": q,
    })


@login_required
def panel_cliente_nuevo(request):
    if request.method == "POST":
        cliente = Cliente.objects.create(
            nombre=request.POST.get("nombre", "").strip(),
            telefono=request.POST.get("telefono", "").strip(),
            whatsapp=request.POST.get("whatsapp", "").strip(),
            email=request.POST.get("email", "").strip(),
            documento=request.POST.get("documento", "").strip(),
            ciudad=request.POST.get("ciudad", "").strip(),
            instagram=request.POST.get("instagram", "").strip(),
            notas=request.POST.get("notas", "").strip(),
            recurrente=request.POST.get("recurrente") == "on",
            activo=request.POST.get("activo") == "on",
        )
        messages.success(request, f"Cliente creado correctamente: {cliente.nombre}")
        return redirect("panel_clientes")

    return render(request, "dashboard/cliente_nuevo.html")


@login_required
def panel_cliente_editar(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)

    if request.method == "POST":
        cliente.nombre = request.POST.get("nombre", "").strip()
        cliente.telefono = request.POST.get("telefono", "").strip()
        cliente.whatsapp = request.POST.get("whatsapp", "").strip()
        cliente.email = request.POST.get("email", "").strip()
        cliente.documento = request.POST.get("documento", "").strip()
        cliente.ciudad = request.POST.get("ciudad", "").strip()
        cliente.instagram = request.POST.get("instagram", "").strip()
        cliente.notas = request.POST.get("notas", "").strip()
        cliente.recurrente = request.POST.get("recurrente") == "on"
        cliente.activo = request.POST.get("activo") == "on"
        cliente.save()

        messages.success(request, "Cliente actualizado correctamente.")
        return redirect("panel_clientes")

    return render(request, "dashboard/cliente_editar.html", {
        "cliente": cliente,
    })


@login_required
def panel_pedidos(request):
    q = request.GET.get("q", "").strip()
    estado = request.GET.get("estado", "").strip()

    pedidos = Pedido.objects.order_by("-created_at")

    if q:
        pedidos = pedidos.filter(nombre_cliente__icontains=q)

    if estado:
        pedidos = pedidos.filter(estado=estado)

    return render(request, "dashboard/pedidos.html", {
        "pedidos": pedidos,
        "q": q,
        "estado": estado,
        "estados": Pedido.ESTADOS,
    })


@login_required
def panel_pedido_detalle(request, pedido_id):
    pedido = get_object_or_404(
        Pedido.objects.prefetch_related("items__producto"),
        id=pedido_id
    )

    return render(request, "dashboard/pedido_detalle.html", {
        "pedido": pedido,
        "estados": Pedido.ESTADOS,
    })


@login_required
def panel_pedido_estado(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if request.method == "POST":
        nuevo_estado = request.POST.get("estado", "").strip()

        estados_validos = [key for key, _ in Pedido.ESTADOS]
        if nuevo_estado in estados_validos:
            pedido.estado = nuevo_estado
            pedido.save(update_fields=["estado"])
            messages.success(request, f"Estado del pedido #{pedido.id} actualizado a {pedido.get_estado_display()}.")
        else:
            messages.error(request, "Estado no válido.")

    return redirect("panel_pedido_detalle", pedido_id=pedido.id)



@login_required
def panel_proveedores(request):
    q = request.GET.get("q", "").strip()

    proveedores_qs = (
        Proveedor.objects
        .order_by("nombre")
        .prefetch_related("productos__inventario")
    )

    if q:
        proveedores_qs = proveedores_qs.filter(nombre__icontains=q)

    proveedores = []

    for proveedor in proveedores_qs:
        productos = list(proveedor.productos.all())
        total_productos = len(productos)

        total_stock = 0
        valor_stock = Decimal("0.00")

        for producto in productos:
            if hasattr(producto, "inventario"):
                inventario = producto.inventario
                total_stock += inventario.stock_actual

                costo = inventario.costo_unitario or producto.costo_adquisicion or Decimal("0.00")
                valor_stock += Decimal(inventario.stock_actual) * costo

        proveedor.total_productos = total_productos
        proveedor.total_stock = total_stock
        proveedor.valor_stock = valor_stock

        proveedores.append(proveedor)

    return render(request, "dashboard/proveedores.html", {
        "proveedores": proveedores,
        "q": q,
    })


@login_required
def panel_proveedor_nuevo(request):
    if request.method == "POST":
        proveedor = Proveedor.objects.create(
            nombre=request.POST.get("nombre", "").strip(),
            contacto=request.POST.get("contacto", "").strip(),
            telefono=request.POST.get("telefono", "").strip(),
            whatsapp=request.POST.get("whatsapp", "").strip(),
            email=request.POST.get("email", "").strip(),
            ciudad=request.POST.get("ciudad", "").strip(),
            pais=request.POST.get("pais", "").strip(),
            tiempo_entrega_dias=request.POST.get("tiempo_entrega_dias") or 0,
            notas=request.POST.get("notas", "").strip(),
            activo=request.POST.get("activo") == "on",
        )
        messages.success(request, f"Proveedor creado correctamente: {proveedor.nombre}")
        return redirect("panel_proveedores")

    return render(request, "dashboard/proveedor_nuevo.html")


from decimal import Decimal
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from ventas.models import Venta, VentaItem
from catalogo.models import Producto
from inventario.models import InventarioItem, MovimientoInventario
from clientes.models import Cliente


@login_required
def panel_ventas(request):
    q = request.GET.get("q", "").strip()
    canal = request.GET.get("canal", "").strip()

    ventas = Venta.objects.select_related("cliente").order_by("-created_at")

    if q:
        ventas = ventas.filter(cliente__nombre__icontains=q)

    if canal:
        ventas = ventas.filter(canal=canal)

    return render(request, "dashboard/ventas.html", {
        "ventas": ventas,
        "q": q,
        "canal": canal,
        "canales": Venta.CANALES,
    })


@login_required
def panel_venta_nueva(request):
    clientes = Cliente.objects.filter(activo=True).order_by("nombre")
    productos = Producto.objects.filter(activo=True).order_by("nombre")

    if request.method == "POST":
        cliente_id = request.POST.get("cliente")
        canal = request.POST.get("canal") or "tienda"
        notas = request.POST.get("notas", "").strip()

        producto_id = request.POST.get("producto")
        cantidad = int(request.POST.get("cantidad") or 1)
        descuento_porcentaje = Decimal(request.POST.get("descuento_porcentaje") or "0")

        cliente = None
        if cliente_id:
            cliente = Cliente.objects.filter(id=cliente_id).first()

        producto = get_object_or_404(Producto, id=producto_id, activo=True)

        inventario_item = InventarioItem.objects.filter(producto=producto, activo=True).first()
        if not inventario_item:
            messages.error(request, "Este producto no tiene inventario creado.")
            return redirect("panel_venta_nueva")

        if cantidad <= 0:
            messages.error(request, "La cantidad debe ser mayor a 0.")
            return redirect("panel_venta_nueva")

        if inventario_item.stock_actual < cantidad:
            messages.error(request, f"Stock insuficiente. Disponible: {inventario_item.stock_actual}")
            return redirect("panel_venta_nueva")

        precio_unitario = producto.precio or Decimal("0.00")
        subtotal = precio_unitario * cantidad
        descuento_valor = subtotal * (descuento_porcentaje / Decimal("100"))
        total = subtotal - descuento_valor

        with transaction.atomic():
            venta = Venta.objects.create(
                cliente=cliente,
                canal=canal,
                notas=notas,
                subtotal=subtotal,
                descuento_porcentaje=descuento_porcentaje,
                descuento_valor=descuento_valor,
                total=total,
            )

            VentaItem.objects.create(
                venta=venta,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=precio_unitario,
            )

            MovimientoInventario.objects.create(
                item=inventario_item,
                tipo="salida",
                cantidad=cantidad,
                nota=f"Venta #{venta.id}"
            )

        messages.success(request, f"Venta #{venta.id} creada correctamente.")
        return redirect("panel_venta_detalle", venta_id=venta.id)

    return render(request, "dashboard/venta_nueva.html", {
        "clientes": clientes,
        "productos": productos,
        "canales": Venta.CANALES,
    })


@login_required
def panel_venta_detalle(request, venta_id):
    venta = get_object_or_404(
        Venta.objects.select_related("cliente").prefetch_related("items__producto"),
        id=venta_id
    )

    return render(request, "dashboard/venta_detalle.html", {
        "venta": venta,
    })


@login_required
def panel_venta_eliminar(request, venta_id):
    venta = get_object_or_404(
        Venta.objects.prefetch_related("items__producto"),
        id=venta_id
    )

    if request.method == "POST":
        with transaction.atomic():
            for item in venta.items.all():
                inventario_item = InventarioItem.objects.filter(
                    producto=item.producto,
                    activo=True
                ).first()

                if inventario_item:
                    inventario_item.stock_actual += item.cantidad
                    inventario_item.save(update_fields=["stock_actual"])

                    MovimientoInventario.objects.create(
                        item=inventario_item,
                        tipo="entrada",
                        cantidad=item.cantidad,
                        nota=f"Reverso por eliminación venta #{venta.id}"
                    )

            venta.delete()

        messages.success(request, f"Venta #{venta_id} eliminada correctamente.")
        return redirect("panel_ventas")

    return render(request, "dashboard/venta_eliminar.html", {
        "venta": venta,
    })


@login_required
def panel_proveedor_editar(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)

    if request.method == "POST":
        proveedor.nombre = request.POST.get("nombre", "").strip()
        proveedor.contacto = request.POST.get("contacto", "").strip()
        proveedor.telefono = request.POST.get("telefono", "").strip()
        proveedor.whatsapp = request.POST.get("whatsapp", "").strip()
        proveedor.email = request.POST.get("email", "").strip()
        proveedor.ciudad = request.POST.get("ciudad", "").strip()
        proveedor.pais = request.POST.get("pais", "").strip()
        proveedor.tiempo_entrega_dias = request.POST.get("tiempo_entrega_dias") or 0
        proveedor.notas = request.POST.get("notas", "").strip()
        proveedor.activo = request.POST.get("activo") == "on"
        proveedor.save()

        messages.success(request, "Proveedor actualizado correctamente.")
        return redirect("panel_proveedores")

    return render(request, "dashboard/proveedor_editar.html", {
        "proveedor": proveedor,
    })

@login_required
def panel_compras(request):
    items_reponer = (
        InventarioItem.objects
        .select_related("producto", "producto__proveedor")
        .filter(
            activo=True,
            producto__activo=True,
            producto__stock_objetivo__gt=0,
            stock_actual__lt=F("producto__stock_objetivo")
        )
        .order_by("producto__proveedor__nombre", "producto__nombre")
    )

    compras_sugeridas = []
    total_estimado = Decimal("0.00")
    total_unidades = 0

    for item in items_reponer:
        producto = item.producto
        proveedor = producto.proveedor

        stock_objetivo = producto.stock_objetivo or 0
        cantidad_sugerida = stock_objetivo - item.stock_actual
        if cantidad_sugerida < 0:
            cantidad_sugerida = 0

        costo_unitario = item.costo_unitario or producto.costo_adquisicion or Decimal("0.00")
        costo_estimado = costo_unitario * Decimal(cantidad_sugerida)
        total_estimado += costo_estimado
        total_unidades += cantidad_sugerida

        if item.stock_actual <= 0:
            prioridad = "Crítica"
            prioridad_color = "#b42318"
        elif item.stock_actual <= item.stock_minimo:
            prioridad = "Alta"
            prioridad_color = "#c96b16"
        else:
            prioridad = "Media"
            prioridad_color = "#7a5c3e"

        compras_sugeridas.append({
            "item": item,
            "producto": producto,
            "proveedor": proveedor,
            "stock_actual": item.stock_actual,
            "stock_minimo": item.stock_minimo,
            "stock_objetivo": stock_objetivo,
            "cantidad_sugerida": cantidad_sugerida,
            "costo_unitario": costo_unitario,
            "costo_estimado": costo_estimado,
            "lead_time": proveedor.tiempo_entrega_dias if proveedor else producto.tiempo_adquisicion_dias,
            "prioridad": prioridad,
            "prioridad_color": prioridad_color,
        })

    total_productos_reponer = len(compras_sugeridas)

    proveedores_involucrados = len({
        c["proveedor"].id for c in compras_sugeridas if c["proveedor"]
    })

    return render(request, "dashboard/compras.html", {
        "compras_sugeridas": compras_sugeridas,
        "total_estimado": total_estimado,
        "total_unidades": total_unidades,
        "total_productos_reponer": total_productos_reponer,
        "proveedores_involucrados": proveedores_involucrados,
    })