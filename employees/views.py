from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DepartmentForm, EmployeeForm
from .models import Department, Employee


@login_required
def dashboard(request):
    employees = Employee.objects.select_related("department")

    context = {
        "employee_count": employees.count(),
        "department_count": Department.objects.count(),
        "recent_employees": employees.order_by("-created_at")[:5],
    }

    return render(
        request,
        "employees/dashboard.html",
        context,
    )


@login_required
def employee_list(request):
    employees = Employee.objects.select_related("department")

    query = request.GET.get("q", "").strip()
    department_id = request.GET.get("department", "").strip()

    if query:
        employees = employees.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(email__icontains=query)
            | Q(designation__icontains=query)
        )

    if department_id:
        employees = employees.filter(department_id=department_id)

    employees = employees.order_by("first_name", "last_name")

    paginator = Paginator(employees, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {
        "page_obj": page_obj,
        "departments": Department.objects.all().order_by("name"),
        "query": query,
        "selected_department": department_id,
    }

    return render(
        request,
        "employees/employee_list.html",
        context,
    )


@login_required
def employee_create(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("employees:employee_list")
    else:
        form = EmployeeForm()

    return render(
        request,
        "employees/employee_form.html",
        {
            "form": form,
            "page_title": "Add Employee",
        },
    )


@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(
        Employee.objects.select_related("department"),
        pk=pk,
    )

    return render(
        request,
        "employees/employee_detail.html",
        {"employee": employee},
    )


@login_required
def employee_update(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == "POST":
        form = EmployeeForm(
            request.POST,
            request.FILES,
            instance=employee,
        )

        if form.is_valid():
            form.save()
            return redirect(
                "employees:employee_detail",
                pk=employee.pk,
            )
    else:
        form = EmployeeForm(instance=employee)

    return render(
        request,
        "employees/employee_form.html",
        {
            "form": form,
            "page_title": "Edit Employee",
            "employee": employee,
        },
    )


@login_required
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == "POST":
        employee.delete()
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
    ).order_by("name")

    return render(
        request,
        "employees/department_list.html",
        {"departments": departments},
    )


@login_required
def department_create(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("employees:department_list")
    else:
        form = DepartmentForm()

    return render(
        request,
        "employees/department_form.html",
        {
            "form": form,
            "page_title": "Add Department",
        },
    )


@login_required
def department_update(request, pk):
    department = get_object_or_404(Department, pk=pk)

    if request.method == "POST":
        form = DepartmentForm(
            request.POST,
            instance=department,
        )

        if form.is_valid():
            form.save()
            return redirect("employees:department_list")
    else:
        form = DepartmentForm(instance=department)

    return render(
        request,
        "employees/department_form.html",
        {
            "form": form,
            "page_title": "Edit Department",
        },
    )


@login_required
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)

    if request.method == "POST":
        department.delete()
        return redirect("employees:department_list")

    return render(
        request,
        "employees/department_confirm_delete.html",
        {"department": department},
    )
