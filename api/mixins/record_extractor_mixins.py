
from rest_framework.exceptions import NotFound

class RecordExtractor:
    def get_or_throw(self,model,id):
        try:
            record = model.objects.get(id=id)
            return record
        except model.DoesNotExist:
            raise NotFound(detial="not found")
            
        


