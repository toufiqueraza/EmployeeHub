from datetime import date

from django.contrib.auth.models import Group, Permission, User
from django.test import TestCase
from django.urls import reverse

from .models import Department, Employee


class EmployeeModelTest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(
            name="IT",
            description="Information Technology",
        )

    def test_employee_creation(self):
        employee = Employee.objects.create(
            first_name="Rahul",
            last_name="Kumar",
            email="rahul@example.com",
            phone="9876543210",
            designation="Developer",
            department=self.department,
            date_joined=date(2026, 1, 1),
        )

        self.assertEqual(
            str(employee),
            "Rahul Kumar",
        )

    def test_department_protects_employees(self):
        employee = Employee.objects.create(
            first_name="Rahul",
            last_name="Kumar",
            email="rahul2@example.com",
            phone="9876543211",
            designation="Developer",
            department=self.department,
            date_joined=date(2026, 1, 1),
        )

        self.assertEqual(
            employee.department,
            self.department,
        )


class AuthenticationTest(TestCase):
    def test_employee_list_requires_login(self):
        response = self.client.get(
            reverse("employees:employee_list")
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(
            "/accounts/login/",
            response.url,
        )


class EmployeePermissionTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="employee_test",
            password="Test@12345",
        )

        self.group = Group.objects.create(
            name="EmployeeTest"
        )

        permission = Permission.objects.get(
            codename="view_employee",
            content_type__app_label="employees",
        )

        self.group.permissions.add(permission)
        self.user.groups.add(self.group)

    def test_employee_can_view_employee_list(self):
        self.client.login(
            username="employee_test",
            password="Test@12345",
        )

        response = self.client.get(
            reverse("employees:employee_list")
        )

        self.assertEqual(response.status_code, 200)
