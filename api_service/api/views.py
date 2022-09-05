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
from .models import UserRequestHistory
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import datetime
from django.db.models import Count
from .stock_client import StockClient


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
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        stock_code = request.query_params.get('q')
        stock_client = StockClient()
        user_id = self.request.user.id
        try:
            stock_client_response = stock_client.get(stock_code)
        except ValueError:
            return Response({"message": "Invalid Stock Code"}, status=406)
        except Exception:
            return Response({"message": "Something Failed Successfully"},status=500)

        stock_client_response["user_id"] = user_id

        stock = UserRequestHistory.objects.create(**stock_client_response)
        serializer = UserRequestHistorySerializer(stock)
        return Response(serializer.data, status=200)


class HistoryView(generics.ListAPIView):
    """
    Returns queries made by current user.
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserRequestHistorySerializer

    def get_queryset(self, *args, **kwargs):
        username = self.request.user.username
        queryset = UserRequestHistory.objects.filter(user__username=username)
        return queryset


class StatsView(APIView):
    """
    Allows super users to see which are the most queried stocks.
    """
    # TODO: Implement the query needed to get the top-5 stocks as described in the README, and return
    # the results to the user.
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            return Response({"message": "Not Valid User"}, status=403)
        stats = UserRequestHistory.objects.get_top_stocks(5)
        return Response(stats, status=200)
