from django.urls import path

from . import views
from . import user_views


app_name = "employees"


urlpatterns = [
    path("", views.employee_list, name="employee_list"),

    path("add/", views.employee_create, name="employee_create"),

    path("<int:pk>/", views.employee_detail, name="employee_detail"),

    path("<int:pk>/edit/", views.employee_update, name="employee_update"),

    path("<int:pk>/delete/", views.employee_delete, name="employee_delete"),

    path("departments/", views.department_list, name="department_list"),

    path("departments/add/", views.department_create, name="department_create"),

    path(
        "departments/<int:pk>/edit/",
        views.department_update,
        name="department_update",
    ),

    path(
        "departments/<int:pk>/delete/",
        views.department_delete,
        name="department_delete",
    ),

    # User management
    path("users/", user_views.user_list, name="user_list"),
    path("users/add/", user_views.user_create, name="user_create"),
]
