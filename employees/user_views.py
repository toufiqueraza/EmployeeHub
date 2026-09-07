from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404, redirect, render


User = get_user_model()


@login_required
@permission_required("auth.view_user", raise_exception=True)
def user_list(request):
    users = User.objects.prefetch_related("groups").all().order_by("username")

    return render(
        request,
        "employees/user_list.html",
        {"users": users},
    )


@login_required
@permission_required("auth.add_user", raise_exception=True)
def user_create(request):
    groups = Group.objects.filter(
        name__in=["Admin", "HR", "Employee"]
    )

    error = None

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        role = request.POST.get("role", "")

        if not username or not password or not role:
            error = "Username, password and role are required."

        elif User.objects.filter(username=username).exists():
            error = "Username already exists."

        elif not Group.objects.filter(name=role).exists():
            error = "Invalid role selected."

        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )

            group = get_object_or_404(Group, name=role)
            user.groups.add(group)

            return redirect("employees:user_list")

    return render(
        request,
        "employees/user_form.html",
        {
            "groups": groups,
            "error": error,
        },
    )


@login_required
@permission_required("auth.change_user", raise_exception=True)
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)

    groups = Group.objects.filter(
        name__in=["Admin", "HR", "Employee"]
    )

    error = None

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        role = request.POST.get("role", "")

        if not username or not role:
            error = "Username and role are required."

        elif User.objects.filter(
            username=username
        ).exclude(pk=user.pk).exists():
            error = "Username already exists."

        else:
            user.username = username
            user.email = email
            user.save()

            group = get_object_or_404(Group, name=role)
            user.groups.set([group])

            return redirect("employees:user_list")

    current_group = user.groups.first()

    return render(
        request,
        "employees/user_form.html",
        {
            "user_obj": user,
            "groups": groups,
            "error": error,
            "edit_mode": True,
            "current_group": current_group,
        },
    )


@login_required
@permission_required("auth.change_user", raise_exception=True)
def user_toggle_status(request, pk):
    user = get_object_or_404(User, pk=pk)

    if user != request.user:
        user.is_active = not user.is_active
        user.save(update_fields=["is_active"])

    return redirect("employees:user_list")


@login_required
@permission_required("auth.delete_user", raise_exception=True)
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)

    if user != request.user:
        user.delete()

    return redirect("employees:user_list")
