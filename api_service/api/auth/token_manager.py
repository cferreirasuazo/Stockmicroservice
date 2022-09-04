from rest_framework.authtoken.models import Token


class TokenManager():
    @classmethod
    def create_token(self, user):
        token = Token.objects.get_or_create(user=user)
        return token[0].key

    @classmethod
    def delete_token(user_email):
        try:
            token = Token.objects.get(user__email=user_email)
            token.delete()
        except Token.DoesNotExist:
            pass