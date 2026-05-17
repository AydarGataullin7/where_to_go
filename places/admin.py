from django.contrib import admin
from .models import Place, Images


class ImagesInline(admin.TabularInline):
    model = Images
    extra = 1


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [ImagesInline]
    list_display = ['title', 'latitude', 'longitude']
    search_fields = ['title']
