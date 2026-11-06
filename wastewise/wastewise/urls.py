"""
URL configuration for wastewise project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='pickups:dashboard', permanent=False)),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.web_urls')),
    path('pickups/', include('pickups.urls')),  # Include the pickups app URLs
    path('rubbish/', include('rubbish.urls')), # Include the rubbish management app URLs
    path('', include('collectors.urls')), # Include the collectors app URLs
    path('api/', include('payments.urls')), # Include the payments app URLs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path("api/auth/", include("accounts.urls")),
    path("api/profile/", include("profiles.urls")),
    
]
