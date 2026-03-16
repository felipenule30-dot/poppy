from django.db import models


class Artesano(models.Model):

    nombre = models.CharField(max_length=200)

    slug = models.SlugField(unique=True)

    foto = models.ImageField(upload_to="artesanos/", blank=True, null=True)

    region = models.CharField(max_length=200, blank=True)

    tecnica = models.CharField(max_length=200, blank=True)

    bio_corta = models.TextField(blank=True)

    bio_larga = models.TextField(blank=True)

    destacado = models.BooleanField(default=False)

    activo = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.nombre