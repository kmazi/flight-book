"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path("", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path("", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from api.urls import router
from user.urls import router as user_router
from api.views import home
from rest_framework_swagger.views import get_swagger_view


schema_view = get_swagger_view(title="Flightbookie API")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("v1/", include(router.urls)),
    path("account/", include(user_router.urls)),
    path("docs/", schema_view),
    path("api/token/",
         TokenObtainPairView.as_view(),
         name="token_obtain_pair"),
    path("api/token/refresh/",
         TokenRefreshView.as_view(),
         name="token_refresh"),
    path("", home, name="home")
]
