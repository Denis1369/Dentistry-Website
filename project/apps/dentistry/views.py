import datetime
import os

from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from yaml import serialize

from .serializers.UserSerializers import LoginSerializer, RegisterSerializer, ProfileSerializer
from .serializers.FeedbackSerializers import LeaveFeedbackSerializer, GetFeedbackSerializer
from .serializers.ServiceSerializer import ServiceSerializer
from .serializers.ProfessionSerializer import ProfessionSerializer
from .serializers.WorkersSerializer import WorkersSerializer 
from .models import Services, Profession, Workers, CustomUser, Feedback
from rest_framework_simplejwt.tokens import AccessToken

from .utils.ObjectStorageUtil import upload_file_to_cloud

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
        description="Получить профиль текущего авторизованного пользователя",
        responses={200: ProfileSerializer}
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        user = CustomUser.objects.get(user_id=request.user.user_id)
        serializer = ProfileSerializer(user)

        return Response({
            "user": serializer.data
        })

    @extend_schema(
        summary="Загрузить аватар пользователя",
        description="Принимает изображение в формате multipart/form-data и сохраняет в облако.",
        request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'avatar': {
                        'type': 'string',
                        'format': 'binary',
                        'description': 'Файл изображения (jpg, png и т.д.)'
                    }
                },
                'required': ['avatar']
            }
        },
    )
    @action(detail=False, methods=['put'], parser_classes=[MultiPartParser], permission_classes=[IsAuthenticated])
    def update_avatar(self, request):
        file = request.FILES['avatar']

        if not file:
            return Response({'error': 'Файл не предоставлен'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_id = request.user.user_id
            file_name, file_extension = os.path.splitext(file.name)
            upload_file_to_cloud(file, f'{user_id}{file_extension}')

            request.user.user_img = f'https://dentistry.s3.cloud.ru/avatars/{user_id}{file_extension}'
            request.user.save()

            return Response({'message': 'Аватар успешно изменён'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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

class FeedbackViewSet(ViewSet):

    @extend_schema(
        request=LeaveFeedbackSerializer,
        responses={200: OpenApiResponse(description="Отзыв успешно оставлен", examples={"message": "Отзыв отправлен"})},
        description="Оставление отзыва по JWT токену"
    )
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def leave_feedback(self, request):
        serializer = LeaveFeedbackSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(feedback_user=request.user)
            return Response({"message": "Отзыв отправлен"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={200: OpenApiResponse(examples={"feedbacks": [
            {"feedback_rating":5, "feedback_text":"Очень круто", "feedback_date":datetime.datetime.now(), 'first_name':"Денис", 'last_name':"Ибрагимов"}
        ]
        }
        )},
        description="Получение отзывов"
    )
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def get_feedbacks(self, request):
        feedbacks = Feedback.objects.select_related('feedback_user')
        serializer = GetFeedbackSerializer(feedbacks, many=True)

        return Response({
            "feedbacks": serializer.data
        })
