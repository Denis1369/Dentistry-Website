from datetime import datetime, time, timedelta
from django.utils import timezone
import os

from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiTypes
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from yaml import serialize

from .serializers.UserSerializers import LoginSerializer, RegisterSerializer, ProfileSerializer, UpdateProfileSerializer
from .serializers.FeedbackSerializers import LeaveFeedbackSerializer, GetFeedbackSerializer
from .serializers.ServiceSerializer import ServiceSerializer
from .serializers.ProfessionSerializer import ProfessionSerializer
from .serializers.WorkersSerializer import WorkersSerializer 
from .serializers.MedicalCardSerializer import MedicalCardSerializer
from .serializers.AppointmentSerializer import AppointmentSerializer
from .models import Services, Profession, Workers, CustomUser, Feedback, MedicalCard, Appointment
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

    @extend_schema(
        summary="Изменить данные пользователя",
        description="Изменяет введённые данные текущего авторизованного пользователя",
        request=UpdateProfileSerializer,
        responses={"message": OpenApiResponse(description="Изменения успешно сохранены")}
    )
    @action(detail=False, methods=['patch'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        serializer = UpdateProfileSerializer(
            instance=request.user,
            data=request.data,
            partial=True  # частичное обновление
        )

        if serializer.is_valid():
            serializer.save()

            return Response({
                "message": "Изменения успешно сохранены"
            }, status=status.HTTP_200_OK)

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
            {"feedback_rating":5, "feedback_text":"Очень круто", "feedback_date":datetime.now(), 'first_name':"Денис", 'last_name':"Ибрагимов"}
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

class MedicalCardView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MedicalCardSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='user_id',
                description='ID пользователя, чью медицинскую карту нужно получить',
                required=True,
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
            )
        ]
    )

    def get(self, request):
        user_id = request.query_params.get('user_id')

        if user_id is None:
            return Response({
                "error": "Параметр 'user_id' обязателен"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user_id = int(user_id)

        except ValueError:
            return Response({
                "error": "Параметр 'user_id' должен быть числом"},
                status=status.HTTP_400_BAD_REQUEST
            )

        medicalCard = MedicalCard.objects.filter(medical_card_user = user_id)
        serializer = self.get_serializer(medicalCard, many=True)

        return Response({
            "medicalCard": serializer.data
        })
    
class AppointmentSet(ViewSet):

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='worker_id',
                description='ID врача',
                required=True,
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY
            ),
            OpenApiParameter(
                name='date',
                description='Дата в формате YYYY-MM-DD',
                required=True,
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY
            )
        ],
        responses={
            200: {
                "type": "object",
                "properties": {
                    "slots": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "start": {"type": "string", "format": "date-time"},
                                "end": {"type": "string", "format": "date-time"}
                            }
                        }
                    }
                }
            },
            400: "Bad Request"
        }
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def get_appointment(self, request):
        worker_id = request.query_params.get('worker_id')
        date_str = request.query_params.get('date')

        if not worker_id or not date_str:
            return Response(
                {"error": "Параметры 'worker_id' и 'date' обязательны"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            worker = Workers.objects.get(workers_id=int(worker_id))
        except (ValueError, Workers.DoesNotExist):
            return Response(
                {"error": "Врач не найден"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {"error": "Неверный формат даты. Используйте YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Получаем длительность приёма из профессии
        profession = worker.workers_profession
        if not profession or not profession.profession_time:
            return Response(
                {"error": "Для этого врача не указана длительность приёма"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Рабочее время клиники: 7:00–21:00
        work_start = datetime.combine(target_date, time(7, 0))
        work_end = datetime.combine(target_date, time(21, 0))

        # Все записи врача на эту дату
        appointments = Appointment.objects.filter(
            appointment_workers=worker,
            appointment_date__date=target_date,
            appointment_status__in=['confirmed', 'pending', 'string']
        ).order_by('appointment_date')

        slot_minutes = int(profession.profession_time)

        occupied = set()
        for appt in appointments:
            appt_dn = timezone.make_naive(appt.appointment_date)
            appt_dn = appt_dn.replace(second=0, microsecond=0)
            occupied.add(appt_dn)

        free_slots = []

        current = work_start
        while current < work_end:
            slot_start = current.replace(second=0, microsecond=0)
            if slot_start not in occupied:
                free_slots.append(slot_start)
            current += timedelta(minutes=slot_minutes)

        return Response({"slots": free_slots})
    
    @extend_schema(
            request=AppointmentSerializer,
            responses={200: OpenApiResponse(description="Запись успешно оставлена", examples={"message": "Запись отправлена"})},
            description="Запись по JWT токену"
    )
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def post_appointment(self, request):
        serializer = AppointmentSerializer(data=request.data)

        if serializer.is_valid():
            try:
                worker = serializer.validated_data['appointment_workers']
                service = serializer.validated_data['appointment_services']
                start_time = serializer.validated_data['appointment_date']

                # Получаем длительность
                duration = service.services_profession.profession_time
                if not duration:
                    return Response(
                        {"error": "Длительность приёма не указана."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Повторная проверка доступности (на случай гонки)
                if not is_slot_available(worker, start_time, duration):
                    return Response(
                        {"error": "Время уже занято. Обновите список свободных слотов."},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Сохраняем
                appointment = serializer.save(
                    appointment_user=request.user,
                )

                return Response(
                    {"message": "Запись успешно создана", "appointment_id": appointment.appointment_id},
                    status=status.HTTP_201_CREATED
                )

            except Exception as e:
                return Response(
                    {"error": "Ошибка при создании записи: " + str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def is_slot_available(worker, start_time, duration_minutes):
    """
    Проверяет, свободен ли слот для врача.
    Использует JOIN, чтобы получить profession_time из связанной профессии.
    """
    from datetime import timedelta
    start_time = start_time.replace(second=0, microsecond=0)
    
    end_time = start_time + timedelta(minutes=duration_minutes)

    overlapping = Appointment.objects.filter(
        appointment_workers=worker,
        appointment_status__in=['confirmed', 'pending']
    ).select_related(
        'appointment_services__services_profession'
    ).extra(
        where=[
            """
            (%s < DATE_ADD(appointment_date, INTERVAL COALESCE(
                (SELECT profession_time FROM profession 
                 WHERE profession.profession_id = (
                     SELECT services_profession_id FROM services 
                     WHERE services.services_id = appointment.appointment_services_id
                 )
                ), %s
            ) MINUTE))
            AND
            (%s > appointment_date)
            """
        ],
        params=[end_time, duration_minutes, start_time]
    ).exists()

    return not overlapping
