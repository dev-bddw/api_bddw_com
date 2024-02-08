from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    blurb = models.TextField()
    meta = models.JSONField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="")
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
