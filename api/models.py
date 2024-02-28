import os
import time
from io import BytesIO

import boto3
from django.conf import settings
from django.core.files.base import ContentFile
from django.db import models
from django.db.models.fields.files import ImageFieldFile
from django.utils.deconstruct import deconstructible
from PIL import Image
from django.utils.html import format_html

@deconstructible
class LowercaseRename(object):
    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):  # type: ignore
        # Lowercase the entire filename including the extension
        filename = filename.lower()
        # Return the new path with the lowercased filename
        return os.path.join(self.path, filename)


class CloudFrontImageFieldFile(ImageFieldFile):
    def create_invalidation(self):

        if settings.SETTINGS_MODULE in ["config.settings.production", 'config.settings.staging']:

            client = boto3.client(
                "cloudfront",
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name="us-east-1",  # Specify the appropriate region
            )

            distribution_id = settings.CLOUDFLARE_DISTRIBUTION_ID
            path = "/" + self.name
            client.create_invalidation(
                DistributionId=distribution_id,
                InvalidationBatch={"Paths": {"Quantity": 1, "Items": [path]}, "CallerReference": str(time.time())},
            )


class CloudFrontImageField(models.ImageField):
    attr_class = CloudFrontImageFieldFile


class Product(models.Model):
    name = models.CharField(help_text="The name you want to appear in the template", max_length=255)
    blurb = models.TextField(help_text="The blurb text that appears underneath the carousel", null=True, blank=True)
    meta = models.JSONField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def slugify(self):
        return self.name.lower().replace(" ", "-")

    def get_absolute_url(self):

        return f"https://bddw.com/product/{self.slugify()}"

    def get_absolute_url_link(self):
        link = f'https://bddw.com/product/{self.slugify()}'
        return format_html(f'<a href="{link}">{link}</a>')

    def get_blurb_preview(self):
        return f"{self.blurb[0:100]}..."

    def image_number(self):
        return len(ProductImage.objects.filter(product__pk=self.id))


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, help_text="image for what product?", related_name="images", on_delete=models.CASCADE
    )
    image = CloudFrontImageField(help_text="upload your image here", upload_to=LowercaseRename(""))
    thumbnail = CloudFrontImageField(
        default=None, blank=True, null=True, help_text="thumbnail of image", upload_to=LowercaseRename("")
    )
    order = models.IntegerField(help_text="the order the image should appear in the carousel")
    created_on = models.DateTimeField(auto_now_add=True)
    caption = models.CharField(help_text="image caption", null=True, blank=True, max_length=200)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order"]

    def save(self, *args, **kwargs):
        self.image.create_invalidation()
        img = Image.open(self.image)
        img.thumbnail((300, 300))
        thumb_io = BytesIO()
        img.save(thumb_io, img.format, quality=85)

        file_name = self.image.name
        root, ext = os.path.splitext(file_name)
        file_name = f"{root}-thumb{ext}"
        thumb_file = ContentFile(thumb_io.getvalue(), file_name)

        self.thumbnail.save(file_name, thumb_file, save=False)
        super().save(*args, **kwargs)  # Save the instance only once, after the thumbnail is created

    def __str__(self):
        return f"{self.image} - {self.product.name} - # {self.order}"


class LandingPageImage(models.Model):
    image = CloudFrontImageField(help_text="upload your image here", upload_to=LowercaseRename(""))  # type: ignore
    thumbnail = (
        CloudFrontImageField(default=None, blank=True, null=True, help_text="thumbnail of image", upload_to=LowercaseRename(""))
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_on"]

    def save(self, *args, **kwargs):
        self.image.create_invalidation()
        img = Image.open(self.image)
        img.thumbnail((300, 300))
        thumb_io = BytesIO()
        img.save(thumb_io, img.format, quality=85)

        file_name = self.image.name
        root, ext = os.path.splitext(file_name)
        file_name = f"{root}-thumb{ext}"
        thumb_file = ContentFile(thumb_io.getvalue(), file_name)

        self.thumbnail.save(file_name, thumb_file, save=False)
        super().save(*args, **kwargs)  # Save the instance only once, after the thumbnail is created

    def __str__(self):
        return f"{self.image}"


class MenuList(models.Model):
    name = models.CharField(help_text="name appears at the top of the menu template", max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    meta = models.JSONField(null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def slugify(self):
        return self.name.lower().replace(" ", "-")

    def get_absolute_url(self):

        return f"https://bddw.com/list/{self.slugify()}"

    def get_absolute_url_link(self):
        link = f'https://bddw.com/list/{self.slugify()}'
        return format_html(f'<a href="{link}">{link}</a>')

    def number_of_list_items(self):
        return len(MenuListItem.objects.filter(menu_list_id=self.id))


class MenuListItem(models.Model):
    name = models.CharField(help_text="name of the menu item", max_length=255)
    menu_list = models.ForeignKey(
        MenuList,
        help_text="menu list where this item appears",
        related_name="MenuListItems",
        on_delete=models.CASCADE,
    )
    image = CloudFrontImageField(
        help_text="'thumbnail' image you want for this menu item", upload_to=LowercaseRename("")
    )
    url = models.CharField(help_text="path for linking: /list/list-name or /product/product-name", max_length=255)
    order = models.IntegerField(help_text="order item to appear")
    updated_on = models.DateTimeField(auto_now=True)


    def get_absolute_url(self):
        return 'https://bddw.com' + f'{self.url}'

    def get_absolute_url_link(self):
        link = 'https://bddw.com' + f'{self.url}'
        return format_html(f'<a href="{link}">{link}</a>')

    def save(self, *args, **kwargs):
        self.image.create_invalidation()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Menu List Item: {self.name}"

    class Meta:
        ordering = ["order"]


class DropDownMenu(models.Model):
    data = models.JSONField(null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"BDDW.COM DROPDOWN MENU {self.id}"
