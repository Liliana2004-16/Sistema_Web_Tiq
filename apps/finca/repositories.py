from .models import Finca

class FincaRepository:

    def get_all(self):
        return Finca.objects.all()

    def get_by_id(self, finca_id):
        return Finca.objects.filter(id=finca_id).first()

    def create(self, data):
        return Finca.objects.create(**data)

    def update(self, finca, data):
        for field, value in data.items():
            setattr(finca, field, value)
        finca.save()
        return finca

    def delete(self, finca):
        finca.delete()
