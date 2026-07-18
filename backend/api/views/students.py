# views.py
from rest_framework import viewsets, permissions, status

from account.models import User
from api.serializers.students import StudentSerializer
from helper.utils.response.response_format import success_response, paginate_success_response


class StudentViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_staff=False).order_by("-created_at")
    serializer_class = StudentSerializer
    # permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return success_response(serializer.data)
    

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return paginate_success_response(
            request,
            serializer.data,
            page_size=int(request.GET.get("page_size",20))
        )
