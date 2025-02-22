from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.pagination import PageNumberPagination
from .models import LeaveRequest, Employee
from .serializers import LeaveRequestSerializers, LeaveStatusUpdateSerializer
# Create your views here.
class CustomPagination(PageNumberPagination):
    page_size = 10

class LeaveRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = LeaveRequestSerializers
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = LeaveRequest.objects.all()

        employee_id = self.request.query_params.get('employee_id', None)
        if employee_id:
            queryset = queryset.filter(employee_id=employee_id)

        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(status=status)
        
        queryset = queryset.order_by('start_date')
        return queryset
    
    def perform_create(self, serializer):
        employee_id = self.request.data.get("employee_id")
        employee = get_object_or_404(Employee, id=employee_id)
        serializer.save(employee=employee)

class LeaveStatusUpdateView(generics.UpdateAPIView):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveStatusUpdateSerializer

    def get_object(self):
        return LeaveRequest.objects.get(id=self.kwargs['leave_id'])
    
    def update(self, request, *args, **kwargs):
        leave_request = self.get_object()
        if leave_request.status not in ['pending']:
            return Response({"detail":"Leave status can only be updated if it is pending"},status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)
    
