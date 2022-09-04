# encoding: utf-8

from django.contrib import admin
from django.urls import path

from api import views as api_views

urlpatterns = [
    path('stock', api_views.StockView.as_view(), name="stock"),
    path('history', api_views.HistoryView.as_view(), name="history"),
    path('stats', api_views.StatsView.as_view(), name="stats"),
    path('admin', admin.site.urls),
    path("signup", api_views.UserSignInAPIView.as_view(), name="signup-user"),
    path('signin', api_views.UserSignupAPIView.as_view(), name="signin-user")
]
