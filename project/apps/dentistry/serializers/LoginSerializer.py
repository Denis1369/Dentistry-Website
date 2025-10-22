from rest_framework import serializers
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    user_email = serializers.EmailField(required=True)
    user_password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        email = data.get('user_email')
        password = data.get('user_password')

        if not email or not password:
            raise serializers.ValidationError("Email и пароль обязательны.")

        user = authenticate(username=email, password=password)
        if not user:
            raise  serializers.ValidationError("Неверный email или пароль")

        data['user'] = user
        return data
