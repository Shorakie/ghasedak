import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from ghasedak.accounts.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture()
def active_user(db, user_factory):
    return user_factory.create(is_active=True)


@pytest.fixture
def inactive_user(db, user_factory):
    return user_factory.create(is_active=False)


@pytest.fixture
def authenticate_user(api_client, active_user: User, auth_user_otp):
    """Create a user and return token needed for authentication"""

    def _user(verified=True, is_active=True, is_admin=False):
        active_user.verified = verified
        active_user.is_active = is_active
        active_user.is_admin = is_admin
        active_user.save()
        active_user.refresh_from_db()
        url = reverse("auth:login")
        data = {
            "phone": active_user.phone,
            "otp": auth_user_otp,
        }
        response = api_client.post(url, data)
        token = response.json()["access"]
        return {
            "token": token,
            "user_username": active_user.username,
            "user_instance": active_user,
        }

    return _user
