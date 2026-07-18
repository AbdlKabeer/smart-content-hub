from rest_framework import serializers

from account.models import User




class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        exclude = ('password','last_login','groups','user_permissions','is_admin','is_superuser','is_staff',)