from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DepartmentForm, EmployeeForm
from .models import Department, Employee


@login_required
def dashboard(request):
    employees = Employee.objects.select_related("department")

    return render(
        request,
        "employees/dashboard.html",
        {
            "employee_count": employees.count(),
            "department_count": Department.objects.count(),
            "recent_employees": employees.order_by("-created_at")[:5],
        },
    )


@login_required
def employee_list(request):
    employees = Employee.objects.select_related("department")

    q = request.GET.get("q", "").strip()
    dept = request.GET.get("department", "").strip()

    if q:
        employees = employees.filter(
            Q(first_name__icontains=q)
            | Q(last_name__icontains=q)
            | Q(email__icontains=q)
            | Q(designation__icontains=q)
        )

    if dept:
        employees = employees.filter(department_id=dept)

    page_obj = Paginator(employees.order_by("first_name"), 10).get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "employees/employee_list.html",
        {
            "page_obj": page_obj,
            "departments": Department.objects.all(),
            "query": q,
            "selected_department": dept,
        },
    )


@login_required
def employee_create(request):
    form = EmployeeForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        emp = form.save()
        messages.success(
            request,
            f"{emp.first_name} {emp.last_name} created successfully.",
        )
        return redirect("employees:employee_list")

    return render(request, "employees/employee_form.html", {"form": form})


@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(
        request,
        "employees/employee_detail.html",
        {"employee": employee},
    )


@login_required
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    form = EmployeeForm(
        request.POST or None,
        request.FILES or None,
        instance=employee,
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Employee updated successfully.")
        return redirect("employees:employee_detail", pk=pk)

    return render(request, "employees/employee_form.html", {"form": form})


@login_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == "POST":
        name = f"{employee.first_name} {employee.last_name}"
        employee.delete()
        messages.warning(request, f"{name} deleted successfully.")
        return redirect("employees:employee_list")

    return render(
        request,
        "employees/employee_confirm_delete.html",
        {"employee": employee},
    )


@login_required
def department_list(request):
    departments = Department.objects.annotate(
        employee_count=Count("employees")
    )
    return render(
        request,
        "employees/department_list.html",
        {"departments": departments},
    )


@login_required
def department_create(request):
    form = DepartmentForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        dept = form.save()
        messages.success(
            request,
            f"{dept.name} department created successfully.",
        )
        return redirect("employees:department_list")

    return render(request, "employees/department_form.html", {"form": form})


@login_required
def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)

    form = DepartmentForm(request.POST or None, instance=department)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Department updated successfully.")
        return redirect("employees:department_list")

    return render(request, "employees/department_form.html", {"form": form})


@login_required
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)

    if request.method == "POST":
        name = department.name
        department.delete()
        messages.warning(request, f"{name} deleted successfully.")
        return redirect("employees:department_list")

    return render(
        request,
        "employees/department_confirm_delete.html",
        {"department": department},
    )
