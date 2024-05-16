
from django.urls import path
from .views import home, products, exit, register, servicios, crear_cita, empleado, eliminar_cita

urlpatterns = [
    path('', home, name='home'),
    path('products/', products, name='products'),
    path('logout/', exit, name='exit'),
    path('register/', register, name='register'),
    path('servicios/', servicios, name='servicios'),
    path('citas/', crear_cita, name='citas'),
    path('empleado/', empleado, name='empleado'),
    path('eliminar_cita/', eliminar_cita, name='eliminar_cita'),
]
