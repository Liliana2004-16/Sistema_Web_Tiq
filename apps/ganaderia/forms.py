# apps/ganaderia/forms.py
from django import forms
from .models import Pesaje, Parto, ProduccionLeche, EventoSalida, Animal, Traslado
from apps.finca.models import Finca
from apps.ganaderia.models import Pesaje 


class PesajeForm(forms.Form):
    numero_arete = forms.CharField(
        max_length=50,
        label='Número de arete',
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese el arete'})
    )

    nombre_animal = forms.CharField(
        label="Nombre del animal",
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    finca = forms.CharField(
        label="Finca",
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    peso = forms.FloatField(
        min_value=0.01,
        label='Peso (kg)'
    )

    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    def clean(self):
        cleaned = super().clean()

        numero = cleaned.get('numero_arete')
        if not numero:
            raise forms.ValidationError("Debe ingresar un número de arete.")

        try:
            animal = Animal.objects.get_by_arete(numero)
        except Animal.DoesNotExist:
            raise forms.ValidationError("El número de arete no corresponde a ningún animal registrado.")

        cleaned["animal"] = animal
        cleaned["finca"] = animal.finca
        cleaned["nombre_animal"] = animal.nombre

        if cleaned.get("peso") and cleaned["peso"] <= 0:
            raise forms.ValidationError("El peso debe ser mayor a 0.")

        return cleaned

class PesajeEditForm(forms.ModelForm):
    class Meta:
        model = Pesaje
        fields = ['peso', 'fecha', 'finca']

        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'peso': forms.NumberInput(attrs={'step': '0.1'}),
        }


class PartoForm(forms.ModelForm):
    numero_arete_madre = forms.CharField(label="Arete de la madre")
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    numero_arete_cria = forms.CharField(label="Arete de la cría")
    nombre_cria = forms.CharField(required=False)
    sexo = forms.ChoiceField(choices=[('M','Macho'),('F','Hembra')])
    raza = forms.CharField(required=False)
    peso = forms.FloatField(required=False)
    finca = forms.ModelChoiceField(queryset=Finca.objects.all())
    class Meta:
        model = Parto
        fields = [
            'numero_arete_madre',
            'fecha_nacimiento',
            'numero_arete_cria',
            'nombre_cria',
            'sexo',
            'raza',
            'peso',
            'finca'
        ]
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'})
        }

    def clean_numero_arete_madre(self):
        numero = self.cleaned_data['numero_arete_madre']
        madre = Animal.objects.get_by_arete(numero)
        if not madre:
            raise forms.ValidationError("No existe la madre con ese número de arete")
        if madre.sexo != 'F':
            raise forms.ValidationError("La madre debe ser hembra.")
        return numero

    def clean_numero_arete_cria(self):
        numero = self.cleaned_data['numero_arete_cria']
        if Animal.objects.filter(numero_arete=numero).exists():
            raise forms.ValidationError("El número de arete de la cría ya existe")
        return numero

class ProduccionForm(forms.ModelForm):
    numero_arete = forms.CharField(label="Número de arete", max_length=50)

    class Meta:
        model = ProduccionLeche
        fields = ['fecha', 'peso_am', 'peso_pm', 'numero_arete']
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, turno=None, **kwargs):
        super().__init__(*args, **kwargs)

        if turno == "AM":
            self.fields['peso_pm'].widget = forms.HiddenInput()
            self.fields['peso_pm'].required = False

        elif turno == "PM":
            self.fields['peso_am'].widget = forms.HiddenInput()
            self.fields['peso_am'].required = False

    def clean(self):
        cleaned = super().clean()
        numero = cleaned.get("numero_arete")

        if not numero:
            raise forms.ValidationError("Debe ingresar un número de arete")

        try:
            animal = Animal.objects.get(numero_arete=numero)
        except Animal.DoesNotExist:
            raise forms.ValidationError("El número de arete ingresado no corresponde a ningún animal registrado")

        cleaned['animal'] = animal
        cleaned['finca'] = animal.finca

        return cleaned

class EventoSalidaForm(forms.ModelForm):
    numero_arete = forms.CharField(max_length=50)
    class Meta:
        model = EventoSalida
        fields = ['fecha', 'tipo_evento', 'numero_arete', 'observaciones']

    def clean(self):
        cleaned = super().clean()
        numero = cleaned.get('numero_arete')
        animal = Animal.objects.get_by_arete(numero)
        if not animal:
            raise forms.ValidationError("El número de arete ingresado no corresponde a ningún animal registrado")
        cleaned['animal'] = animal
        return cleaned

class TrasladoForm(forms.Form):
    lista_aretes = forms.CharField(widget=forms.Textarea, help_text="Ingrese aretes separados por comas")
    finca_destino = forms.ModelChoiceField(queryset=Finca.objects.all())

    def clean_lista_aretes(self):
        value = self.cleaned_data['lista_aretes']
        items = [x.strip() for x in value.split(',') if x.strip()]
        if not items:
            raise forms.ValidationError("Debe ingresar al menos un arete")
        return items
