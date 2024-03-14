from rest_framework import viewsets
from tasks.serializers import TaskSerializer, LabelSerializer
from .models import Task, Label
from user_management.permissions import UserPermission



class LabelViewSet(viewsets.ModelViewSet):
    
    permission_classes = [UserPermission]
    queryset = Label.objects.all()
    serializer_class = LabelSerializer

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(created_by=self.request.user)
        return query_set

class TaskViewSet(viewsets.ModelViewSet):
    
    permission_classes = [UserPermission]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(created_by=self.request.user)
        return query_set
