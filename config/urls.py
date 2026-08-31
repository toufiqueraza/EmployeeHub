from django.contrib import admin
from django.urls import include, path

from employees import views


urlpatterns = [
    path("admin/", admin.site.urls),

    path("", views.dashboard, name="dashboard"),

    path(
        "accounts/",
        include("django.contrib.auth.urls"),
    ),

    path(
        "employees/",
        include("employees.urls"),
    ),
]
