from django.contrib import admin
from .models import Product, ProductImage, MenuList, MenuListItem, DropDownMenu
from .forms import DropDownMenuModelForm
from reversion.admin import VersionAdmin


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 10


@admin.register(DropDownMenu)
class DropDownMenuAdmin(VersionAdmin):
    form = DropDownMenuModelForm


@admin.register(Product)
class ProductAdmin(VersionAdmin):
    inlines = [ProductImageInline]
    list_display = ("name", "created_on")
    search_fields = ("name",)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


# @admin.register(ProductImage)
# class ProductImageAdmin(admin.ModelAdmin):
#     list_display = ("product", "order", "created_on")
#     list_filter = ("product",)
#     search_fields = ("product__name",)


class MenuListItemInline(admin.TabularInline):
    model = MenuListItem
    extra = 10


@admin.register(MenuList)
class MenuListAdmin(VersionAdmin):
    inlines = [MenuListItemInline]
    list_display = ("name", "created_on")
    search_fields = ("name",)


# @admin.register(MenuListItem)
# class MenuListItemAdmin(admin.ModelAdmin):
#     list_display = ("name", "menu_list", "order", "url")
#     list_filter = ("menu_list",)
#     search_fields = ("name", "menu_list__name")


# Registering models with inlines
admin.site.unregister(Product)
admin.site.register(Product, ProductAdmin)
admin.site.unregister(MenuList)
admin.site.register(MenuList, MenuListAdmin)
