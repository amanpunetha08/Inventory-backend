from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests


@api_view(['POST'])
@permission_classes([AllowAny])
def google_login(request):
    token = request.data.get('token')
    if not token:
        return Response({'error': 'Token required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.GOOGLE_CLIENT_ID)
        email = idinfo['email']
        name = idinfo.get('name', '')

        user, created = User.objects.get_or_create(
            username=email,
            defaults={'email': email, 'first_name': name}
        )

        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {'email': email, 'name': name}
        })
    except ValueError as e:
        return Response({'error': f'Invalid token: {str(e)}'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'error': f'Auth failed: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
