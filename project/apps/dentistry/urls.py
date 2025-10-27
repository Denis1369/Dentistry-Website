from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ServiceView, FeedbackView, ProfessionView, WorkersView

router = DefaultRouter()
router.register(prefix='user', viewset=UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('services/', ServiceView.as_view(), name='services'),
    path('feedback/', FeedbackView.as_view(), name='feedback'),
    path('profession/', ProfessionView.as_view(), name='profession'),
    path('workers/', WorkersView.as_view(), name='workers'),
    ]