from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import RegexValidator
from .models import CustomUser, Content

password_validator = RegexValidator(
    regex='^(?=.*[a-z])(?=.*[A-Z]).{8,}$',
    message='Password must be at least 8 characters long and contain at least one uppercase letter and one lowercase letter.'
)

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True,validators=[password_validator])
    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        refresh = RefreshToken.for_user(obj)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'full_name', 'phone', 'address', 'city', 'state', 'country', 'pincode', 'token']

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            phone=validated_data['phone'],
            address=validated_data['address'],
            city=validated_data['city'],
            state=validated_data['state'],
            country=validated_data['country'],
            pincode=validated_data['pincode']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ['id','title', 'body', 'summary', 'document', 'author']

    def validate(self, attrs):
        if attrs['author'] != self.context['request'].user:
            raise serializers.ValidationError("You can only create content for yourself!")
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['email'] = self.user.email
        data['full_name'] = self.user.full_name
        return data
