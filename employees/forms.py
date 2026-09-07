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

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if not email:
            raise forms.ValidationError(
                "Email address is required."
            )

        return email

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()

        if not phone.isdigit():
            raise forms.ValidationError(
                "Phone number must contain only digits."
            )

        if len(phone) < 10 or len(phone) > 15:
            raise forms.ValidationError(
                "Phone number must be between 10 and 15 digits."
            )

        return phone


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = [
            "name",
            "description",
        ]

    def clean_name(self):
        return self.cleaned_data["name"].strip()
