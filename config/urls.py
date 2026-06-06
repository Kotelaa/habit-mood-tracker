from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from drf_spectacular.views import (
    SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
)

from habits import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('habits.urls')),

    # Auth urls
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),

    #Api urls
    path('api/', include('habits.api_urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger_ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'),
         name='redoc'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
