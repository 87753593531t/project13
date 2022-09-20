from rest_framework import serializers

from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'uuid',
            'phone',
            'first_name',
            'last_name',
            'is_staff',
            'is_active',
        )


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'uuid',
            'phone',
            'first_name',
            'last_name',
            'is_staff',
            'is_active',

        )

    def create(self, validated_data):
        users = validated_data['user']
        new_user_data = {}
        new_user_data['first_name'] = users['first_name']
        new_user_data['last_name'] = users['last_name']
        if new_user_data:
            new_user = UserCreateSerializer(data=new_user_data)
            new_user.is_valid(raise_exception=True)
            new_user.save()
            validated_data['user'] = new_user.instance
        return super().create(validated_data)


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'uuid',
            'phone',
            'first_name',
            'last_name',
            'is_staff',
            'is_active',

        )

    def update(self, instance, validated_data):
        if 'user' in validated_data.keys():
            user = CustomUser.objects.filter(id=instance.user_uuid).first()
            user_serializer = UserCreateSerializer(user)
            user_serializer.update(user, dict(validated_data['user']))
            del validated_data['user']
        return super().update(instance, validated_data)