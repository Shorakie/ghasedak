from django.contrib.admin import apps


class AdminConfig(apps.AdminConfig):
    default = True
    default_site = 'ghasedak.admin.AdminSite'
