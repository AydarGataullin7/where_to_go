from django.db import models

from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description_short = models.TextField(
        verbose_name="Короткое описание", blank=True)
    description_long = HTMLField(verbose_name="Полное описание", blank=True)
    latitude = models.FloatField(verbose_name="Широта")
    longitude = models.FloatField(verbose_name="Долгота")

    def __str__(self):
        return self.title


class Images(models.Model):
    place = models.ForeignKey(
        Place, on_delete=models.CASCADE, related_name='images', verbose_name="Место")
    image = models.ImageField(
        upload_to='places_images/', verbose_name="Изображение")
    order = models.IntegerField(default=0, verbose_name="Порядок")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.order} - {self.place.title}"
