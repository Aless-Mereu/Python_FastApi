user = {
    "name": "Juan",
    "age": 34,
    "email": "Juan@gmail.com",
    "active": True,
    (19.12, -9.328): "Cancun Mexico"
}

#cambiar el valor de name
user["name"] = "Alessandro"
print(user)

print(user["age"])
print(user[19.12, -9.328])

#values, items , keys
print(user.items())
print(user.values())
print(user.keys())

user["country"] = "Spain"
print(user)