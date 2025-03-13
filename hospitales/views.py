from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Emp, Dept, Hospital
from django.db import connection
from django.http import JsonResponse

@login_required
def index(request):
    return render(request, 'aplicacion/index.html')

@login_required
def empleados(request):
    empleados_list = []
    if request.method == 'POST':
        empleados_list = Emp.objects.raw('SELECT * FROM EMP')
    return render(request, 'aplicacion/empleados.html', {'empleados': empleados_list})

@login_required
def insertar_departamento(request):
    if request.method == 'POST':
        dept_no = request.POST.get('dept_no')
        dnombre = request.POST.get('dnombre')
        loc = request.POST.get('loc')
        
        try:
            Dept.objects.create(
                dept_no=dept_no,
                dnombre=dnombre,
                loc=loc
            )
            # Get all departments after insertion
            departamentos_list = Dept.objects.raw('SELECT * FROM DEPT')
            return render(request, 'aplicacion/departamentos.html', {'departamentos': departamentos_list})
        except Exception as e:
            return render(request, 'aplicacion/insertar_departamento.html', {'error': str(e)})
    
    return render(request, 'aplicacion/insertar_departamento.html')

@login_required
def departamentos(request):
    departamentos_list = Dept.objects.raw('SELECT * FROM DEPT')  # Always show departments
    return render(request, 'aplicacion/departamentos.html', {'departamentos': departamentos_list})

@login_required
def empleados(request):
    empleados_list = Emp.objects.raw('SELECT * FROM EMP')  # Always show employees
    return render(request, 'aplicacion/empleados.html', {'empleados': empleados_list})

@login_required
def detalle_departamento(request, dept_no):
    try:
        departamento = Dept.objects.get(deptno=dept_no)
    except Dept.DoesNotExist:
        return HttpResponse("Departamento no encontrado", status=404)
    return render(request, 'aplicacion/detalle_departamento.html', {'departamento': departamento})

@login_required
def hospitales(request):
    hospitales_list = []
    if request.method == 'POST':
        hospitales_list = Hospital.objects.raw('SELECT * FROM HOSPITAL')
    return render(request, 'aplicacion/hospitales.html', {'hospitales': hospitales_list})

@login_required
def test_db(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM DUAL")
            result = cursor.fetchone()
            if result:
                return JsonResponse({"status": "Connected", "message": "Successfully connected to Oracle database"})
    except Exception as e:
        return JsonResponse({"status": "Error", "message": str(e)}, status=500)

@login_required
def insertar_empleado(request):
    if request.method == 'POST':
        emp_no = request.POST.get('emp_no')
        apellido = request.POST.get('apellido')
        oficio = request.POST.get('oficio')
        dir = request.POST.get('dir')
        fecha_alt = request.POST.get('fecha_alt')
        salario = request.POST.get('salario')
        comision = request.POST.get('comision')
        dept_no = request.POST.get('dept_no')
        
        try:
            Emp.objects.create(
                emp_no=emp_no,
                apellido=apellido,
                oficio=oficio,
                dir=dir,
                fecha_alt=fecha_alt,
                salario=salario,
                comision=comision,
                dept_no_id=dept_no
            )
            return redirect('empleados')
        except Exception as e:
            return render(request, 'aplicacion/insertar_empleado.html', {'error': str(e)})
    
    departamentos = Dept.objects.all()
    return render(request, 'aplicacion/insertar_empleado.html', {'departamentos': departamentos})


@login_required
def eliminar_departamento(request, dept_no):
    try:
        departamento = Dept.objects.raw('SELECT * FROM DEPT WHERE DEPT_NO = %s', [dept_no])[0]
        if request.method == 'POST':
            with connection.cursor() as cursor:
                cursor.execute('DELETE FROM DEPT WHERE DEPT_NO = %s', [dept_no])
            return redirect('departamentos')
        return render(request, 'aplicacion/eliminar_departamento.html', {'departamento': departamento})
    except IndexError:
        return HttpResponse("Departamento no encontrado", status=404)

@login_required
def eliminar_empleado(request, emp_no):
    try:
        empleado = Emp.objects.raw('SELECT * FROM EMP WHERE EMP_NO = %s', [emp_no])[0]
        if request.method == 'POST':
            with connection.cursor() as cursor:
                cursor.execute('DELETE FROM EMP WHERE EMP_NO = %s', [emp_no])
            return redirect('empleados')
        return render(request, 'aplicacion/eliminar_empleado.html', {'empleado': empleado})
    except IndexError:
        return HttpResponse("Empleado no encontrado", status=404)
