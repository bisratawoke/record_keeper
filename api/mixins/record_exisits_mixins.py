from rest_framework.exceptions import NotFound

class RecordExisitsMixin:
    def check_if_record_exisits(self,model,id):
        if not model.objects.filter(id=id).exists():
            raise NotFound(detail=f"{model.__name__} not found")


