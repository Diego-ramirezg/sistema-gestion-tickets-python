#lista de usuarios administradores
import hashlib
#--- seguridad de contraseña ---
def encriptar_contraseña(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()
#--- acceso al sistema ---
usuarios_seguros = {
    "admin": encriptar_contraseña("demo123"),
    "administrador": encriptar_contraseña("demo123"),
    "administradores": encriptar_contraseña("demo123")
}
#--- login ---
def login():
    intentos = 3
    while intentos > 0:
        usuario = input("Ingrese su usuario: ").strip()
        contraseña = input("Ingrese su contraseña: ").strip()
        #encriptacion
        contraseña_encriptada = encriptar_contraseña(contraseña)
        if usuario in usuarios_seguros and usuarios_seguros[usuario] == contraseña_encriptada:
            print(f"Bienvenido al sistema {usuario}")
            return usuario
        else:
            intentos -= 1
            print("Credenciales invalidas")
    print("Usuario bloqueado")
    return None