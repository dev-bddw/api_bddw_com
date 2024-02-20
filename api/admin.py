from django.contrib import admin
from .models import Product, ProductImage, MenuList, MenuListItem, DropDownMenu, LandingPageImage
from .forms import DropDownMenuModelForm
from reversion.admin import VersionAdmin
from django.utils.html import format_html


@admin.register(DropDownMenu)
class DropDownMenuAdmin(VersionAdmin):
    form = DropDownMenuModelForm


@admin.register(LandingPageImage)
class LandingPageImageAdmin(VersionAdmin):
    list_display = ["thumbnail_list_display", "dimensions", "image_name"]
    fields = [
        "image_display",
        "image",
    ]

    readonly_fields = ["image_display"]  # Ensure image_thumbnail is treated as a read-only field,

    def image_display(self, obj):
        return format_html('<img src="{}" width="1500" />', obj.image.url)

    def dimensions(self, obj):
        width, height = obj.image.width, obj.image.height
        return format_html("<p>{} x {}</p>", width, height)

    def thumbnail_list_display(self, obj):
        return format_html('<img src="{}" width="75" />', obj.thumbnail.url)

    def image_name(self, obj):
        return obj.image.name


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    fields = ["image_thumbnail", "image", "order", "caption"]
    readonly_fields = ["image_thumbnail"]  # Ensure image_thumbnail is treated as a read-only field,

    def image_thumbnail(self, obj):
        return format_html('<img src="{}" width="75" />', obj.thumbnail.url)


@admin.register(Product)
class ProductAdmin(VersionAdmin):
    inlines = [ProductImageInline]
    list_display = ("name", "get_absolute_url", "image_number", "get_blurb_preview")
    search_fields = ("name",)


@admin.register(ProductImage)
class ProductImageAdmin(VersionAdmin):
    list_display = ("image_thumbnail_list", "product", "order", "image", "created_on", "dimensions")
    list_filter = ("product",)
    search_fields = ("product__name", "image")
    fields = ["image_thumbnail", "image", "product", "order", "caption"]
    readonly_fields = ["image_thumbnail"]  # Ensure image_thumbnail is treated as a read-only field

    def image_thumbnail_list(self, obj):
        return format_html('<img src="{}" height="40"  />', obj.thumbnail.url)

    def image_thumbnail(self, obj):
        return format_html('<img src="{}" width="300"  />', obj.thumbnail.url)

    def dimensions(self, obj):
        width, height = obj.image.width, obj.image.height
        return format_html("<p>{} x {}</p>", width, height)


class MenuListItemInline(admin.TabularInline):
    model = MenuListItem
    extra = 10
    fields = [
        "name",
        "image_thumbnail",
        "image",
        "url",
        "order",
    ]
    readonly_fields = ["image_thumbnail"]  # Ensure image_thumbnail is treated as a read-only field

    def image_thumbnail(self, obj):
        return format_html('<img src="{}" width="75" />', obj.image.url)


@admin.register(MenuList)
class MenuListAdmin(VersionAdmin):
    inlines = [MenuListItemInline]
    list_display = ("name", "get_absolute_url", "number_of_list_items", "created_on")
    search_fields = ["name"]


@admin.register(MenuListItem)
class MenuListItemAdmin(VersionAdmin):
    list_display = ("name", "menu_list", "order", "image", "url")
    list_filter = ("menu_list",)
    search_fields = ("name", "menu_list__name", "image")
    fields = ["name", "image_thumbnail", "url", "order"]
    readonly_fields = ["image_thumbnail"]  # Ensure image_thumbnail is treated as a read-only field

    def image_thumbnail(self, obj):
        return format_html('<img src="{}" width="75" />', obj.image.url)


# Registering models with inlines
admin.site.unregister(Product)
admin.site.register(Product, ProductAdmin)
admin.site.unregister(MenuList)
admin.site.register(MenuList, MenuListAdmin)
