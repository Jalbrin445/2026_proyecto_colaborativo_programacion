import unittest
import logging

# Configuración personalizada de bitácora para Software FJ
logging.basicConfig(
    filename='bitacora_excepciones.log',
    level=logging.WARNING,
    format='%(asctime)s >> [%(levelname)s] >> %(message)s'
)
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

class ValidacionRobustezSistema(unittest.TestCase):

    def test_verificar_alta_usuario_valido(self):
        usuario = RegistroUsuarioFJ(77, "Kenier Perez Solano", "kperezso@unadvirtual.edu.co")
        self.assertEqual(usuario.codigo, 77)

    def test_detectar_correo_sin_punto(self):
        with self.assertRaises(ErrorFalloIdentidad):
            RegistroUsuarioFJ(88, "Albrin Meza", "albrin@unadvirtual")

    def test_detectar_identificador_nulo(self):
        with self.assertRaises(ErrorFalloIdentidad):
            RegistroUsuarioFJ(0, "Carlos Leal", "carlos@unad.com")

    def test_concesion_sala_correcta(self):
        reserva = AgendamientoServicio("sala_reunion", 6)
        self.assertEqual(reserva.categoria, "sala_reunion")

    def test_concesion_consultoria_correcta(self):
        reserva = AgendamientoServicio("consultoria", 1)
        self.assertEqual(reserva.tiempo, 1)

    def test_concesion_dispositivos_correcta(self):
        reserva = AgendamientoServicio("dispositivos", 24)
        self.assertEqual(reserva.tiempo, 24)

    def test_bloqueo_servicio_fantasma(self):
        with self.assertRaises(ErrorContratoInvalido):
            AgendamientoServicio("mantenimiento_tecnico", 4)

    def test_bloqueo_tiempo_incoherente(self):
        with self.assertRaises(ErrorContratoInvalido):
            AgendamientoServicio("sala_reunion", -10)

    def test_captura_omision_argumentos(self):
        with self.assertRaises(TypeError):
            RegistroUsuarioFJ()

    def test_verificar_resiliencia_ejecucion(self):
        acciones = [
            lambda: RegistroUsuarioFJ(100, "Usuario Ok", "ok@unad.co"),
            lambda: RegistroUsuarioFJ(-20, "Usuario Fallo", "fallo@unad.co")
        ]
        contador_exitos = 0
        for accion in acciones:
            try:
                accion()
                contador_exitos += 1
            except ErrorFalloIdentidad as error_captured:
                registrar_log.warning(f"Excepción controlada en auditoría: {error_captured}")
        self.assertEqual(contador_exitos, 1)

if __name__ == "__main__":
    unittest.main()
