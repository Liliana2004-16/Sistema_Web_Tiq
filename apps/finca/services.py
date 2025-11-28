from django.core.exceptions import ValidationError
from .repositories import FincaRepository

class FincaService:
    
    def __init__(self):
        self.repo = FincaRepository()

    def listar_fincas(self):
        return self.repo.get_all()

    def crear_finca(self, data):
        finca = self.repo.create(data)
        finca.full_clean()
        finca.save()
        return finca

    def actualizar_finca(self, finca_id, data):
        finca = self.repo.get_by_id(finca_id)
        if not finca:
            raise ValidationError("La finca no existe.")
        finca = self.repo.update(finca, data)
        finca.full_clean()
        finca.save()
        return finca

    def eliminar_finca(self, finca_id):
        finca = self.repo.get_by_id(finca_id)
        if not finca:
            raise ValidationError("La finca no existe.")
        self.repo.delete(finca)
