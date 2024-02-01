from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "api_bddw_com.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import api_bddw_com.users.signals  # noqa: F401
        except ImportError:
            pass
