from django.contrib import admin
from django.urls import include, path

from . import settings

urlpatterns = [
    path("", include("recipes.urls")),
    path("admin/", admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
]
