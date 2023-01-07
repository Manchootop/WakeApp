from django.contrib.auth import get_user_model
from rest_framework import serializers

UserModel = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('email', 'password')

    def create(self, validated_data):
        # Fix issue with password in plain text
        user = super().create(validated_data)

        user.set_password(validated_data['password'])
        user.save()

        return user

    # Remove password from response
    def to_representation(self, instance):
        result = super().to_representation(instance)
        result.pop('password')
        return result
