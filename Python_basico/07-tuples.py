
#Son ordenadas, indexadas e inmutables
my_tuple = (1, 2, 3, "hola",True, False, 2, "hi", 3)

print(my_tuple.count(2))
print(my_tuple.index(2)) #trae la primera posicion del valor

my_tuple[0] = 4
print(my_tuple) # al ser inmutables, no deja modificarlos

week = ('Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo') # ejemplo de conveniencia de una tupla


