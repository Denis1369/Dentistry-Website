from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers.LoginSerializer import LoginSerializer
from .serializers.RegisterSerializer import RegisterSerializer
from .serializers.ServiceSerializer import ServiceSerializer
from .serializers.FeedbackSerializer import FeedbackSerializer
from .models import Services
from rest_framework_simplejwt.tokens import AccessToken


class LoginView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            token = AccessToken.for_user(user)

            return Response({
                'token': str(token),
            }, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "message": "Регистрация прошла успешно"
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ServiceView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ServiceSerializer

    def get(self, request):
        services = Services.objects.all()
        serializer = self.get_serializer(services, many=True)

        return Response({
            "services": serializer.data
        })

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "message": "Услуга создана"
            })

        return Response({
            "error": serializer.errors
        })
    
class FeedbackView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FeedbackSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save(feedback_user=request.user)
            return Response({"message": "Отзыв отправлен"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)