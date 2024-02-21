from django.urls import path

from .views import api_create_menulist, api_create_product, api_drop_down_menu, api_landing_page_images, api_response

app_name = "api"

urlpatterns = [
    path("create-product", api_create_product, name="create-product"),  # create
    path("create-menulist", api_create_menulist, name="create-menulist"),  # create
    path("drop-down-menu", api_drop_down_menu, name="drop-down-menu"),
    path("landing-page-images", api_landing_page_images, name="landing-page-images"),
    path("<slug>", api_response, name="api-endpoint"),  # upadate or read
]
