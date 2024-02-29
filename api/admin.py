from django.contrib import admin
from django.utils.html import format_html
from reversion.admin import VersionAdmin
import requests

from .forms import DropDownMenuModelForm
from .models import DropDownMenu, LandingPageImage, MenuList, MenuListItem, Product, ProductImage


@admin.register(DropDownMenu)
class DropDownMenuAdmin(VersionAdmin):
    form = DropDownMenuModelForm


@admin.register(LandingPageImage)
class LandingPageImageAdmin(VersionAdmin):
    """
    Admin interface for the LandingPageImage model.

    It provides a list display with thumbnail, dimensions, image's name and updated date.
    It also ensures that the image is treated as a read-only field.
    """

    list_display = ["thumbnail_list_display", "dimensions", "image_name", "updated_on"]
    fields = ["image_display", "image"]
    readonly_fields = ["image_display"]  # Ensure image_thumbnail is treated as a read-only field,
    ordering = ["-updated_on"]

    def image_display(self, obj):
        """
        Method to display the image thumbnail in the admin interface.

        Args:
            obj (LandingPageImage): The LandingPageImage instance.

        Returns:
            str: HTML representation of the image.
        """
        return format_html('<img src="{}" width="1500" />', obj.image.url)

    def dimensions(self, obj):
        """
        Method to display the dimensions of the image.

        Args:
            obj (LandingPageImage): The LandingPageImage instance.

        Returns:
            str: HTML string displaying the width and height of the image.
        """
        width, height = obj.image.width, obj.image.height
        return format_html("<p>{} x {}</p>", width, height)

    def thumbnail_list_display(self, obj):
        """
        Method to display a thumbnail of the image in the list display of the admin interface.

        Args:
            obj (LandingPageImage): The LandingPageImage instance.

        Returns:
            str: HTML representation of the thumbnail.
        """
        return format_html('<img src="{}" width="75" />', obj.thumbnail.url)

    def image_name(self, obj):
        """
        Method to obtain the name of the image file.

        Args:
            obj (LandingPageImage): The LandingPageImage instance.

        Returns:
            str: The name of the image file.
        """
        return obj.image.name


class ProductImageInline(admin.TabularInline):
    """
    Django admin inline class for ProductImage. This class is used to represent
    a ProductImage object in the Django admin interface.

    Attributes:
        model (django.db.models.Model): Model for this Inline class.
            Should be a ProductImage model.
        fields (list): A list of field names to display in addition to the
            default ones. All fields should be a valid field in the model
            ProductImage.
        readonly_fields (list): A list of field names that will be displayed
            as read-only.

    Methods:
        image_thumbnail(self, obj): Method to display the thumbnail of a
            ProductImage instance.
    """

    model = ProductImage
    fields = ["image_thumbnail", "image", "order", "caption"]
    readonly_fields = ["image_thumbnail"]  # Ensure image_thumbnail is treated as a read-only field,

    def image_thumbnail(self, obj):
        """
        Returns an HTML snippet that represents a thumbnail image of the
        ProductImage instance.

        Args:
            obj (ProductImage): The ProductImage instance for which the
                thumbnail image needs to be displayed.

        Returns:
            django.utils.html.format_html: HTML snippet that represents a
                thumbnail image.

        Raises:
            AttributeError: If the thumbnail attribute of the ProductImage
                instance does not have a 'url' attribute.
        """

        return format_html('<img src="{}" width="75" />', obj.thumbnail.url)


@admin.register(Product)
class ProductAdmin(VersionAdmin):
    """
    Admin interface for Product Model with version control provided by VersionAdmin.

    Attributes:
        inlines (list): A list of inline model class instances for the admin interface.
        list_display (tuple): A tuple of field names to display on the admin interface's list page.
        search_fields (tuple): A tuple defining search-enabled fields for the admin interface.
        ordering (list): A list specifying the order in which records are listed in the admin interface.
    """

    # Inline models for the product
    inlines = [ProductImageInline]

    # Fields to display in the Product list in the Admin interface
    list_display = ("name", "get_absolute_url_link", "image_number", "get_blurb_preview", "updated_on")

    # Fields to be used in searching in the Admin interface
    search_fields = ("name",)

    # Ordering of the products in the Admin interface based on 'updated_on' field in descending order
    ordering = ["-updated_on"]


@admin.register(ProductImage)
class ProductImageAdmin(VersionAdmin):
    """
    The ProductImageAdmin class is a django ModelAdmin subclass customized for the
    ProductImage model. It adds extra features like search, filter and ordering functionality
    to the admin interface for ProductImage model.
    """

    list_display = ("image_thumbnail_list", "product", "order", "image", "updated_on", "dimensions", 'image_file_size')
    list_filter = ("product",)
    search_fields = ("product__name", "image")
    fields = ["image_thumbnail", "image", "product", "order", "caption"]
    readonly_fields = ["image_thumbnail"]  # Ensure image_thumbnail is treated as a read-only field
    ordering = ["-updated_on"]
    list_per_page = 20

    def image_file_size(self, obj):
        img_mb = obj.image.size / 1048576
        too_big = img_mb > 1
        return format_html(f'<p style="color: {'red' if too_big == True else 'black'};">{round(img_mb, 3)} mb</p>')

    def image_thumbnail_list(self, obj):
        """
        Creates a thumbnail for display in the list view.

        Args:
            obj (ProductImage): The current ProductImage object.

        Returns:
            str: A string of HTML displaying the thumbnail image.
        """
        return format_html('<img src="{}" height="40"  />', obj.thumbnail.url)

    def image_thumbnail(self, obj):
        """
        Creates a larger thumbnail for display in the detail view.

        Args:
            obj (ProductImage): The current ProductImage object.

        Returns:
            str: A string of HTML displaying the thumbnail image.
        """
        return format_html('<img src="{}" width="300"  />', obj.thumbnail.url)

    def dimensions(self, obj):
        """
        Gets the dimensions of the image.

        Args:
            obj (ProductImage): The current ProductImage object.

        Returns:
            str: A string of HTML displaying the width and height of the image.
        """
        width, height = obj.image.width, obj.image.height
        return format_html("<p>{} x {}</p>", width, height)


class MenuListItemInline(admin.TabularInline):
    """
    Inline model to display MenuListItem objects related to a specific MenuList in the admin interface.
    """

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
        """
        Returns the HTML representation of the image thumbnail for a MenuListItem object.

        Parameters:
        obj (MenuListItem): The MenuListItem object.

        Returns:
        str: HTML string that represents the image thumbnail.
        """
        return format_html('<img src="{}" width="75" />', obj.image.url)


@admin.register(MenuList)
class MenuListAdmin(VersionAdmin):
    """
    This is the admin interface for the MenuList model with VersionAdmin as the base class.
    It displays the list of MenuList objects in the admin interface with specific fields.
    It also allows searching and ordering these objects.
    """

    inlines = [MenuListItemInline]
    list_display = ("name", "get_absolute_url_link", "number_of_list_items", "updated_on")
    search_fields = ["name"]
    ordering = ["-updated_on"]




@admin.register(MenuListItem)
class MenuListItemAdmin(VersionAdmin):
    """
    This is the admin interface for the MenuListItem model with VersionAdmin as the base class.
    It displays the list of MenuListItem objects in the admin interface with specific fields.
    It also allows searching, filtering and ordering these objects.

    """

    list_display = ("name", "menu_list", "order", "image", "get_absolute_url_link", 'dimensions', 'image_file_size', "updated_on")
    list_filter = ("menu_list",)
    search_fields = ("name", "menu_list__name", "image")
    fields = ["name", "menu_list", "image_thumbnail", "image", "url", "link_health", "order"]
    readonly_fields = ["image_thumbnail", "link_health"]  # Ensure image_thumbnail is treated as a read-only field
    ordering = ["-updated_on"]
    list_per_page = 25

    def image_file_size(self, obj):
        img_mb = obj.image.size / 1048576
        too_big = img_mb > 1
        return format_html(f'<p style="color: {'red' if too_big == True else 'black'};">{round(img_mb, 3)}mb</p>')



    def dimensions(self, obj):
        """
        Method to display the dimensions of the image.

        Args:
            obj (LandingPageImage): The LandingPageImage instance.

        Returns:
            str: HTML string displaying the width and height of the image.
        """
        width, height = obj.image.width, obj.image.height
        return format_html("<p>{} x {}</p>", width, height)



    def image_thumbnail(self, obj):
        """
        Returns the HTML representation of the image thumbnail for a MenuListItem object.

        Parameters:
        obj (MenuListItem): The MenuListItem object.

        Returns:
        str: HTML string that represents the image thumbnail.
        """
        return format_html('<img src="{}" width="75" />', obj.image.url)

    def link_health(self, obj):
        """
        Checks the health of the URL of the MenuListItem object. A URL is considered healthy if it returns a 200 status.

        Parameters:
        obj (MenuListItem): The MenuListItem object.

        Returns:
        str: HTML string. A green light (HTML span element with green background) for healthy links and a red light (span element with red background) for unhealthy links.

        """
        absolute_url = obj.get_absolute_url()

        try:
            response = requests.get(absolute_url)
            healthy = response.status_code == 200
        except requests.exceptions.RequestException:
            healthy = False

        green_light = '<span style="display: inline-block; width: 20px; height: 20px; background-color: #00FF2C; border-radius: 50;"></span>'
        red_light = '<span style="display: inline-block; width: 20px; height: 20px; background-color: red; border-radius: 50;"></span>'

        return format_html(f"{green_light if healthy else red_light}")


# Registering models with inlines
admin.site.unregister(Product)
admin.site.register(Product, ProductAdmin)
admin.site.unregister(MenuList)
admin.site.register(MenuList, MenuListAdmin)
