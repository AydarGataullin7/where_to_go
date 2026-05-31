from adminsortable2.admin import SortableInlineAdminMixin, SortableAdminBase
from django.contrib import admin
from django.utils.html import format_html

from .models import Place, Images


class ImagesInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Images
    extra = 1
    readonly_fields = ['image_preview']
    fields = ['image', 'image_preview', 'order']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 200px; max-width: 200px" />', obj.image.url)
        return "Нет изображения"

    image_preview.short_description = "Превью"


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_preview', 'place', 'order']
    list_display_links = ['id', 'image_preview']
    list_filter = ['place']
    search_fields = ['place__title']
    raw_id_fields = ['place']
    readonly_fields = ['image_preview']
    fields = ['image', 'image_preview', 'place', 'order']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 200px; max-width: 200px" />', obj.image.url)
        return "Нет изображения"

    image_preview.short_description = "Превью"


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [ImagesInline]
    list_display = ['title', 'latitude', 'longitude']
    search_fields = ['title']
