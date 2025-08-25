class Persona: 
    def __init__(self, nombre, apellido,dni, edad): #self es el constructor de la clase, en lugar de usar this.x se usa el self.#
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni #todo es público, no hay nada privado. No hay tanto control como en Java#
        self.edad = edad
        
    def  _str_(self):
        r = self.nombre + " "+ self.apellido
        return r
        
    
pp = Persona("Mariel", "Rodriguez","444444","22")
ft = Persona("Fulano", "de Tal","69","96")

print(pp._str_()) #aquí me muestra la cadena nombre + apellido#
print(ft.__sizeof__()) #aquí me tira la cantidad total de caracteres que tiene la persona ft#