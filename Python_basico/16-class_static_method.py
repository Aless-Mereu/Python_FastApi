class Person:
    species = "Humano"  # Atributo de clase

    def __init__(self,name,age):
        self.name = name
        self.age = age

    def change_species(self, new_species):#cambia el atributo de clase solo para el objeto actual
        self.species = new_species    

    @classmethod #cambia el atributo de clase para todos los objetos
    def change_species(cls, new_species):
        cls.species = new_species

    @staticmethod
    def is_older(age1):
        return age1 >= 18

person1 = Person("Alessandro",41)
person2= Person("Elena",45)

print(person1.species)  # Accede al atributo de clase
print(person2.species)  # Accede al atributo de clase

person1.change_species("Mutante")
print(person1.species)  # Accede al atributo de clase modificado por el objeto person1

Person.change_species("Cyborg")
print(person1.species)  # Accede al atributo de clase modificado por el método
print(person2.species)  # Accede al atributo de clase modificado por el método

print (Person.is_older(20))

print (person1.is_older(15))
print (person2.is_older(30))