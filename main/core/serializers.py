from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(serializers.ModelSerializer):
    """Сериализация при регистрации с валидацией."""
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Поля пароля не совпадают."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.email
        return token


# class UserSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = UserProfile
#         fields = ('first_name', 'last_name', 'phone_number', 'age', 'gender')
# class UserRegistrationSerializer(serializers.ModelSerializer):
#
#     # profile = UserSerializer(required=False)
#
#     class Meta:
#         model = User
#         fields = ('email', 'password', 'profile')
#         extra_kwargs = {'password': {'write_only': True}}
#
#     def create(self, validated_data):
#         # !TODO: Заменить на Activities Profile
#         # profile_data = validated_data.pop('profile')
#         user = User.objects.create_user(**validated_data)
#         # UserProfile.objects.create(
#         #     user=user,
#         #     first_name=profile_data['first_name'],
#         #     last_name=profile_data['last_name'],
#         #     phone_number=profile_data['phone_number'],
#         #     age=profile_data['age'],
#         #     gender=profile_data['gender']
#         # )
#         return user
