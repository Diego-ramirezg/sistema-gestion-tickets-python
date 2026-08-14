import core_tickets

def seleccionar_opcion(nombre_categoria, lista_opciones):
    print(f"\n----- {nombre_categoria} -----")
    for i, opcion in enumerate(lista_opciones, start=1):
        print(f"{i}.- {opcion}")
    while True:
        try:
            seleccion = int(input("Seleccione una opción: "))
            if 1 <= seleccion <= len(lista_opciones):
                return lista_opciones[seleccion - 1]
            print(f"¡Error!, seleccione un número entre 1 y {len(lista_opciones)}")
        except ValueError:
            print("Ingrese números válidos.")

def ingresar_motivo():
    while True:
        motivo = input("Ingrese motivo / detalle: ").strip().capitalize()
        if motivo:
            return motivo
        print("Debe ingresar un motivo válido.")

def flujo_crear_ticket(usuario_activo):
    print("\n--- SELECCIONE EL TIPO DE SOLICITUD ---")
    print("1.- Incidente")
    print("2.- Requerimiento")
    
    opcion = input("Elija una opción (1-2): ").strip()
    if opcion == "1":
        tipo_ticket = "Incidente"
        categoria = seleccionar_opcion("Tipo de Incidencia", core_tickets.lista_incidencias)
    elif opcion == "2":
        tipo_ticket = "Requerimiento"
        categoria = seleccionar_opcion("Tipo de Requerimiento", core_tickets.lista_requerimientos)
    else:
        print("Opción inválida.")
        return

    motivo = ingresar_motivo()
    prioridad = seleccionar_opcion("Prioridades", core_tickets.lista_prioridades)
    
    ticket = core_tickets.crear_ticket(usuario_activo, tipo_ticket, categoria, motivo, prioridad)
    mostrar_ticket(ticket)

def mostrar_ticket(ticket):
    print("\n============================================")
    print(f"       TICKET CREADO: {ticket['id']} ({ticket['tipo_ticket']})")
    print("============================================")
    print(f"Fecha:      {ticket['fecha']}")
    print(f"Usuario:    {ticket['usuario']}")
    print(f"Categoría:  {ticket['categoria'].capitalize()}")
    print(f"Prioridad:  {ticket['prioridad']}")
    print(f"Estado:     {ticket['estado']}")
    print(f"Detalle:    {ticket['detalle']}")
    print("============================================\n")

def listar_tickets():
    lista = core_tickets.obtener_tickets()
    if not lista:
        print("\nNo hay tickets registrados en el sistema.")
        return
    print("\n================ LISTADO DE TICKETS ================")
    for t in lista:
        print(f"ID: {t['id']} | Tipo: {t['tipo_ticket']} | Cat: {t['categoria']} | Estado: {t['estado']} | User: {t['usuario']}")
    print("======================================================")

def flujo_actualizar_estado():
    listar_tickets()
    if not core_tickets.obtener_tickets():
        return
    id_buscar = input("\nIngrese el ID del ticket a actualizar (Ej: INC-0001): ").strip()
    nuevo_estado = seleccionar_opcion("Nuevo estado", ["Pendiente", "En proceso", "Resuelto", "Cerrado"])
    
    if core_tickets.actualizar_estado(id_buscar, nuevo_estado):
        print(f"\n[+] ¡El ticket {id_buscar.upper()} ha sido actualizado a '{nuevo_estado}'!")
    else:
        print("\n[-] No se encontró un ticket con ese ID.")

def flujo_eliminar_ticket():
    listar_tickets()
    if not core_tickets.obtener_tickets():
        return
    id_buscar = input("\nIngrese el ID del ticket a eliminar: ").strip()
    if core_tickets.eliminar_ticket_por_id(id_buscar):
        print(f"\n[+] Ticket {id_buscar.upper()} eliminado correctamente.")
    else:
        print("\n[-] No se encontró el ticket especificado.")

def menu_principal(usuario_activo):
    while True:
        print(f"\n=== MENÚ MESA DE AYUDA (Usuario: {usuario_activo}) ===")
        print("1.- Crear nuevo ticket")
        print("2.- Listar todos los tickets")
        print("3.- Actualizar estado de un ticket")
        print("4.- Eliminar un ticket")
        print("5.- Salir")
        
        opcion = input("Seleccione una opción (1-5): ").strip()
        
        if opcion == "1":
            flujo_crear_ticket(usuario_activo)
        elif opcion == "2":
            listar_tickets()
        elif opcion == "3":
            flujo_actualizar_estado()
        elif opcion == "4":
            flujo_eliminar_ticket()
        elif opcion == "5":
            print("\nSaliendo del sistema... ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")