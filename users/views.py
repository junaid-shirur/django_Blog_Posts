from rest_framework.views import APIView
from .serializer import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from datetime import datetime
from django.db import IntegrityError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            return Response({'access_token': access_token, 'refresh_token': refresh_token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
    

@api_view(['POST'])
def login(request):
    pass
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UserView(request):
   user = request.user 
   try:
        user_profile = user.userprofile  
        data = {
            'username': user.username,
            'email': user.email,
            'bio': user_profile.bio if hasattr(user, 'userprofile') else "",
            # Add other user-related fields here
        }
        return Response(data)
   except User.DoesNotExist:
        return Response({'error': 'User profile not found'}, status=404)
