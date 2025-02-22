from rest_framework import serializers
from .models import LeaveRequest, Employee

class LeaveRequestSerializers(serializers.ModelSerializer):
    employee_id = serializers.IntegerField(write_only=True)
    employee = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = LeaveRequest
        fields = ['id', 'employee_id', 'employee', 'leave_type', 'start_date', 'end_date', 'status']

    def validate_leave_type(self, value):
        if value not in dict(LeaveRequest.LEAVE_TYPE).keys():
            raise serializers.ValidationError("Invalid leave type.")
        return value
    
    def validate_employee(self, value):
        if not Employee.objects.filter(id=value.pk).exists():
            raise serializers.ValidationError("Employee not found.")
        return value
    
    def create(self, validated_data):
        employee_id = validated_data.pop('employee_id')
        employee = Employee.objects.get(id=employee_id)
        validated_data['employee'] = employee
        return super().create(validated_data)
    
class LeaveStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = ['status']
    
    def validate_status(self, value):
        if value not in ['approved', 'rejected']:
            raise serializers.ValidationError("status can only be 'approved' or 'rejected'.")
        return value
