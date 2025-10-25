from rest_framework import serializers
from ..models import Feedback

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['feedback_date', 'feedback_text', 'feedback_rating']