#Las listas son flexibles

list_number = [1, 2, 3, 4, 5]
list_letters = ['a', 'b', 'c']
list_mixed = [1, 'a', True, [1,2,3], 5.5]

shopping_cart = ["Laptop", "silla Gamer","Cafe"]

print(type(list_mixed))

#Metodos

#Aniadir a una lista con append
print(list_mixed)
list_mixed.append("Pantalla")
print(list_mixed)

#Eliminar un elemento de una lista
print(list_number)
list_number.remove(2) #elimina el numero 2
print(list_number)

#Count
print(list_number.count(2))
print(list_number.count(4))

#Mas metodos
# .copy()
# .sort()