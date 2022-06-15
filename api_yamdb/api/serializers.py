from reviews.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



# class TokenSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)

#         token['username'] = user.name
#         token['confirmation_code'] = user.confirmation_code

#         return