from rest_framework import generics

from rest_framework.permissions import IsAuthenticated
from account.models import User
from account.serializers.account import AccountProfileSerializer, PasswordChangeSerializer, UpdateTwoFactorAuthenticationRequestSerializer
from helper.utils.response.response_format import success_response , bad_request_response


# create a view that return user profile using the i am not using path variable use request.user
class UserProfileView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountProfileSerializer

    def get(self,request, **kwargs):
        user = request.user
        return success_response(data=self.serializer_class(user).data)
    

    def put(self,request):
        
        user = User.objects.get(id=request.user.id) 
        is_changed = False
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        user.current_year_level = request.data.get('current_year_level')
        user.study_preference = request.data.get('study_preference')
        user.previous_year_performance = request.data.get('previous_year_performance')
        user.current_year_level = request.data.get('current_year_level')
        user.phone_number = request.data.get('phone_number')
        user.preferred_content = request.data.get('preferred_content')
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        return success_response(message="Profile updated",data=self.serializer_class(user).data)



class PasswordChangeView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordChangeSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        current_password = serializer.validated_data['current_password']
        new_password = serializer.validated_data['new_password']

        # Check if current password is correct
        if not user.check_password(current_password):
            return bad_request_response(message="Current password is incorrect.")

        # Set new password and save user
        user.set_password(new_password)
        user.save()

        return success_response(message= "Password successfully changed.")
    


class UpdateTwoFactorAuthenticationView(generics.GenericAPIView):
    serializer_class = UpdateTwoFactorAuthenticationRequestSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        status = serializer.validated_data['status']
        user:User = request.user
        if status == 'enable':
            user.is_2fa_enabled = True
        else:
            user.is_2fa_enabled = False

        user.save()
        return success_response(
            message="Two factor authentication status updated successfully.",
            data=AccountProfileSerializer(user).data
        )
            
