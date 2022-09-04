# encoding: utf-8

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from api.models import UserRequestHistory
from api.serializers import UserRequestHistorySerializer
from django.contrib.auth.models import User
from .serializers import SignUpSerializer, UserSerializer, SignInSerializer
from .auth.token_manager import TokenManager

class UserSignupAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignInSerializer
    permission_classes = [AllowAny]

class UserSignInAPIView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        """ POST handler. """
        serializer = self.get_serializer(
            data=request.data)  # type: SignUpSerializer

        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            user = User.objects.get(email=email)
            user_data = UserSerializer(user).data  # type: dict

            # Generating token
            user_data['token'] = TokenManager.create_token(user)

            return Response(user_data)

class StockView(APIView):
    """
    Endpoint to allow users to query stocks
    """

    def get(self, request, *args, **kwargs):
        stock_code = request.query_params.get('q')
        # TODO: Call the stock service, save the response, and return the response to the user
        return Response()


class HistoryView(generics.ListAPIView):
    """
    Returns queries made by current user.
    """
    queryset = UserRequestHistory.objects.all()
    serializer_class = UserRequestHistorySerializer
    # TODO: Filter the queryset so that we get the records for the user making the request.


class StatsView(APIView):
    """
    Allows super users to see which are the most queried stocks.
    """
    # TODO: Implement the query needed to get the top-5 stocks as described in the README, and return
    # the results to the user.

    def get(self, request, *args, **kwargs):
        return Response()
