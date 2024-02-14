from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords

import time
import boto3
from django.db.models.fields.files import ImageFieldFile


class CloudFrontImageFieldFile(ImageFieldFile):
    def create_invalidation(self):

        if settings.SETTINGS_MODULE == "config.settings.production":

            client = boto3.client(
                "cloudfront",
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name="us-east-1",  # Specify the appropriate region
            )

            distribution_id = "EWK3EMFHZGQ8"
            path = "/" + self.name
            response = client.create_invalidation(
                DistributionId=distribution_id,
                InvalidationBatch={"Paths": {"Quantity": 1, "Items": [path]}, "CallerReference": str(time.time())},
            )


class CloudFrontImageField(models.ImageField):
    attr_class = CloudFrontImageFieldFile


class Product(models.Model):
    name = models.CharField(max_length=255)
    blurb = models.TextField(null=True, blank=True)
    meta = models.JSONField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def slugify(self):
        return self.name.lower().replace(" ", "-")

    def get_absolute_url(self):

        return f"https://bddw.com/product/{self.slugify()}"

    def get_blurb_preview(self):
        return f"{self.blurb[0:100]}..."

    def image_number(self):
        return len(ProductImage.objects.filter(product__pk=self.id))


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = CloudFrontImageField(upload_to="")
    order = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    caption = models.CharField(null=True, blank=True, max_length=200)

    class Meta:
        ordering = ["order"]

    def save(self, *args, **kwargs):
        self.image.create_invalidation()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.image} - {self.product.name} - # {self.order}"


class MenuList(models.Model):
    name = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    meta = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name

    def slugify(self):
        return self.name.lower().replace(" ", "-")

    def get_absolute_url(self):

        return f"https://bddw.com/list/{self.slugify()}"

    def number_of_list_items(self):
        return len(MenuListItem.objects.filter(menu_list_id=self.id))


class MenuListItem(models.Model):
    name = models.CharField(max_length=255)
    menu_list = models.ForeignKey(MenuList, related_name="MenuListItems", on_delete=models.CASCADE)
    image = CloudFrontImageField(upload_to="")
    url = models.CharField(max_length=255)
    order = models.IntegerField()

    def save(self, *args, **kwargs):
        self.image.create_invalidation()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Menu List Item: {self.name}"

    class Meta:
        ordering = ["order"]


class DropDownMenu(models.Model):
    data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"BDDW.COM DROPDOWN MENU {self.id}"
