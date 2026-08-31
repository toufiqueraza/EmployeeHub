from django import forms

from .models import Department, Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "designation",
            "department",
            "photo",
            "date_joined",
        ]

        widgets = {
            "date_joined": forms.DateInput(
                attrs={"type": "date"}
            ),
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = [
            "name",
            "description",
        ]
