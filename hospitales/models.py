from django.db import models
import oracledb

# Database connection
connection = oracledb.connect(
    user="SYSTEM",
    password="oracle",
    dsn="localhost:1521/xe"
)

from django.db import models

class Dept(models.Model):
    dept_no = models.IntegerField(primary_key=True, db_column='DEPT_NO')
    dnombre = models.CharField(max_length=50, db_column='DNOMBRE')
    loc = models.CharField(max_length=50, db_column='LOC')

    class Meta:
        db_table = 'DEPT'
        managed = False

class Emp(models.Model):
    emp_no = models.IntegerField(primary_key=True, db_column='EMP_NO')
    apellido = models.CharField(max_length=50, db_column='APELLIDO')
    oficio = models.CharField(max_length=50, db_column='OFICIO')
    dir = models.IntegerField(null=True, db_column='DIR')
    fecha_alt = models.DateField(db_column='FECHA_ALT')
    salario = models.DecimalField(max_digits=10, decimal_places=2, db_column='SALARIO')
    comision = models.DecimalField(max_digits=10, decimal_places=2, null=True, db_column='COMISION')
    dept_no = models.ForeignKey(Dept, on_delete=models.CASCADE, db_column='DEPT_NO')

    class Meta:
        db_table = 'EMP'
        managed = False

class Hospital(models.Model):
    hospital_cod = models.IntegerField(primary_key=True, db_column='HOSPITAL_COD')
    nombre = models.CharField(max_length=50, db_column='NOMBRE')
    direccion = models.CharField(max_length=100, db_column='DIRECCION')
    telefono = models.CharField(max_length=15, db_column='TELEFONO')
    num_cama = models.IntegerField(db_column='NUM_CAMA')  # Changed from NUM_CAMAS to NUM_CAMA

    class Meta:
        db_table = 'HOSPITAL'
        managed = False
    
    def __str__(self):
        return self.nombre

class Departamento(models.Model):
    numero = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    localidad = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nombre

class ServiceDepartamentos:
    def __init__(self):
        self.connection = oracledb.connect(
            user="SYSTEM",
            password="oracle",
            dsn="localhost:1521/xe"
        )
    
    def get_departamentos(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT DEPT_NO, DNOMBRE, LOC FROM DEPT")  # Changed from EMP table to DEPT table
        departamentos = cursor.fetchall()
        cursor.close()
        return departamentos
    
    def get_departamento_by_id(self, dept_no):
        cursor = self.connection.cursor()
        cursor.execute("SELECT DEPTNO, DNAME, LOC FROM DEPT WHERE DEPTNO = :1", [dept_no])
        departamento = cursor.fetchone()
        cursor.close()
        return departamento
    
    def get_empleados(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM EMP WHERE DEPTNO = :1", [dept_no])  # Ejemplo de consulta parametrizada
        empleados = cursor.fetchall()
        cursor.close()
        return empleados

class ServiceHospitales:
    def __init__(self):
        self.connection = oracledb.connect(
            user="SYSTEM",
            password="oracle",
            dsn="localhost:1521/xe"
        )
    
    def get_hospitales(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM HOSPITAL")
        hospitales = cursor.fetchall()
        cursor.close()
        return hospitales
