from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from where_to_go import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.show_map),
    path('places/<int:place_id>/', views.place_detail, name='place_detail'),
    path('tinymce/', include('tinymce.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.BASE_DIR / 'static')
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
