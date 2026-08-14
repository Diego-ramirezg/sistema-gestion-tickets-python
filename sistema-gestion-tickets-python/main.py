import seguridad
import core_tickets
import interfaz

if __name__ == "__main__":
    core_tickets.cargar_datos()
    usuario_activo = seguridad.login()
    if usuario_activo:
        interfaz.menu_principal(usuario_activo)