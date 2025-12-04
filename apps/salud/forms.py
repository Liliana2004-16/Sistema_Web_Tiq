from django import forms
from .models import EventoSanitario, Inseminacion, ConfirmacionGestacion


class EventoSanitarioForm(forms.ModelForm):
    class Meta:
        model = EventoSanitario
        fields = [
            'fecha', 'animal', 'diagnostico', 'tratamiento',
            'responsable', 'sintomas',
        ]
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }

class InseminacionForm(forms.ModelForm):
    class Meta:
        model = Inseminacion
        fields = ['fecha', 'animal', 'tipo_semen', 'inseminador']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'inseminador': forms.TextInput(attrs={'placeholder': 'Nombre del inseminador'}),
            'animal': forms.HiddenInput(),
        }

class ConfirmacionGestacionForm(forms.ModelForm):

    class Meta:
        model = ConfirmacionGestacion
        fields = [
            'fecha_confirmacion',
            'metodo_diagnostico',
            'resultado',
            'responsable',
            'observaciones'
        ]
        widgets = {
            'fecha_confirmacion': forms.DateInput(attrs={'type': 'date'}),
        }
