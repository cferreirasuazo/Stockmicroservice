from rest_framework.views import APIView
from rest_framework.response import Response
from stocks.stock_client import StooqClient

class StockView(APIView):
    """
    Receives stock requests from the API service.
    """
    def get(self, request, *args, **kwargs):
        stooq_client = StooqClient()
        stock_code = request.query_params.get('code')
        try:
            stock = stooq_client.get_stock(stock_code)
        except:
            error_message = {
                "message": "invalid stock code"
            }
            return Response(error_message,status=500)
        return Response(stock,status=200)
