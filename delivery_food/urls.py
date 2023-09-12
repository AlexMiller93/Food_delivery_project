"""
URL configuration for delivery_food project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from drf_spectacular.views import (SpectacularAPIView,
                                   SpectacularSwaggerView,
                                   SpectacularRedocView)

from rest_framework.authtoken import views as rest_views

urlpatterns = [
    # http://localhost:8000/admin/
    path('admin/', admin.site.urls),

    # apps
    # http://localhost:8000/
    # http://localhost:8000/users/

    path('', include('menu.urls')),
    path('users/', include('accounts.urls')),
]

urlpatterns += [
    path('api-auth/', include('rest_framework.urls'), name='rest_framework'),

    path('api-token-auth/', rest_views.obtain_auth_token, name='api-token-auth'),


    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]