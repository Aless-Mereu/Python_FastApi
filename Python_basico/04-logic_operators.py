#and todo tienes que ser verdadero
age = 25
licensed = False

if age >= 18 and licensed:
    print("Puedes manejar")
else:
    print("No puedes manejar, pendejo")

#or con que solo uno sea verdadero es true
is_student = False
membership = False

if is_student or membership:
    print("Obtiene precio especial")
else:
    print("PAGA PUTASO")

#not
is_admin = True

if not is_admin:
    print("Acceso denegado")
else:
    print("Acceso concedido")

#Short Circuiting
name = False
print(name and name.upper()) #todo lo hace false5