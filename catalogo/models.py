from django.db import models


class Coleccion(models.Model):
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to="catalogo/colecciones/", blank=True, null=True)
    orden = models.PositiveIntegerField(default=0)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    coleccion = models.ForeignKey(
        Coleccion,
        on_delete=models.CASCADE,
        related_name="productos"
    )

    artesano = models.ForeignKey(
        "artesanos.Artesano",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="productos"
    )

    material = models.CharField(max_length=200, blank=True)
    medidas = models.CharField(max_length=200, blank=True)
    destacado = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)

    peso_gramos = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notas_internas = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


class ProductoImagen(models.Model):
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name="imagenes"
    )
    imagen = models.ImageField(upload_to="catalogo/productos/")
    orden = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Imagen {self.producto.nombre}"