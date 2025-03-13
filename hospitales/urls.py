from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hospitales/', views.hospitales, name='hospitales'),
    path('empleados/', views.empleados, name='empleados'),
    path('departamentos/', views.departamentos, name='departamentos'),
    path('insertar-departamento/', views.insertar_departamento, name='insertar_departamento'),
    path('insertar-empleado/', views.insertar_empleado, name='insertar_empleado'),
    path('eliminar-departamento/<int:dept_no>/', views.eliminar_departamento, name='eliminar_departamento'),
    path('eliminar-empleado/<int:emp_no>/', views.eliminar_empleado, name='eliminar_empleado'),
]