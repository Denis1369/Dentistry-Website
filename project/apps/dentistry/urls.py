from django.urls import path
from .views import LoginView, RegisterView, ServiceView, FeedbackView, ProfessionView, WorkersView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('services/', ServiceView.as_view(), name='services'),
    path('feedback/', FeedbackView.as_view(), name='feedback'),
    path('profession/', ProfessionView.as_view(), name='profession'),
    path('workers/', WorkersView.as_view(), name='workers'),
    ]