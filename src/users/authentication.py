from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User

class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print(f'Authenticating\nemail: {username}\npass: {password}')
        UserModel = get_user_model()
        print(type(UserModel))
        try:
            print(UserModel.objects.all())
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            print('User does not exist')
            return None
        else:
            if user.check_password(password):
                return user
            print('Invalid pass')
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None