import unittest
from src.modelo.paciente import Paciente
from src.modelo.medico import Medico
from src.modelo.especialidad import Especialidad
from src.modelo.turno import Turno
from src.modelo.receta import Receta
from src.modelo.historia_clinica import HistoriaClinica
from src.excepciones import DatosInvalidosException


class TestHistoriaClinica(unittest.TestCase):

    def setUp(self):
        self.paciente = Paciente("Juan Cruz", "12345678", "03/02/1980")
        self.otro_paciente = Paciente("Martina Arias", "87654321", "15/05/1980")
        self.medico = Medico("Dr. Juan García", "M12345")

        especialidad = Especialidad("Pediatría", ["lunes", "miércoles", "viernes"])
        self.medico.agregar_especialidad(especialidad)

        self.historia = HistoriaClinica(self.paciente)

    def test_crear_historia_clinica_valida(self):
        historia = HistoriaClinica(self.paciente)
        self.assertEqual(historia.obtener_paciente().obtener_dni(), "12345678")
        self.assertEqual(len(historia.obtener_turnos()), 0)
        self.assertEqual(len(historia.obtener_recetas()), 0)

    def test_crear_historia_clinica_sin_paciente(self):
        with self.assertRaises(DatosInvalidosException):
            HistoriaClinica(None)

        with self.assertRaises(DatosInvalidosException):
            HistoriaClinica("No es paciente")

    def test_agregar_turno_valido(self):
        turno = Turno(self.paciente, self.medico, "16/07/2025", "10:30", "Pediatría")
        self.historia.agregar_turno(turno)

        turnos = self.historia.obtener_turnos()
        self.assertEqual(len(turnos), 1)
        self.assertEqual(turnos[0].obtener_fecha(), "16/07/2025")

    def test_agregar_turno_invalido(self):
        with self.assertRaises(DatosInvalidosException):
            self.historia.agregar_turno(None)

        with self.assertRaises(DatosInvalidosException):
            self.historia.agregar_turno("No es turno")

    def test_agregar_turno_paciente_diferente(self):
        turno_otro_paciente = Turno(
            self.otro_paciente, self.medico, "16/07/2025", "10:30", "Pediatría"
        )

        with self.assertRaises(DatosInvalidosException):
            self.historia.agregar_turno(turno_otro_paciente)

    def test_agregar_receta_valida(self):
        receta = Receta(
            self.paciente,
            self.medico,
            "15/07/2025",
            ["Paracetamol 500mg"],
            "Tomar cada 7 horas",
        )
        self.historia.agregar_receta(receta)

        recetas = self.historia.obtener_recetas()
        self.assertEqual(len(recetas), 1)
        self.assertEqual(recetas[0].obtener_fecha(), "15/07/2025")

    def test_agregar_receta_invalida(self):
        with self.assertRaises(DatosInvalidosException):
            self.historia.agregar_receta(None)

        with self.assertRaises(DatosInvalidosException):
            self.historia.agregar_receta("No es receta")

    def test_agregar_receta_paciente_diferente(self):
        receta_otro_paciente = Receta(
            self.otro_paciente,
            self.medico,
            "15/07/2025",
            ["Paracetamol 500mg"],
            "Tomar cada 7 horas",
        )

        with self.assertRaises(DatosInvalidosException):
            self.historia.agregar_receta(receta_otro_paciente)

    def test_obtener_turnos_copia(self):
        turno = Turno(self.paciente, self.medico, "16/07/2025", "10:30", "Pediatría")
        self.historia.agregar_turno(turno)

        turnos_obtenidos = self.historia.obtener_turnos()
        turnos_obtenidos.clear()

        self.assertEqual(len(self.historia.obtener_turnos()), 1)

    def test_obtener_recetas_copia(self):
        receta = Receta(
            self.paciente,
            self.medico,
            "15/07/2025",
            ["Paracetamol 500mg"],
            "Tomar cada 7 horas",
        )
        self.historia.agregar_receta(receta)

        recetas_obtenidas = self.historia.obtener_recetas()
        recetas_obtenidas.clear()

        self.assertEqual(len(self.historia.obtener_recetas()), 1)

    def test_multiples_turnos_y_recetas(self):
        turno1 = Turno(self.paciente, self.medico, "16/07/2025", "10:30", "Pediatría")
        turno2 = Turno(self.paciente, self.medico, "18/07/2025", "15:00", "Pediatría")

        self.historia.agregar_turno(turno1)
        self.historia.agregar_turno(turno2)

        receta1 = Receta(
            self.paciente,
            self.medico,
            "15/07/2025",
            ["Paracetamol 500mg"],
            "Tomar cada 7 horas",
        )
        receta2 = Receta(
            self.paciente,
            self.medico,
            "17/07/2025",
            ["Ibuprofeno 400mg"],
            "Tomar cada 12 horas",
        )

        self.historia.agregar_receta(receta1)
        self.historia.agregar_receta(receta2)

        self.assertEqual(len(self.historia.obtener_turnos()), 2)
        self.assertEqual(len(self.historia.obtener_recetas()), 2)

    def test_representacion_historia_clinica(self):
        representacion_vacia = str(self.historia)
        self.assertIn("Juan Cruz", representacion_vacia)
        self.assertIn("12345678", representacion_vacia)
        self.assertIn("0 turnos", representacion_vacia)
        self.assertIn("0 recetas", representacion_vacia)

        turno = Turno(self.paciente, self.medico, "16/07/2025", "10:30", "Pediatría")
        receta = Receta(
            self.paciente,
            self.medico,
            "15/07/2025",
            ["Paracetamol 500mg"],
            "Tomar cada 7 horas",
        )

        self.historia.agregar_turno(turno)
        self.historia.agregar_receta(receta)

        representacion_con_datos = str(self.historia)
        self.assertIn("1 turnos", representacion_con_datos)
        self.assertIn("1 recetas", representacion_con_datos)


if __name__ == "__main__":
    unittest.main()