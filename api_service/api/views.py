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
        date_format = '%Y-%m-%d %H:%M:%S'
        user_id = self.request.user.id
        stock_client_response = {
            "symbol": "ra.us",
            "date": "2022-09-02",
            "time": "15:45:01",
            "open": "9.94",
            "high": "9.94",
            "low": "9.94",
            "close": "9.94",
            "volume": "155",
            "name": "RAUL"
        }
        datetime_str = stock_client_response.get("date") + " " + stock_client_response.get("time")
        dt_object = datetime.datetime.strptime(datetime_str, date_format)
        data = {
            "symbol": stock_client_response.get("symbol"),
            "date":   dt_object,
            "open":   stock_client_response.get("open"),
            "high":   stock_client_response.get("high"),
            "low":    stock_client_response.get("low"),
            "close":  stock_client_response.get("close"),
            "name":   stock_client_response.get("name"),
            "user_id" : user_id
        }
        
        stock_code = request.query_params.get('q')
        stock = UserRequestHistory.objects.create(**data)
        serializer = UserRequestHistorySerializer(stock)
        return Response(serializer.data,status=200)


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
        counts = UserRequestHistory.objects.values('symbol').annotate(requested = Count('symbol')).order_by('-requested')
        stats = [ 
            { 
                "stock": count["symbol"], 
                "times_requested": count["requested"] 
            } for count in counts[:5] ]
        
        if not self.request.user.is_staff:
            return Response(stats, status=406)

        return Response(stats,status=200)