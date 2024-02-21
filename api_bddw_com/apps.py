from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "api_bddw_com"  # Replace 'your_app_name' with the name of your app

    def ready(self):
        # Import admin module and set the site_header
        from django.contrib import admin

        admin.site.site_header = "BDDW.COM API"
