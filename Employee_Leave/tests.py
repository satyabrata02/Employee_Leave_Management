from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Employee, LeaveRequest

# Create your tests here.
class LeaveRequestAPITestCase(APITestCase):
    def setUp(self):
        """Setup initial data before each test"""
        self.employee = Employee.objects.create(name="John Doe", position="Software Engineer")

        self.leave_request = LeaveRequest.objects.create(
            employee=self.employee,
            leave_type="sick_leave",
            start_date="2025-03-15",
            end_date="2025-03-17",
            status="pending"
        )

        self.leave_create_url = reverse("leave-request-list-create")
        self.leave_update_url = reverse("leave-status-update", kwargs={"leave_id": self.leave_request.id})

    def test_create_leave_request(self):
        """Test creating a new leave request"""
        data = {
            "employee_id": self.employee.id,
            "leave_type": "casual_leave",
            "start_date": "2025-04-01",
            "end_date": "2025-04-03",
            "status": "pending"
        }
        response = self.client.post(self.leave_create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["leave_type"], "casual_leave")

    def test_get_leave_requests(self):
        """Test retrieving leave requests"""
        response = self.client.get(self.leave_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertIn("results", response.data)
        self.assertGreaterEqual(len(response.data["results"]), 1)

    def test_filter_leave_requests_by_employee(self):
        """Test filtering leave requests by employee_id"""
        response = self.client.get(f"{self.leave_create_url}?employee_id={self.employee.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertIn("results", response.data)
        self.assertEqual(response.data["results"][0]["employee"], self.employee.name)

    def test_update_leave_status(self):
        """Test updating leave request status"""
        data = {"status": "approved"}
        response = self.client.put(self.leave_update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.leave_request.refresh_from_db()
        self.assertEqual(self.leave_request.status, "approved")

    def test_update_leave_status_invalid(self):
        """Test updating leave status when it's not pending (should fail)"""
        self.leave_request.status = "approved"
        self.leave_request.save()

        data = {"status": "rejected"}
        response = self.client.put(self.leave_update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Leave status can only be updated if it is pending")
