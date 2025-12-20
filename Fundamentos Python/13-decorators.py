# es una forma elegante de modificar el comportamiento sin cambiar el codigo

def require_auth(func):
    def wrapper(user):
        if user.lower() == "admin":
            return func(user)
        else:
            return "Acceso denegado"

    return wrapper
@require_auth
def admin_dashboard(user):
    return f"Bienvenido al panel {user}"

print(admin_dashboard("ADMIN"))
print(admin_dashboard("admin"))


