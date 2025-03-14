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
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT COUNT(*) FROM EMP')
            count = cursor.fetchone()[0]
            print(f"Number of employees: {count}")  # Debug print
            
            cursor.execute('''
                SELECT 
                    EMP_NO,
                    APELLIDO,
                    OFICIO,
                    DIR,
                    FECHA_ALT,
                    SALARIO,
                    COMISION,
                    DEPT_NO
                FROM EMP
            ''')
            rows = cursor.fetchall()
            print(f"Fetched rows: {rows}")  # Debug print
            
            columns = ['EMP_NO', 'APELLIDO', 'OFICIO', 'DIR', 'FECHA_ALT', 'SALARIO', 'COMISION', 'DEPT_NO']
            empleados_list = [dict(zip(columns, row)) for row in rows]
            
    except Exception as e:
        print(f"Database error: {e}")  # Debug print
        empleados_list = []
            
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
def lista_departamentos(request):
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT d.DEPT_NO, d.DNOMBRE, d.LOC,
                   COUNT(e.EMP_NO) as num_empleados,
                   NVL(SUM(e.SALARIO), 0) as total_salarios
            FROM DEPT d
            LEFT JOIN EMP e ON d.DEPT_NO = e.DEPT_NO
            GROUP BY d.DEPT_NO, d.DNOMBRE, d.LOC
            ORDER BY d.DEPT_NO
        ''')
        columns = ['DEPT_NO', 'DNOMBRE', 'LOC', 'NUM_EMPLEADOS', 'TOTAL_SALARIOS']
        departamentos = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return render(request, 'aplicacion/lista_departamentos.html', {'departamentos': departamentos})

@login_required
def detalle_departamento(request, dept_no):
    with connection.cursor() as cursor:
        # Get department info
        cursor.execute('''
            SELECT d.DEPT_NO, d.DNOMBRE, d.LOC,
                   COUNT(e.EMP_NO) as num_empleados,
                   NVL(SUM(e.SALARIO), 0) as total_salarios
            FROM DEPT d
            LEFT JOIN EMP e ON d.DEPT_NO = e.DEPT_NO
            WHERE d.DEPT_NO = %s
            GROUP BY d.DEPT_NO, d.DNOMBRE, d.LOC
        ''', [dept_no])
        dept_data = cursor.fetchone()
        
        # Get employees in department
        cursor.execute('''
            SELECT EMP_NO, APELLIDO, OFICIO, FECHA_ALT, SALARIO, COMISION
            FROM EMP
            WHERE DEPT_NO = %s
            ORDER BY APELLIDO
        ''', [dept_no])
        empleados = [dict(zip(['EMP_NO', 'APELLIDO', 'OFICIO', 'FECHA_ALT', 'SALARIO', 'COMISION'], row)) 
                    for row in cursor.fetchall()]
        
        if dept_data:
            departamento = dict(zip(['DEPT_NO', 'DNOMBRE', 'LOC', 'NUM_EMPLEADOS', 'TOTAL_SALARIOS'], dept_data))
            return render(request, 'aplicacion/detalle_departamento.html', {
                'departamento': departamento,
                'empleados': empleados
            })
        return HttpResponse("Departamento no encontrado", status=404)

@login_required
def hospitales(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT HOSPITAL_COD, NOMBRE, DIRECCION, TELEFONO, NUM_CAMA FROM HOSPITAL')
        columns = ['HOSPITAL_COD', 'NOMBRE', 'DIRECCION', 'TELEFONO', 'NUM_CAMA']
        hospitales_list = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return render(request, 'aplicacion/hospitales.html', {'hospitales': hospitales_list})

@login_required
def empleados(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM EMP')
        columns = [col[0] for col in cursor.description]
        empleados_list = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return render(request, 'aplicacion/empleados.html', {'empleados': empleados_list})

@login_required
def departamentos(request):
    with connection.cursor() as cursor:
        cursor.execute('SELECT DEPT_NO, DNOMBRE, LOC FROM DEPT')
        columns = ['DEPT_NO', 'DNOMBRE', 'LOC']
        departamentos_list = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return render(request, 'aplicacion/departamentos.html', {'departamentos': departamentos_list})

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


@login_required
def editar_departamento(request, dept_no):
    try:
        with connection.cursor() as cursor:
            if request.method == 'POST':
                dnombre = request.POST.get('dnombre')
                loc = request.POST.get('loc')
                cursor.execute('UPDATE DEPT SET DNOMBRE = %s, LOC = %s WHERE DEPT_NO = %s', 
                             [dnombre, loc, dept_no])
                return redirect('departamentos')
            
            # Get department data for editing
            cursor.execute('SELECT DEPT_NO, DNOMBRE, LOC FROM DEPT WHERE DEPT_NO = %s', [dept_no])
            row = cursor.fetchone()
            if row:
                departamento = dict(zip(['DEPT_NO', 'DNOMBRE', 'LOC'], row))
                return render(request, 'aplicacion/editar_departamento.html', {'departamento': departamento})
            
        return HttpResponse("Departamento no encontrado", status=404)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)

@login_required
def editar_empleado(request, emp_no):
    try:
        with connection.cursor() as cursor:
            if request.method == 'POST':
                apellido = request.POST.get('apellido')
                oficio = request.POST.get('oficio')
                dir = request.POST.get('dir')
                fecha_alt = request.POST.get('fecha_alt')
                salario = request.POST.get('salario')
                comision = request.POST.get('comision')
                dept_no = request.POST.get('dept_no')
                
                cursor.execute('''
                    UPDATE EMP 
                    SET APELLIDO = %s, OFICIO = %s, DIR = %s, 
                        FECHA_ALT = %s, SALARIO = %s, COMISION = %s, 
                        DEPT_NO = %s 
                    WHERE EMP_NO = %s
                ''', [apellido, oficio, dir, fecha_alt, salario, comision, dept_no, emp_no])
                return redirect('empleados')
            
            # Get employee data for editing
            cursor.execute('SELECT * FROM EMP WHERE EMP_NO = %s', [emp_no])
            row = cursor.fetchone()
            columns = ['EMP_NO', 'APELLIDO', 'OFICIO', 'DIR', 'FECHA_ALT', 'SALARIO', 'COMISION', 'DEPT_NO']
            empleado = dict(zip(columns, row))
            
            # Get departments for dropdown
            cursor.execute('SELECT DEPT_NO, DNOMBRE FROM DEPT')
            departamentos = [dict(zip(['DEPT_NO', 'DNOMBRE'], row)) for row in cursor.fetchall()]
            
            return render(request, 'aplicacion/editar_empleado.html', {
                'empleado': empleado,
                'departamentos': departamentos
            })
            
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)
