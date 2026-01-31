# Parametros
def hello_world(greet="Hola,", name="q ase"):
    print(f"{greet} {name}")


# Argumentos
# hello_world("Hello", "World")
# hello_world("Ciao", "Fernando")
# hello_world()
# hello_world(name="Teddy",greet="Hello")

def big_function(*args, **kwargs):
    print(args)
    print(kwargs)
    return kwargs

print(big_function(1,2,3,4,5,name="Fernando", age=25))


