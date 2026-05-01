from django.db import models


class Place(models.Model):
    title = models.CharField(max_length=200)
    description_short = models.TextField()
    description_long = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.title


class Images(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='places_images/')
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.order} - {self.place.title}"
