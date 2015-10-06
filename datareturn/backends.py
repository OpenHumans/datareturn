from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model


class UserTokenBackend(object):

    def authenticate(self, username=None, token=None):
        """
        Authenticate a user based on their token.

        This system is using the built in token generator in django.contrib.auth
        which is typically used for password reset.
        """
        UserModel = get_user_model()
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
            if default_token_generator.check_token(user, token):
                return user
        except UserModel.DoesNotExist:
            pass
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
