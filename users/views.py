from rest_framework.views import APIView
from .serializer import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from datetime import datetime
import jwt

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)
    


class LoginView(APIView):
    def post(self,request):
        email = request.data["email"]
        password = request.data["password"]

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("User not found")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")
        

        payload = {
            "id": user.id,
            "exp": datetime.utcnow() + datetime.timedelta(minute=60),
            "iat": datetime.utcnow()
        }
        token = jwt.encode(payload,"secret", algorithm="HS256").decode("utf-8")

        res = Response()
        res.data = {
            token
        }
        return res
    


class UserView(APIView):
    def get(self,request):
        pass
