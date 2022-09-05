# enconding: utf-8

from urllib import request
from django.conf import settings
from django.db import models
from django.db.models import Count


class UserRequestHistoryManager(models.Manager):
    def format_stats(self, stocks, amount):
        stats = [
            {
                "stock": count["symbol"],
                "times_requested": count["requested"]
            } for count in stocks[:amount]]

        return stats

    def get_top_stocks(self, amount):
        requests = UserRequestHistory.objects.values('symbol').annotate(
            requested=Count('symbol')).order_by('-requested')
        stats = self.format_stats(requests, amount)
        return stats


class UserRequestHistory(models.Model):
    """
    Model to store the requests done by each user.
    """
    date = models.DateTimeField()
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=20)
    open = models.DecimalField(max_digits=10, decimal_places=2)
    high = models.DecimalField(max_digits=10, decimal_places=2)
    low = models.DecimalField(max_digits=10, decimal_places=2)
    close = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    objects = UserRequestHistoryManager()
