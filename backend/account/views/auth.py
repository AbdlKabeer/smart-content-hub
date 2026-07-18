import json
import requests
import re
from urllib.parse import unquote, urlencode, quote
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework import generics, response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from account.models import  User
from account.serializers.auth import CodeConfirmationSerializer, Login2FAOTPSerializer, LoginSerializer, PasswordResetConfirmSerializer, PasswordResetRequestSerializer, UserRegisterSerializer, UserSerializer
from helper.utils.response.response_format import internal_server_error_response, success_response , bad_request_response
from helper.utils.tokens import TokenManager




def generate_tokens_for_user(user):
    """
    Generate access and refresh tokens for the given user
    """
    serializer = TokenObtainPairSerializer()
    token_data = serializer.get_token(user)
    access_token = token_data.access_token
    refresh_token = token_data
    return access_token, refresh_token




class LoginTokenObtainPairView(generics.GenericAPIView):
    serializer_class = LoginSerializer
  
    def post(self, request ):
        
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email'] 
        password = serializer.validated_data['password']
        try: 
            user = authenticate(username=email , password=password)

            if user is not None :
                if user.is_active:

                    valid_user = User.objects.get(pk=user.id)
                    tokens = TokenManager.get_tokens_for_user(user)
                    response = {
                        "tokens" : tokens , 
                        'user' : UserSerializer(valid_user).data 
                    }
                    return success_response(data=response)
                else:
                    return bad_request_response(message="Your account is disabled, kindly contact the administrative", status_code=401)
                
            return bad_request_response(message='Invalid login credentials')
        except Exception as e:
            print(e)
            return internal_server_error_response()



class Confirm2FAOTPView(generics.GenericAPIView):
    serializer_class = Login2FAOTPSerializer
  
    def post(self, request ):
        
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data['code'] 

        otp_object = CodeConfirmation.objects.filter(
            code=code,
            confirmation_type='login',
            is_active=True
        ).first()

        if not otp_object:
            return bad_request_response(message="Invalid code")

        try: 
            user = otp_object.user
            valid_user = User.objects.get(pk=user.id)
            tokens = TokenManager.get_tokens_for_user(user)
            response = {
                "tokens" : tokens , 
                'user' : UserSerializer(valid_user).data 
            }
            otp_object.delete()
            return success_response(data=response)
        except Exception as e:
            print(e)
            return internal_server_error_response()



class RegisterUserView(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer


    def validate_password(self, password):
        """
        Validates password requirements:
        - Must be more than 6 characters
        - Must contain at least one symbol
        - Must contain at least one number
        - Must contain at least one uppercase letter
        """
        if len(password) <= 6:
            return "Password must be longer than 6 characters."

        if not re.search(r"\d", password):  # Check for at least one digit
            return "Password must contain at least one number."

        if not re.search(r"[A-Z]", password):  # Check for at least one uppercase letter
            return "Password must contain at least one uppercase letter."

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):  # Check for at least one symbol
            return "Password must contain at least one special symbol."

        return None

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        first_name = serializer.validated_data['first_name']
        last_name = serializer.validated_data['last_name']
        email = serializer.validated_data['email'].lower()
        password = serializer.validated_data['password']
        confirmPassword = serializer.validated_data['confirmPassword']
        phone_number = serializer.validated_data['password']
        preferred_content = serializer.validated_data['preferred_content']
        # study_preference = serializer.validated_data['study_preference']
        # previous_year_performance = serializer.validated_data['previous_year_performance']
        current_year_level = serializer.validated_data['current_year_level']

        # validate that password and confirm password are the same
        if password != confirmPassword:
            return bad_request_response(message="Passwords do not match")
        

        password_validation_error = self.validate_password(password)
        if password_validation_error:
            return bad_request_response(message=password_validation_error)

        # check if email exist if yes return bad request
        if User.objects.filter(email=email).exists():
            return bad_request_response(message="Email already exist")
        
        # create new user if email does not exist
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_active=True,
            phone_number=phone_number,
            preferred_content=preferred_content,
            # study_preference=study_preference,
            # previous_year_performance=previous_year_performance,
            current_year_level=current_year_level,
        )
        user.set_password(password)
        user.save()
        response_data = dict(
            tokens= TokenManager.get_tokens_for_user(user),
            user=UserSerializer(user).data
        )

        return success_response(message='User registered successfully.',data=response_data,status_code=201)



class AccountVerifyCodeView(generics.GenericAPIView):
    serializer_class = CodeConfirmationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            code_entry = CodeConfirmation.objects.get(code=serializer.validated_data['code'], is_active=True)
            if code_entry.confirmation_type != 'registration':
                return bad_request_response(message="Invalid verification code")
        except CodeConfirmation.DoesNotExist:
            return bad_request_response(message="Invalid verification code")

        user = code_entry.user
        user.is_verify = True
        user.is_active = True
        user.set_password(serializer.validated_data['password'])
        user.save()
        code_entry.delete()
        response_data = dict(
            tokens= TokenManager.get_tokens_for_user(user),
            user=UserSerializer(user).data
        )
        return success_response(message='Account verified successfully.',data=response_data)



class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, uidb64, token, *args, **kwargs):
        try:
            # Decode the user ID from the URL
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_model().objects.get(pk=uid)
        except (ValueError, TypeError, get_user_model().DoesNotExist):
            return bad_request_response(message="Invalid token or user ID.")

        # Validate the token
        if not default_token_generator.check_token(user, token):
            return bad_request_response(message="Invalid or expired token.")

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_password = serializer.validated_data['new_password']

        # Set the new password and save
        user.set_password(new_password)
        user.save()

        return success_response(message= "Password successfully reset.")
    


class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user_model = get_user_model()

        try:
            user = user_model.objects.get(email=email)
        except user_model.DoesNotExist:
            return bad_request_response(message="User with this email does not exist.")

        # Generate password reset token and uid
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(user.pk.encode())

        # Construct the reset link
        reset_link = f"/password-reset/{uid}/{token}/"
        # reset_link = f"{settings.FRONTEND_URL}/password-reset/{uid}/{token}/"

        # Send the email with the reset link
        subject = "Password Reset Request"
        

        return success_response(message= "Password reset email sent.")
    
