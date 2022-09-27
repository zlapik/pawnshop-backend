from django.contrib import admin
from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from authentication.views import UserViewSet
from shop.views import ShopViewSet

#####

schema_view = get_schema_view(
    openapi.Info(
        title="Pawnshop API",
        default_version="v1",
        description="A REST API for a Pawnshop system",
        contact=openapi.Contact(email="lapes.zdenek@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]

router = routers.DefaultRouter()
router.register(prefix="shops", viewset=ShopViewSet)
router.register(prefix="users", viewset=UserViewSet)

urlpatterns += [
    path("admin/", admin.site.urls),
]

urlpatterns += router.urls
