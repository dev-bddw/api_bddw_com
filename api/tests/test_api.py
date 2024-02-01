from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from api.models import Product, MenuList

from rest_framework.authtoken.models import Token
import tempfile
from PIL import Image

User = get_user_model()


class ProductMenuListTestCase(APITestCase):
    def setUp(self):
        # Set up data for testing
        self.client = APIClient()

        self.user = User.objects.create_user(email="testuser@bddw.com", password="12345")
        self.token = Token.objects.create(user=self.user)

        self.product = Product.objects.create(name="Test Product", blurb="Test Blurb")
        self.menulist = MenuList.objects.create(name="Test MenuList")
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_get_product(self):
        # Test retrieving a product
        response = self.client.get(
            reverse("api:api-endpoint", kwargs={"slug": self.product.name.lower().replace(" ", "-")})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.product.name)

    def test_get_menulist(self):
        # Test retrieving a menulist
        response = self.client.get(
            reverse("api:api-endpoint", kwargs={"slug": self.menulist.name.lower().replace(" ", "-")})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.menulist.name)

    def test_get_not_found(self):
        # Test retrieving a non-existent object
        response = self.client.get(reverse("api:api-endpoint", kwargs={"slug": "nonexistent"}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreatProductTestCase(APITestCase):
    def setUp(self):
        # Set up data for testing
        self.client = APIClient()

        self.user = User.objects.create_user(email="testuser@bddw.com", password="12345")
        self.token = Token.objects.create(user=self.user)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_create_product_with_images(self):
        url = reverse("api:create-product")  # Update with your actual URL name
        data = {
            "name": "Test Product",
            "blurb": "Test Blurb",
            "meta": "{}",
            "images": [
                {"image": self.create_image_file(), "order": 1},
                {"image": self.create_image_file(), "order": 2},
            ],
        }

        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.first().images.count(), 2)

    def create_image_file(self):
        from PIL import Image
        from io import BytesIO
        from django.core.files.base import File

        image = Image.new("RGB", (100, 100))
        tmp_file = BytesIO()
        image.save(tmp_file, "JPEG")
        tmp_file.seek(0)
        return File(tmp_file, name="test.jpg")
