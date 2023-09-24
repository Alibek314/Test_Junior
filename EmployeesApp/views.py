from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from .models import Employees

# Create your views here.


def all_employees(request):
    """
    Displays all employees in Tree form (recursetree used in template)
    """
    employees = Employees.objects.all()
    username = request.user.username
    return render(request, "EmployeesApp/all_employees.html", {
        "employees": employees,
        "username": username,
    })


def get_employee(request, emp_id):
    """
    Shows detailed employee information
    """
    employee = get_object_or_404(Employees, id=emp_id)
    username = request.user.username
    return render(request, "EmployeesApp/one_employee.html", {
        "employee": employee
    })


def show_team(request):
    """
    Shows list of all employees
    """
    team = Employees.objects.all()
    paginator = Paginator(team, 100)
    username = request.user.username
    if request.user.is_authenticated:
        if "Table-Order" in request.headers:
            sort_by = request.headers["Table-Order"].split(",")[1]
            page_num = int(request.headers["Table-Order"].split(",")[0])
            current_objects = paginator.get_page(page_num).object_list
            if sort_by == 'name':
                sorted_employees = sorted(current_objects, key=lambda x: x.name)
            elif sort_by == 'position':
                sorted_employees = sorted(current_objects, key=lambda x: x.position)
            elif sort_by == 'hire_date':
                sorted_employees = sorted(current_objects, key=lambda x: x.hire_date)
            elif sort_by == 'salary':
                sorted_employees = sorted(current_objects, key=lambda x: x.salary)
            else:
                sorted_employees = current_objects
            return render(request, "EmployeesApp/sorted_table.html", {
                "sorted_employees": sorted_employees,
                "username": username,
            })
        else:
            page_obj = paginator.get_page(request.GET.get("page"))
            return render(request, "EmployeesApp/show_team.html", {
                "page_obj": page_obj,
                "username": username,
            })
    else:
        page_obj = paginator.get_page(request.GET.get("page"))
        return render(request, "EmployeesApp/team_stable.html", {
                    "page_obj": page_obj,
                    "username": username,
            })


def redirect_company(request):
    """
    This view redirects client from rest_framework's default login page to "http://127.0.0.1:8000/company/"
    """
    return redirect('hierarchy_route')
