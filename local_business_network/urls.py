from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('business/', include('business.urls')),  # Include URLs from the business app
    path('accounts/', include('allauth.urls')),  # Include Allauth URLs
    path('', RedirectView.as_view(url='/business/', permanent=True)),  # Redirect root to business index
    # path("ai_features/", include("ai_features.urls")),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 