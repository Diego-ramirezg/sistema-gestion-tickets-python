import json
import os
from datetime import datetime
"""clase que representa la unidad de tickets"""
class Ticket:
    def __init__(self,id,usuario, tipo, categoria, motivo, prioridad, fecha = None, estado= 'Pendiente' ):
        self.id = id
        self.usuario = usuario
        self.tipo = tipo
        self.estado = estado
        self.categoria = categoria
        self.motivo = motivo
        self.prioridad = prioridad
        self.fecha = fecha if fecha else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    """propiedad para transformar el objeto a un dict para json"""
    def to_dict(self):
        return{
            "id": id,
            "usuario": self.usuario,
            "tipo": self.tipo,
            "categoria": self.categoria,
            "motivo": self.motivo,
            "prioridad": self.prioridad,
            "fecha": self.fecha,
            "estado": self.estado
        }
class GestorTickets:
    def __init__(self,archivo_bd = 'base_datos/tickets.json'):
        self.archivo_bd = archivo_bd
        self.lista_requerimientos = ['instalacion de software', 'nuevo acceso', 'configuracion de correo', 'solicitud de hardware']
        self.lista_incidentes = ['software', 'hardware', 'impresora', 'red', 'accesos']
        self.prioridades = ['Alta', 'Media', 'Baja']
        self.contador_req = 1
        self.inc = 1
        #cargar los datos automaticamente
        self.cargar_datos()
    def cargar_datos(self):
        if os.path.exists(self.archivo_bd):
            try:
                with open(self.archivo_bd,"r",encoding='utf-8') as file:
                    datos = json.load(file)
                    self.tickets = [Ticket(**t) for t in datos.get('tickets,[]')]
                    self.contador_req = datos.get('contador_req',0)
                    self.contador_inc = datos.get('contador_inc',0)
                print("Datos cargados correctamente")
            except json.JSONDecodeError:
                print(f"Base de datos dañada: {self.archivo_bd}")
            except Exception as e:
                print(f"Error inesperado: {e}")
                self.tickets = []
    def guardar_datos(self):
        """serializar los objetos y guardar el estado actual"""
        try:
            os.makedirs(os.path.dirname(self.archivo_bd), exist_ok= True)
            datos_guardar = {
                "contador_inc": self.contador_inc,
                "contador_req": self.contador_req,
                "tickets" : [t.to_dict() for t in self.tickets]
            }
            with open(self.archivo_bd,"w", encoding='utf-8') as file:
                json.dump(datos_guardar, file, indent= 4, ensure_ascii= False)
                print("Información guardada con exito")
        except Exception as e:
            print("No se pudo guardar información: {e}")
    def crear_ticket(self,usuario, tipo_ticket, categoria,motivo,prioridad):
        """Genera un nuevo ticket, actualiza contadores y guarda la bd"""
        #generacion de id incremental
        if tipo_ticket.lower() == "incidencia":
            self.contador_inc += 1
            id_ticket = f"INC-{self.contador_inc:04d}"
        else:
            self.contador_req += 1
            id_ticket = f"REQ-{self.contador_req:04d}"
        #instanciar un nuevo ticket
        nuevo_ticket = Ticket(id_ticket, usuario, tipo_ticket, categoria,motivo,prioridad)
        #almacenar ticket
        self.tickets.append(nuevo_ticket)
        self.guardar_datos()
        return id_ticket