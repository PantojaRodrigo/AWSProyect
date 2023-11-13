from api.models.alumno import Alumno
from api.models.profesor import Profesor


class Repository():
    elementos = []
          
    def add_element(self,element:Alumno|Profesor):
        if self.get_element_by_id(element.id) is None: 
            self.elementos.append(element)
            return element.id
        return None
        
    def get_element_by_id(self, id:int)->(Alumno|Profesor|None):
        return next(filter(lambda element: element.id == id,  self.elementos), None)
    
    def update_element(self,id:int,new_element:Alumno|Profesor):
        element = self.get_element_by_id(id) 
        if element is not None and element.id==new_element.id:
            self.elementos.remove(element)
            self.elementos.append(new_element)
            return new_element.id 
        return None
    
    def delete_element(self,id:int):
        element = self.get_element_by_id(id) 
        if element is not None :
            self.elementos.remove(element)
            return True
        return False
