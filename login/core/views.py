from django.shortcuts import render, redirect
from .forms import CitaForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login
import mysql.connector
from .forms import ServicioForm
from .models import Cita
from django.db import connection
from .models import Empleado
from django.contrib import messages
from django.db import connection
from .models import Cita

def crear_cita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            username = request.user.username
            form.instance.username = username
            form.save()
            return redirect('citas')
    else:
        form = CitaForm()
    return render(request, 'core/citas.html', {'form': form})
    
def insert_empleado(username, nombre, apellido, contrasena, cargo, email):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="barberia"
        )
        cursor = connection.cursor()

  
        query = "INSERT INTO empleados (username, nombre, apellido, contrasena, cargo, email) VALUES (%s, %s, %s, %s, %s, %s);"
        cursor.execute(query, (username, nombre, apellido, contrasena, cargo, email))


        connection.commit()

        cursor.close()
        connection.close()

        return True
    except mysql.connector.Error as e:
        print("Error al insertar en la tabla empleados:", e)
        return False

def register(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)

        if user_creation_form.is_valid():
            user = user_creation_form.save()

            username = user_creation_form.cleaned_data['username']
            nombre = user_creation_form.cleaned_data['first_name']
            apellido = user_creation_form.cleaned_data['last_name']
            contrasena = user_creation_form.cleaned_data['password1']
            cargo = request.POST.get('cargo')  
            email = user_creation_form.cleaned_data['email']

            if insert_empleado(username, nombre, apellido, contrasena, cargo, email):
                user = authenticate(username=username, password=contrasena)
                login(request, user)
                return redirect('home')
            else:
                data['error_message'] = "Error al registrar al empleado"

        else:
            data['form'] = user_creation_form

    return render(request, 'registration/register.html', data)


# Create your views here.
def home(request):
    return render(request, 'core/home.html')

@login_required
def servicios(request):
    return render(request, 'core/servicios.html')

@login_required
def products(request):
    return render(request, 'core/products.html')

@login_required
def citas(request):
    return render(request, 'core/citas.html')



def exit(request):
    logout(request)
    return redirect('home')

def insert_servicio(username, tipos_servicio, fecha, hora, productos, cantidad_producto):
    print("insert servicio entro")
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="barberia"
        )
        cursor = connection.cursor()

        for tipo_servicio in tipos_servicio:
            for producto in productos:
                query = "INSERT INTO servicios (username, tipo_servicio, fecha, hora, producto, cantidad_producto) VALUES (%s, %s, %s, %s, %s, %s);"
                cursor.execute(query, (username, tipo_servicio, fecha, hora, producto, cantidad_producto))
                
        connection.commit()

        cursor.close()
        connection.close()

        return True
    except mysql.connector.Error as e:
        print("Error al insertar en la tabla servicios:", e)
        return False

def servicios(request):
    print("La función servicios se ha llamado.")
    print(request.user.username)

    form = ServicioForm()
    try:
        if request.method == 'POST':
            form = ServicioForm(request.POST)
            if form.is_valid():
                username = request.user.username 
                tipos_servicio = [form.cleaned_data['tipo_servicio']]  
                fecha = form.cleaned_data['fecha']  
                hora = form.cleaned_data['hora']  
                productos = form.cleaned_data['productos']  
                cantidad_producto = form.cleaned_data['cantidad_producto']  
                if insert_servicio(username, tipos_servicio, fecha, hora, productos, cantidad_producto):
                    print("Servicio insertado correctamente")
                    return redirect('success') 
                else:
                    print("Error al insertar el servicio")
            else:
                print("El formulario no es válido")
                print(form.errors)  
    except Exception as e:
        print("Ocurrió una excepción:", e)
    return render(request, 'core/servicios.html', {'form': form})




def obtener_cargo(username):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="barberia"
        )
        cursor = connection.cursor()

        query = "SELECT cargo FROM empleados WHERE username = %s"
        cursor.execute(query, (username,))
        cargo = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return cargo
    except mysql.connector.Error as e:
        print("Error al obtener el cargo del empleado:", e)
        return None
    
@login_required
def empleado(request):
    if request.method == 'POST':
        certificacion = request.POST.get('certificacion')
        username = request.user.username
        Empleado.objects.filter(username=username).update(certificados=certificacion)
        return redirect('empleado')
    else:
        username = request.user.username
        cargo = obtener_cargo(username)
        usuario = request.user

        # Obtener todas las citas del empleado utilizando un query SQL
        citas = []
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM citas WHERE username = %s", [username])
                print(username)
                citas = cursor.fetchall()
        except Exception as e:
            print("Error al obtener las citas del empleado:", e)

        return render(request, 'core/empleado.html', {'cargo': cargo, 'user': usuario, 'citas': citas})

@login_required
def eliminar_cita(request):
    if request.method == 'POST':
        cliente_nombre = request.POST.get('cliente_nombre')
        tipo_servicio = request.POST.get('tipo_servicio')
        username = request.user.username

        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM citas WHERE cliente_nombre = %s AND tipo_servicio = %s AND username = %s",
                               [cliente_nombre, tipo_servicio, username])
            messages.success(request, 'La cita ha sido eliminada correctamente.')
        except Exception as e:
            print("Error al eliminar la cita:", e)
            messages.error(request, 'Ocurrió un error al eliminar la cita.')

    return redirect('empleado')