import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from api.models import MenuList, Product


@pytest.mark.django_db
class TestSingularPluralFallback:
    def setup_method(self):
        self.client = APIClient()

    @pytest.fixture(autouse=True)
    def _authenticate(self, db):
        user = get_user_model().objects.create_user(email="tester@example.com", password="password")
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def _get(self, slug):
        return self.client.get(reverse("api:api-endpoint", kwargs={"slug": slug}))

    def test_singular_slug_matches_plural_menu_list(self):
        MenuList.objects.create(name="Vases")

        response = self._get("vase")

        assert response.status_code == 200
        assert response.data["body"]["name"] == "Vases"

    def test_plural_slug_matches_singular_product(self):
        Product.objects.create(name="Ceramic Crock")

        response = self._get("ceramic-crocks")

        assert response.status_code == 200
        assert response.data["body"]["name"] == "Ceramic Crock"

    def test_exact_match_still_takes_precedence_over_fallback(self):
        Product.objects.create(name="Vase")
        MenuList.objects.create(name="Vases")

        response = self._get("vase")

        assert response.status_code == 200
        assert response.data["body"]["name"] == "Vase"

    def test_no_match_still_404s(self):
        response = self._get("nonexistent-thing")

        assert response.status_code == 404
