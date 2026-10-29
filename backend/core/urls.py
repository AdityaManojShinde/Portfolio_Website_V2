from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from datetime import datetime, timezone
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)


def api_root(request):
    return JsonResponse({
        "message": "Welcome to the API",
        "datetime": datetime.now(timezone.utc).isoformat(),
    })


urlpatterns = [

    path("", api_root, name="api-root"),
    path("admin/", admin.site.urls),
    path(
        "api-auth/",
        include("rest_framework.urls", namespace="rest_framework"),
    ),
    
    # Blog API
    path("api/", include("blog.urls")),
    
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("ckeditor5/", include("django_ckeditor_5.urls")),

] 


admin.site.site_title = "Aditya's Admin Panel"