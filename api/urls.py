from django.urls import include, path

from .views import api_response, api_create_product, api_create_menulist, api_drop_down_menu

app_name = "api"

urlpatterns = [
    path("create-product", api_create_product, name="create-product"),  # create
    path("create-menulist", api_create_menulist, name="create-menulist"),  # create
    path("drop-down-menu", api_drop_down_menu, name="drop-down-menu"),
    path("<slug>", api_response, name="api-endpoint"),  # upadate or read
]
