from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('questions.urls')),
    path('', include('core.urls')),  # <-- Добавили
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include('debug_toolbar.urls')),
    ] + urlpatterns
    # Раздача медиа-файлов при DEBUG=True (ТЗ 7)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)