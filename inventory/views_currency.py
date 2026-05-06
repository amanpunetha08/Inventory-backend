import requests as http_requests
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

EXCHANGE_API = 'https://api.exchangerate-api.com/v4/latest/INR'


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def exchange_rates(request):
    try:
        res = http_requests.get(EXCHANGE_API, timeout=5)
        data = res.json()
        rates = data.get('rates', {})
        return Response({
            'base': 'INR',
            'rates': {
                'INR': 1,
                'USD': rates.get('USD', 0.012),
                'EUR': rates.get('EUR', 0.011),
            }
        })
    except Exception:
        return Response({
            'base': 'INR',
            'rates': {'INR': 1, 'USD': 0.012, 'EUR': 0.011}
        })
