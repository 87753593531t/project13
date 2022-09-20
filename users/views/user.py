from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response


from users.models import CustomUser
from users.serializers import UserCreateSerializer, UserSerializer, UserUpdateSerializer


class UserViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()


    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(CustomUser.objects.all(), many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


    def put(self, request, *args, **kwargs):
        uuid = request.query_params.put('uuid', False)
        uuid = CustomUser.objects.filter(pk=uuid).first()
        serializer = UserUpdateSerializer(data=request.data, context={'uuid': uuid.user_uuid})
        serializer.is_valid(raise_exception=True)
        serializer.update(uuid, serializer.data)
        return Response(data=serializer.data, status=status.HTTP_200_OK)