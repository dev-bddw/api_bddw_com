from django.urls import path

from .views_v1 import api_create_menulist, api_create_product, api_drop_down_menu, api_landing_page_images, api_response
from .views_v2 import products, menu_lists, product_images, landing_page_images, menu_list_items

app_name = "api"

# api v1 patterns this is what bddw.com consumes currently

urlpatterns = [
    path("create-product", api_create_product, name="create-product"),  # create
    path("create-menulist", api_create_menulist, name="create-menulist"),  # create
    path("drop-down-menu", api_drop_down_menu, name="drop-down-menu"),
    path("landing-page-images", api_landing_page_images, name="landing-page-images"),
    path("<slug>", api_response, name="api-endpoint"),  # upadate or read
    ]

# api v2 patterns this is the api the editor will use
urlpatterns += [
    path('v2/products/<product_name_slug>', products),
    path('v2/menu-lists/<menu_list_slug>', menu_lists),
    path('v2/menu-list-items/<menu_list_item_id>', menu_list_items),
    path('v2/product-images/<product_image_id>', product_images),
    path('v2/landing-page-images/<landing_page_image_id>', landing_page_images),
    # To Do add drop down menu
    ]


