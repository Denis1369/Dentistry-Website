from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers.LoginSerializer import LoginSerializer
from .serializers.RegisterSerializer import RegisterSerializer
from .serializers.ServiceSerializer import ServiceSerializer
from .serializers.FeedbackSerializer import FeedbackSerializer
from .serializers.ProfessionSerializer import ProfessionSerializer
from .serializers.UserProfileSerializer import ProfileSerializer
from .serializers.WorkersSerializer import WorkersSerializer 
from .models import Services, Profession, Workers, CustomUser
from rest_framework_simplejwt.tokens import AccessToken


class UserViewSet(ViewSet):

    @extend_schema(
        request=LoginSerializer,
        responses={200: OpenApiResponse(description="Успешная аутентификация", examples={"token": "abc123..."})},
        description="Авторизация пользователя по email и паролю"
    )
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']

            token = AccessToken.for_user(user)

            return Response({
                'token': str(token),
            }, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=RegisterSerializer,
        responses={200: OpenApiResponse(description="Успешная регистрация")},
        description="Регистрация нового пользователя"
    )
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "message": "Регистрация прошла успешно"
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={200: ProfileSerializer},
        description="Получить профиль текущего авторизованного пользователя"
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        user = CustomUser.objects.get(user_id=request.user.user_id)
        serializer = ProfileSerializer(user)

        return Response({
            "user": serializer.data
        })


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
    
class ProfessionView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProfessionSerializer

    def get(self, request):
        profession = Profession.objects.all()
        serializer = self.get_serializer(profession, many=True)

        return Response({
            "profession": serializer.data
        })
    
class WorkersView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = WorkersSerializer

    def get(self, request):
        workers = Workers.objects.all()
        serializer = self.get_serializer(workers, many=True)

        return Response({
            "workers": serializer.data
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