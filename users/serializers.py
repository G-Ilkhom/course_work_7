from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Cериализатор для модели User"""

    class Meta:
        model = User
        fields = "__all__"


class UserRegisterSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя"""

    password2 = serializers.CharField()

    class Meta:
        model = User
        fields = ["email", "password", "password2", "telegram_id"]

    def save(self, *args, **kwargs):
        user = User(
            email=self.validated_data["email"],
            telegram_id=self.validated_data["telegram_id"],
            is_superuser=False,
            is_staff=False,
            is_active=True,
        )

        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]
        if password != password2:
            raise serializers.ValidationError({password: "Пароли не совпадают"})
        user.set_password(password)
        user.save()
        return user
