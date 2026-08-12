from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ContactoInfo(TimeStampedModel):
    telefono = models.CharField(max_length=50, blank=True)
    whatsapp = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    horario = models.CharField(max_length=255, blank=True)
    mapa_embed = models.TextField(blank=True)
    instagram_url = models.URLField(blank=True)

    ubicacion_titulo = models.CharField(max_length=255, blank=True, default="Visítanos en tienda")
    ubicacion_texto = models.TextField(blank=True, default="Descubre el espacio físico de Poppy Cartagena y vive la marca de cerca.")
    ubicacion_imagen = models.ImageField(upload_to="web/ubicacion/", blank=True, null=True)

    instagram_titulo_pagina = models.CharField(max_length=255, blank=True, default="Síguenos en Instagram")
    instagram_texto_pagina = models.TextField(blank=True, default="Descubre el universo visual de Poppy Cartagena: piezas, procesos, tienda y contexto.")
    instagram_imagen_1 = models.ImageField(upload_to="web/instagram/", blank=True, null=True)
    instagram_imagen_2 = models.ImageField(upload_to="web/instagram/", blank=True, null=True)
    instagram_imagen_3 = models.ImageField(upload_to="web/instagram/", blank=True, null=True)
    instagram_imagen_4 = models.ImageField(upload_to="web/instagram/", blank=True, null=True)
    instagram_cta_titulo = models.CharField(max_length=255, blank=True, default="Explora más en nuestro perfil")
    instagram_cta_texto = models.TextField(blank=True, default="Síguenos para descubrir nuevas piezas, historias y procesos detrás de cada objeto.")

    def __str__(self):
        return "Información de contacto"


class HistoriaPagina(TimeStampedModel):
    titulo = models.CharField(max_length=200)
    subtitulo = models.CharField(max_length=255, blank=True)

    imagen_principal = models.ImageField(upload_to="web/historia/", blank=True, null=True)

    intro_label = models.CharField(max_length=100, blank=True, default="Nuestra historia")
    intro_titulo = models.CharField(max_length=255, blank=True)
    intro_texto_1 = models.TextField(blank=True)
    intro_texto_2 = models.TextField(blank=True)

    bloque_2_label = models.CharField(max_length=100, blank=True, default="Origen")
    bloque_2_titulo = models.CharField(max_length=255, blank=True)
    bloque_2_texto = models.TextField(blank=True)
    bloque_2_imagen = models.ImageField(upload_to="web/historia/", blank=True, null=True)

    destacado_label = models.CharField(max_length=100, blank=True, default="Lo que nos mueve")
    destacado_titulo = models.CharField(max_length=255, blank=True)
    destacado_texto = models.TextField(blank=True)

    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo


class HeroHome(TimeStampedModel):
    titulo = models.CharField(max_length=200)
    subtitulo = models.CharField(max_length=255, blank=True)
    imagen = models.ImageField(upload_to="web/home/", blank=True, null=True)
    boton_texto = models.CharField(max_length=100, blank=True)
    boton_url = models.CharField(max_length=255, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo


class HomeContenido(TimeStampedModel):
    nombre = models.CharField(max_length=150, default="Home principal")
    activa = models.BooleanField(default=True)

    intro_label = models.CharField(max_length=100, blank=True, default="Nuestra esencia")
    intro_titulo = models.CharField(max_length=255, blank=True)
    intro_texto_1 = models.TextField(blank=True)
    intro_texto_2 = models.TextField(blank=True)
    intro_imagen = models.ImageField(upload_to="web/home/intro/", blank=True, null=True)

    colecciones_label = models.CharField(max_length=100, blank=True, default="Colecciones")
    colecciones_titulo = models.CharField(max_length=255, blank=True)
    colecciones_texto = models.TextField(blank=True)

    destacados_label = models.CharField(max_length=100, blank=True, default="Productos destacados")
    destacados_titulo = models.CharField(max_length=255, blank=True, default="Una selección representativa de la marca")
    destacados_texto = models.TextField(blank=True, default="Piezas elegidas para mostrar la identidad, materiales y carácter de Poppy.")

    proceso_label = models.CharField(max_length=100, blank=True, default="Proceso")
    proceso_titulo = models.CharField(max_length=255, blank=True)

    proceso_1_titulo = models.CharField(max_length=150, blank=True, default="Selección")
    proceso_1_texto = models.TextField(blank=True)
    proceso_imagen_1 = models.ImageField(upload_to="web/home/proceso/", blank=True, null=True)

    proceso_2_titulo = models.CharField(max_length=150, blank=True, default="Trabajo manual")
    proceso_2_texto = models.TextField(blank=True)
    proceso_imagen_2 = models.ImageField(upload_to="web/home/proceso/", blank=True, null=True)

    proceso_3_titulo = models.CharField(max_length=150, blank=True, default="Curaduría final")
    proceso_3_texto = models.TextField(blank=True)
    proceso_imagen_3 = models.ImageField(upload_to="web/home/proceso/", blank=True, null=True)

    banda_label = models.CharField(max_length=100, blank=True, default="Hecho en contexto")
    banda_titulo = models.CharField(max_length=255, blank=True)
    banda_texto = models.TextField(blank=True)

    tienda_label = models.CharField(max_length=100, blank=True, default="Tienda")
    tienda_titulo = models.CharField(max_length=255, blank=True)
    tienda_texto = models.TextField(blank=True)
    tienda_boton_texto = models.CharField(max_length=100, blank=True, default="Ver ubicación")
    tienda_boton_url = models.CharField(max_length=255, blank=True, default="/ubicacion/")
    tienda_imagen = models.ImageField(upload_to="web/home/tienda/", blank=True, null=True)

    instagram_label = models.CharField(max_length=100, blank=True, default="Instagram")
    instagram_titulo = models.CharField(max_length=255, blank=True)
    instagram_texto = models.TextField(blank=True)
    instagram_boton_texto = models.CharField(max_length=100, blank=True, default="Ir a Instagram")
    instagram_boton_url = models.CharField(max_length=255, blank=True, default="/instagram/")
    instagram_imagen_1 = models.ImageField(upload_to="web/home/instagram/", blank=True, null=True)
    instagram_imagen_2 = models.ImageField(upload_to="web/home/instagram/", blank=True, null=True)
    instagram_imagen_3 = models.ImageField(upload_to="web/home/instagram/", blank=True, null=True)
    instagram_imagen_4 = models.ImageField(upload_to="web/home/instagram/", blank=True, null=True)

    def __str__(self):
        return self.nombre


class HomeColeccion(TimeStampedModel):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to="web/colecciones/", blank=True, null=True)
    coleccion_catalogo = models.ForeignKey(
        "catalogo.Coleccion",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="cards_home",
    )
    orden = models.PositiveIntegerField(default=0)
    activa = models.BooleanField(default=True)

    class Meta:
        ordering = ["orden", "id"]

    def __str__(self):
        return self.nombre