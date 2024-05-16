from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Cita
from django.forms import DateTimeInput, TimeInput
from .models import Empleado



class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['username', 'nombre', 'apellido', 'contrasena', 'cargo', 'email', 'certificados']


class CitaForm(forms.ModelForm):
    TIPOS_SERVICIO_CHOICES = [
        ('corte_hombre', 'Corte de cabello'),
        ('afeitado', 'Afeitado de barba'),
        ('recorte_barba', 'Recorte de barba'),
        ('corte_barba', 'Corte de cabello y barba'),
        ('diseno_barba', 'Diseño de barba'),
        ('tratamiento_cuero_cabelludo', 'Tratamiento de cuero cabelludo'),
        ('peinado_especial_hombre', 'Peinado especial'),
        ('peinado', 'Peinado'),
        ('coloracion_cabello', 'Coloración de cabello'),
        ('alisado_rizado', 'Alisado/Rizado de cabello'),
        ('maquillaje', 'Maquillaje'),
        ('mnicaura_pedicura', 'Manicura y pedicura'),
        ('depilacion_facial', 'Depilación facial'),
        ('tratamiento_facial', 'Tratamiento facial'),
        ('masaje_relajante', 'Masaje relajante'),
    ]
    tipo_servicio = forms.ChoiceField(choices=TIPOS_SERVICIO_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = Cita
        fields = ['cliente_nombre', 'fecha', 'hora', 'tipo_servicio']
        widgets = {
            'fecha': DateTimeInput(attrs={'type': 'date'}),
            'hora': TimeInput(attrs={'type': 'time'})
        }

    def __init__(self, *args, **kwargs):
        super(CitaForm, self).__init__(*args, **kwargs)
        self.fields['cliente_nombre'].widget.attrs.update({'class': 'form-control'})



class CustomUserCreationForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
	def clean_email(self):
		email = self.cleaned_data['email']

		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('Este correo electrónico ya está registrado')
		return email
	
class ServicioForm(forms.Form):
    TIPOS_SERVICIO_CHOICES = [
        ('corte_hombre', 'Corte de cabello '),
        ('afeitado', 'Afeitado de barba'),
        ('recorte_barba', 'Recorte de barba'),
        ('corte_barba', 'Corte de cabello y barba'),
        ('diseno_barba', 'Diseño de barba'),
        ('masaje_capilar', 'Masaje capilar '),
        ('tratamiento_cuero_cabelludo', 'Tratamiento de cuero cabelludo '),
        ('peinado_especial_hombre', 'Peinado especial '),
        ('peinado', 'Peinado '),
        ('coloracion_cabello', 'Coloración de cabello'),
        ('alisado_rizado', 'Alisado/Rizado de cabello'),
        ('maquillaje', 'Maquillaje'),
        ('manicura_pedicura', 'Manicura y pedicura'),
        ('depilacion_facial', 'Depilación facial'),
        ('tratamiento_facial', 'Tratamiento facial'),
        ('masaje_relajante', 'Masaje relajante'),
    ]
    tipo_servicio = forms.ChoiceField(choices=TIPOS_SERVICIO_CHOICES)
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    hora = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    PRODUCTOS_CHOICES = [
        ('gel', 'Gel'),
        ('pomada', 'Pomada'),
        ('shampoo', 'Shampoo'),
        ('acondicionador', 'Acondicionador'),
        ('aceite_barba', 'Aceite para barba'),
        ('locion_aftershave', 'Loción aftershave'),
        ('serum_capilar', 'Serum capilar'),
        ('espuma_afeitar', 'Espuma de afeitar'),
        ('crema_hidratante', 'Crema hidratante'),
        ('mascarilla_capilar', 'Mascarilla capilar'),
        ('crema_peinar', 'Crema para peinar'),
        ('aceite_hidratante', 'Aceite hidratante'),
        ('laca_cabello', 'Laca para cabello'),
        ('gel_fijador', 'Gel fijador'),
        ('tinte_cabello', 'Tinte para cabello'),
        ('spray_brillo', 'Spray de brillo'),
        ('mousse_capilar', 'Mousse capilar'),
        ('cera_modelado', 'Cera para modelado'),
        ('suavizante_cabello', 'Suavizante para cabello'),
        ('crema_definir_rizos', 'Crema para definir rizos'),
    ]
    productos = forms.MultipleChoiceField(choices=PRODUCTOS_CHOICES, widget=forms.SelectMultiple)
    cantidad_producto = forms.IntegerField(min_value=1)