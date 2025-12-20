
#Clase en Python
class Person:
    def __init__(self, name, age): #constructor en Python
        self.name = name
        self.age = age

    def work(self):
        return f"{self.name}" + " que tiene " + f"{self.age}" + " anios, esta estudiando Python"


person1 = Person("Alessandro",41)
person2= Person("Elena",45)

print(person1) # accede a la posicion de memoria
print(person2)


print(person1.name) #Accede al atributo
print(person2.name)

print(person1.work())
