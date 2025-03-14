from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('empleados/', views.empleados, name='empleados'),
    path('departamentos/', views.departamentos, name='departamentos'),
    path('hospitales/', views.hospitales, name='hospitales'),
    path('insertar-empleado/', views.insertar_empleado, name='insertar_empleado'),
    path('insertar-departamento/', views.insertar_departamento, name='insertar_departamento'),
    path('eliminar-empleado/<int:emp_no>/', views.eliminar_empleado, name='eliminar_empleado'),
    path('eliminar-departamento/<int:dept_no>/', views.eliminar_departamento, name='eliminar_departamento'),
    path('editar-departamento/<int:dept_no>/', views.editar_departamento, name='editar_departamento'),
    path('editar-empleado/<int:emp_no>/', views.editar_empleado, name='editar_empleado'),
    path('lista-departamentos/', views.lista_departamentos, name='lista_departamentos'),
    path('detalle-departamento/<int:dept_no>/', views.detalle_departamento, name='detalle_departamento'),
    path('buscar-empleado/', views.buscar_empleado, name='buscar_empleado'),
]