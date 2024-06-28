from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response

from habits.permissions import IsOwner
from users.models import User
from users.serializers import UserSerializer, UserRegisterSerializer


class UserListAPIView(generics.ListAPIView):
    """ Вывод списка пользователей """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """ Вывод одного пользователя """

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(generics.UpdateAPIView):
    """ Редактирование пользователя """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class UserDestroyAPIView(generics.DestroyAPIView):
    """ Удаление пользователя """

    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class UsersRegistrationView(generics.CreateAPIView):
    """ Регистрация нового пользователя """

    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = True
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data)
