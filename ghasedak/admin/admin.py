from django.contrib import admin

from ghasedak.admin.forms import AdminAuthenticationForm


class AdminSite(admin.AdminSite):
    login_form = AdminAuthenticationForm
    login_template = 'admin/login.html'
