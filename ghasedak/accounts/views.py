from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet


class AuthViewSet(GenericViewSet):
    """Auth view set"""

    @action(methods=['GET'], detail=False)
    def otp(self, request, *args, **kwargs):
        pass
