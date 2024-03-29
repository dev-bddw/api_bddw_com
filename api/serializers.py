from rest_framework import serializers

from .models import DropDownMenu, LandingPageImage, MenuList, MenuListItem, Product, ProductImage


class DropDownMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = DropDownMenu
        fields = "__all__"


class ImageNameField(serializers.ImageField):
    def to_representation(self, value):
        return value.name if value else None


class LandingPageImageSerializer(serializers.ModelSerializer):
    image = ImageNameField()
    thumbnail = ImageNameField()

    class Meta:
        model = LandingPageImage
        fields = ["image", "thumbnail"]


class ProductImageSerializer(serializers.ModelSerializer):

    image = ImageNameField()
    thumbnail = ImageNameField()

    class Meta:
        model = ProductImage
        fields = ['id', "image", "thumbnail", "order", "caption"]


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=False)

    class Meta:
        model = Product
        fields = ['id', "name", "blurb", "meta", "images"]

    def create(self, validated_data):

        images_data = validated_data.pop("images")

        product = Product.objects.create(**validated_data)

        for image_data in images_data:
            ProductImage.objects.create(product=product, **image_data)

        return product

    def update(self, instance, validated_data):
        images_data = validated_data.pop("images", None)
        instance = super().update(instance, validated_data)

        if images_data is not None:
            instance.images.all().delete()
            for image_data in images_data:
                ProductImage.objects.create(product=instance, **image_data)

        return instance


class MenuListItemSerializer(serializers.ModelSerializer):
    image = ImageNameField()  # Assuming ImageNameField is a custom field you've defined

    class Meta:
        model = MenuListItem
        fields = ['id', "name", "image", "url", "order"]


class MenuListSerializer(serializers.ModelSerializer):
    records = MenuListItemSerializer(many=True, read_only=False, source="MenuListItems")

    class Meta:
        model = MenuList
        fields = ['id', "name", "meta", "records"]

    def create(self, validated_data):
        print("Validated data:", validated_data)
        records_data = validated_data.pop("MenuListItems")
        menu_list = MenuList.objects.create(**validated_data)
        for record_data in records_data:
            MenuListItem.objects.create(menu_list=menu_list, **record_data)
        return menu_list

    def update(self, instance, validated_data):
        records_data = validated_data.pop("records", None)
        instance.name = validated_data.get("name", instance.name)
        instance.save()

        if records_data is not None:
            # Clear existing records and create new ones
            instance.MenuListItems.all().delete()
            for record_data in records_data:
                MenuListItem.objects.create(menu_list=instance, **record_data)

        return instance
