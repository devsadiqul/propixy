from django.contrib.auth.backends import ModelBackend
from core.models import User


class EmailOrPhoneBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = None

        try:
            if username:
                if '@' in username:
                    user = User.objects.get(email=username)
                elif username.lstrip('+').isdigit():
                    user = User.objects.get(phone=username)
        except User.DoesNotExist:
            return None

        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None