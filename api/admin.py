from django.contrib import admin
from django.utils.html import format_html
from reversion.admin import VersionAdmin

from .forms import DropDownMenuModelForm
from .models import DropDownMenu, LandingPageImage, MenuList, MenuListItem, Product, ProductImage


@admin.register(DropDownMenu)
class DropDownMenuAdmin(VersionAdmin):
    form = DropDownMenuModelForm


@admin.register(LandingPageImage)
class LandingPageImageAdmin(VersionAdmin):
    list_display = ["thumbnail_list_display", "dimensions", "image_name", "updated_on"]
    fields = [
        "image_display",
        "image",
    ]

    readonly_fields = ["image_display"]  # Ensure image_thumbnail is treated as a read-only field,
    ordering = ['-updated_on']

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
    list_display = ("name", "get_absolute_url_link", "image_number", "get_blurb_preview", "updated_on")
    search_fields = ("name",)
    ordering = ['-updated_on']


@admin.register(ProductImage)
class ProductImageAdmin(VersionAdmin):
    list_display = ("image_thumbnail_list", "product", "order", "image", "updated_on", "dimensions")
    list_filter = ("product",)
    search_fields = ("product__name", "image")
    fields = ["image_thumbnail", "image", "product", "order", "caption"]
    readonly_fields = ["image_thumbnail"]  # Ensure image_thumbnail is treated as a read-only field
    ordering = ['-updated_on']

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
    list_display = ("name", "get_absolute_url_link", "number_of_list_items", "updated_on")
    search_fields = ["name"]
    ordering = ['-updated_on']

@admin.register(MenuListItem)
class MenuListItemAdmin(VersionAdmin):
    list_display = ("name", "menu_list", "order", "image", "get_absolute_url_link", "updated_on")
    list_filter = ("menu_list",)
    search_fields = ("name", "menu_list__name", "image")
    fields = ["name", "menu_list", "image_thumbnail", "url", "order"]
    readonly_fields = ["image_thumbnail"]  # Ensure image_thumbnail is treated as a read-only field
    ordering = ['-updated_on']

    def image_thumbnail(self, obj):
        return format_html('<img src="{}" width="75" />', obj.image.url)


# Registering models with inlines
admin.site.unregister(Product)
admin.site.register(Product, ProductAdmin)
admin.site.unregister(MenuList)
admin.site.register(MenuList, MenuListAdmin)
