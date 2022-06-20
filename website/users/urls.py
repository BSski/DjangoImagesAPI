from django.urls import include, path
from users.views import home
from rest_framework.routers import DefaultRouter
from .views import UserViewSet


router = DefaultRouter()
router.register("users", UserViewSet, basename="users")


urlpatterns = [
    path("home/", home),
    path("", include(router.urls)),
]
