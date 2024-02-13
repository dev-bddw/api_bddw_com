from django.db import models
from django.conf import settings
import time
import boto3

class CloudFrontImageField(models.ImageField):
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if settings.DJANGO_SETTINGS_MODULE == 'config.settings.production':
            # Invalidate CloudFront cache here
            # Note: Ensure you implement error handling and consider performance implications
            client = boto3.client('cloudfront')
            distribution_id = settings.CLOUDFLARE_DISTRIBUTION_ID
            path = self.name  # Dynamically construct the path based on your application's logic
            client.create_invalidation(
                DistributionId=distribution_id,
                InvalidationBatch={
                    'Paths': {'Quantity': 1, 'Items': [path]},
                    'CallerReference': str(time.time())
                }
            )

class Product(models.Model):
    name = models.CharField(max_length=255)
    blurb = models.TextField()
    meta = models.JSONField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = CloudFrontImageField(upload_to="")
    order = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    caption = models.CharField(max_length=200)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Image for {self.product.name} - # {self.order}"


class MenuList(models.Model):
    name = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    meta = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name


class MenuListItem(models.Model):
    name = models.CharField(max_length=255)
    menu_list = models.ForeignKey(MenuList, related_name="MenuListItems", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="")
    url = models.CharField(max_length=255)
    order = models.IntegerField()

    class Meta:
        ordering = ["order"]


class DropDownMenu(models.Model):
    data = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"BDDW.COM DROPDOWN MENU #{self.id}"
