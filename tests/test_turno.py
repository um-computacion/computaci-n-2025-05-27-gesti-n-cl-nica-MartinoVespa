import unittest
from src.modelo.paciente import Paciente
from src.modelo.medico import Medico
from src.modelo.especialidad import Especialidad
from src.modelo.turno import Turno
from src.excepciones import (
    DatosInvalidosException,
    MedicoNoDisponibleException,
    EspecialidadInvalidaException,
)


class TestTurno(unittest.TestCase):

    def setUp(self):
        self.paciente = Paciente("Juan Cruz", "12345678", "03/02/1980")
        self.medico = Medico("Dr. Juan García", "M12345")
        self.especialidad = Especialidad("Pediatría", ["lunes", "miércoles", "viernes"])
        self.medico.agregar_especialidad(self.especialidad)

    def test_crear_turno_valido(self):
        turno = Turno(self.paciente, self.medico, "16/07/2025", "10:30", "Pediatría")

        self.assertEqual(turno.obtener_paciente().obtener_dni(), "12345678")
        self.assertEqual(turno.obtener_medico().obtener_matricula(), "M12345")
        self.assertEqual(turno.obtener_fecha(), "16/07/2025")
        self.assertEqual(turno.obtener_hora(), "10:30")
        self.assertEqual(turno.obtener_especialidad(), "Pediatría")
        self.assertEqual(turno.obtener_estado(), "Programado")

    def test_crear_turno_sin_paciente(self):
        with self.assertRaises(DatosInvalidosException):
            Turno(None, self.medico, "16/07/2025", "10:30", "Pediatría")

        with self.assertRaises(DatosInvalidosException):
            Turno("No es paciente", self.medico, "16/07/2025", "10:30", "Pediatría")

    def test_crear_turno_sin_medico(self):
        with self.assertRaises(DatosInvalidosException):
            Turno(self.paciente, None, "16/07/2025", "10:30", "Pediatría")

        with self.assertRaises(DatosInvalidosException):
            Turno(self.paciente, "No es médico", "16/07/2025", "10:30", "Pediatría")

    def test_crear_turno_fecha_invalida(self):
        with self.assertRaises(DatosInvalidosException):
            Turno(self.paciente, self.medico, "", "10:30", "Pediatría")

        with self.assertRaises(DatosInvalidosException):
            Turno(self.paciente, self.medico, "2025-07-16", "10:30", "Pediatría")

        with self.assertRaises(DatosInvalidosException):
            Turno(self.paciente, self.medico, "32/07/2025", "10:30", "Pediatría")

    def test_crear_turno_hora_invalida(self):
        with self.assertRaises(DatosInvalidosException):
            Turno(self.paciente, self.medico, "16/07/2025", "", "Pediatría")

        with self.assertRaises(DatosInvalidosException):
            Turno(self.paciente, self.medico, "16/07/2025", "25:30", "Pediatría")

        with self.assertRaises(DatosInvalidosException):
            Turno(self.paciente, self.medico, "16/07/2025", "10:70", "Pediatría")

    def test_crear_turno_medico_no_disponible_dia(self):
        with self.assertRaises(MedicoNoDisponibleException):
            Turno(self.paciente, self.medico, "17/07/2025", "10:30", "Pediatría")

    def test_crear_turno_especialidad_incorrecta(self):
        with self.assertRaises(EspecialidadInvalidaException):
            Turno(self.paciente, self.medico, "16/07/2025", "10:30", "Cardiología")

    def test_crear_turno_especialidad_vacia(self):
        with self.assertRaises(DatosInvalidosException):
            Turno(self.paciente, self.medico, "16/07/2025", "10:30", "")

        with self.assertRaises(DatosInvalidosException):
            Turno(self.paciente, self.medico, "16/07/2025", "10:30", None)

    def test_marcar_turno_completado(self):
        turno = Turno(self.paciente, self.medico, "16/07/2025", "10:30", "Pediatría")
        turno.marcar_completado()
        self.assertEqual(turno.obtener_estado(), "Completado")

    def test_marcar_turno_cancelado(self):
        turno = Turno(self.paciente, self.medico, "16/07/2025", "10:30", "Pediatría")
        turno.marcar_cancelado()
        self.assertEqual(turno.obtener_estado(), "Cancelado")

    def test_representacion_turno(self):
        turno = Turno(self.paciente, self.medico, "16/07/2025", "10:30", "Pediatría")
        representacion = str(turno)

        self.assertIn("16/07/2025", representacion)
        self.assertIn("10:30", representacion)
        self.assertIn("Juan Cruz", representacion)
        self.assertIn("12345678", representacion)
        self.assertIn("Dr. Juan García", representacion)
        self.assertIn("Pediatría", representacion)
        self.assertIn("Programado", representacion)


if __name__ == "__main__":
    unittest.main()