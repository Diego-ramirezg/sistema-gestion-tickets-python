import json
import os
from datetime import datetime
ARCHIVO_BD = "base_datos/tickets.json"
#--- lista de opciones ---
lista_requerimientos = ['instalacion de software', 'nuevo acceso', 'configuracion de correo', 'solicitud de hardware'] 
lista_incidencias = ['software', 'hardware', 'impresora', 'red', 'accesos']
lista_prioridades = ['Alta', 'Media', 'Baja']
#--- estructura de datos y contadores ---
tickets = []
contador_inc = 0
contador_req = 0
#--- funcion cargar datos ---
def cargar_datos():
    global tickets, contador_inc, contador_req
    if os.path.exists(ARCHIVO_BD):
        try:
            with open(ARCHIVO_BD, "r", encoding='utf-8') as file:
                datos = json.load(file)
                tickets = datos.get('tickets', [])
                contador_req = datos.get('contador_req',1)
                contador_inc = datos.get('contador_inc',1)
                print("[SISTEMA] Base de datos cargada correctamente")
        except json.JSONDecodeError:
            print(f"[AVISO] El archivo {ARCHIVO_BD} está dañado.")
            tickets, contador_req, contador_inc = [], 0, 0
        except Exception as e:
            print(f"[ERROR INESPERADO] {e}")
            tickets = []
    else:
        print("[SISTEMA] No se detecto base de datos previa. Creando sistema")
        tickets, contador_inc, contador_req = [], 0,0
#--- funcion guardar datos ---
def guardar_datos():
    try:
        datos_a_guardar = {
            "contador_inc": contador_inc,
            "contador_req": contador_req,
            "tickets": tickets
        }
        with open(ARCHIVO_BD, "w", encoding='utf-8') as file:
            json.dump(datos_a_guardar, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"[ERROR] No se pudo guardar la información: {e}")

def crear_ticket(usuario, tipo_ticket, categoria, motivo, prioridad):
    global contador_inc, contador_req
    if tipo_ticket == "Incidente":
        codigo = f"INC-{contador_inc:04}"
        contador_inc += 1
    else:
        codigo = f"QER-{contador_req:04}"
        contador_req += 1

    fecha_formateada = datetime.now().strftime("%d/%m/%Y %H:%M")
    nuevo_ticket = {
        "id": codigo,
        "tipo_ticket": tipo_ticket,
        "detalle": motivo,
        "categoria": categoria,
        "fecha": fecha_formateada,
        "estado": "Pendiente",
        "prioridad": prioridad,
        "usuario": usuario
    }
    tickets.append(nuevo_ticket)
    guardar_datos()
    return nuevo_ticket

def obtener_tickets():
    return tickets

def actualizar_estado(id_ticket, nuevo_estado):
    for t in tickets:
        if t['id'].upper() == id_ticket.upper():
            t['estado'] = nuevo_estado
            guardar_datos()
            return True
    return False

def eliminar_ticket_por_id(id_ticket):
    global tickets
    largo_inicial = len(tickets)
    tickets = [t for t in tickets if t['id'].upper() != id_ticket.upper()]
    if len(tickets) < largo_inicial:
        guardar_datos()
        return True
    return False
