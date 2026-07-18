from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from account.models import User


class CodeConfirmationSerializer(serializers.Serializer):
    code = serializers.IntegerField(required=True)
    password = serializers.CharField(required=True)


class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    confirmPassword = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    preferred_content = serializers.CharField(required=True)
    study_preference = serializers.CharField(required=False)
    previous_year_performance = serializers.CharField(required=False)
    current_year_level = serializers.CharField(required=True)

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 
            'email', 
            'first_name', 
            'last_name', 
            'phone_number', 
            'password', 
            'is_active',
            'is_admin',
            'current_year_level',
            'study_preference',
            'preferred_content',
            'previous_year_performance',
            'current_year_level',
            'role'
        ]

    def get_role(self,obj:User):

        if obj.is_admin:
            return 'admin'
        
        return 'user'

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.is_verify = True
            user.save()
        return user
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class Login2FAOTPSerializer(serializers.Serializer):
    code = serializers.CharField(required=True)




class CheckEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    country = serializers.CharField(required=False)



class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise ValidationError("New passwords do not match.")
        return data


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
