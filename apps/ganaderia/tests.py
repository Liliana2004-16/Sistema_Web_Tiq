from django.test import TestCase
from django.utils import timezone
from apps.finca.models import Finca
from apps.users.models import User
from .models import Animal
from .services import AnimalService
from django.core.exceptions import ValidationError

class AnimalTestCase(TestCase):
    def setUp(self):
        self.finca = Finca.objects.create(nombre="Finca Test", direccion="Calle 1")
        self.user = User.objects.create_user(username='test', password='pass', cedula='123')
        self.animal = Animal.objects.create(numero_arete='A001', nombre='Luna', sexo='F', finca=self.finca)

    def test_registrar_pesaje_ok(self):
        pesaje = AnimalService.registrar_pesaje('A001', fecha=timezone.now().date(), peso=120.5, finca=self.finca, usuario=self.user)
        self.assertIsNotNone(pesaje.id)

    def test_registrar_parto_madre_no_existe(self):
        with self.assertRaises(ValidationError):
            AnimalService.registrar_parto(fecha_nac=timezone.now().date(), numero_arete_madre='NO', numero_arete_cria='C001', nombre_cria='Cria', finca=self.finca, raza='Holstein', sexo='F')


