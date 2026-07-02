# Módulo de Clases - Desarrollo Exclusivo Kenier Pérez
import logging

registrar_log = logging.getLogger("ModuloAuditoriaFJ")

class ErrorFalloIdentidad(Exception): pass
class ErrorContratoInvalido(Exception): pass

class RegistroUsuarioFJ:
    def __init__(self, codigo_id, nombre_completo, correo_contacto):
        if not codigo_id or int(codigo_id) <= 0:
            raise ErrorFalloIdentidad("Control de Calidad: El código numérico debe ser positivo.")
        if "@" not in correo_contacto or "." not in correo_contacto:
            raise ErrorFalloIdentidad("Control de Calidad: Dirección de correo electrónico errónea.")
        self.codigo = codigo_id
        self.nombre = nombre_completo
        self.correo = correo_contacto

class AgendamientoServicio:
    def __init__(self, categoria, horas_solicitadas):
        if horas_solicitadas <= 0:
            raise ErrorContratoInvalido("Alerta Reserva: El tiempo debe superar las cero horas.")
        catalogo_unad = ["sala_reunion", "dispositivos", "consultoria"]
        if categoria not in catalogo_unad:
            raise ErrorContratoInvalido("Alerta Reserva: El catálogo FJ no cubre este servicio.")
        self.categoria = categoria
        self.tiempo = horas_solicitadas
