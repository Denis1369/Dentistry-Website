from rest_framework import serializers
from ..models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'first_name', 'last_name', )
