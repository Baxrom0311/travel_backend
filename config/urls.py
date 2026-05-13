"""
Root URL configuration.

Clean architecture:
  /admin/           → Django admin
  /health/          → Health check
  /api/             → API overview (core app)
  /api/home/        → Home summary (core app)
  /api/search/      → Global search (core app)
  /api/hotels/      → Hotels app
  /api/amenities/   → Hotels app (nested)
  /api/transport/   → Transport app
  /api/attractions/ → Attractions app
  /api/events/      → Events app
  /api/news/        → News app
  /api/contact/     → Contact app
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.db import connection
from django.db.utils import Error as DatabaseError
from django.http import JsonResponse
from django.utils import timezone
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


def health_check(request):
    """GET /health/"""
    status_code = 200
    database_status = 'ok'
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
            cursor.fetchone()
    except DatabaseError:
        status_code = 503
        database_status = 'unavailable'

    return JsonResponse({
        'status': 'ok' if status_code == 200 else 'degraded',
        'service': 'Visit Khorezm API',
        'version': '2.0.0',
        'database': database_status,
        'time': timezone.now().isoformat(),
    }, status=status_code)


def handler404(request, exception):
    return JsonResponse({
        'success': False,
        'status_code': 404,
        'error': 'Sahifa topilmadi',
        'detail': str(request.path),
    }, status=404)


def handler500(request):
    return JsonResponse({
        'success': False,
        'status_code': 500,
        'error': 'Server xatosi',
    }, status=500)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health-check'),

    # API docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Core (home, overview, search)
    path('api/', include('core.urls')),

    # Auth
    path('api/auth/', include('users.urls')),

    # Domain apps
    path('api/', include('hotels.urls')),
    path('api/transport/', include('transport.urls_v2')),
    path('api/attractions/', include('attractions.urls')),
    path('api/events/', include('events.urls')),
    path('api/news/', include('news.urls')),
    path('api/contact/', include('contact.urls')),
    path('api/restaurants/', include('restaurants.urls')),
    path('api/tours/', include('tours.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('api/newsletter/', include('newsletter.urls')),
    path('api/settings/', include('settings_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
