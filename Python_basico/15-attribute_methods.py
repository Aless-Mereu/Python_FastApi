
#Clase en Python
class Person:
    species = "Humano"  # Atributo de clase

    def __init__(self, name, age): #constructor en Python
        self.name = name
        self.age = age
        self._energy = 100  # Atributo protegido. Debe accederse a traves de métodos
        self.__password = "12345" # Atributo privado. No debe accederse fuera de la clase



    def work(self):
        return f"{self.name}" + " que tiene " + f"{self.age}" + " anios, esta estudiando Python"
    
    def _waste_energy(self, quantity):
        self._energy -= quantity
        return self._energy
    
    def __generate_pasword(self):
        return f"$${self.name}{self.age}$$"


person1 = Person("Alessandro",41)
person2= Person("Elena",45)

print(person1) # accede a la posicion de memoria
print(person2)


print(person1.name) #Accede al atributo
print(person2.name)

print(person1.work())
print(f"{person1.name} "  " ha gastado "  f" {person1._waste_energy(10)} "  " de energia")  # Acceso al método protegido (no recomendado fuera de la clase)

print(person2._Person__password)  # Acceso al atributo privado (no recomendado fuera de la clase)

print(person1._Person__generate_pasword())  # Acceso al método privado (no recomendado fuera de la clase)