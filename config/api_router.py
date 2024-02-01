from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from api_bddw_com.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)


app_name = "api"
urlpatterns = router.urls
