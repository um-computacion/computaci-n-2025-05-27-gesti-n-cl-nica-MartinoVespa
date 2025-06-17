import unittest
from src.modelo.paciente import Paciente
from src.modelo.medico import Medico
from src.modelo.receta import Receta
from src.excepciones import DatosInvalidosException


class TestReceta(unittest.TestCase):

    def setUp(self):
        self.paciente = Paciente("Juan Cruz", "12345678", "03/02/1980")
        self.medico = Medico("Dr. Juan García", "M12345")
        self.medicamentos = ["Paracetamol 500mg", "Ibuprofeno 400mg"]
        self.indicaciones = "Tomar 1 comprimido cada 7 horas"

    def test_crear_receta_valida(self):
        receta = Receta(
            self.paciente,
            self.medico,
            "15/07/2025",
            self.medicamentos,
            self.indicaciones,
        )

        self.assertEqual(receta.obtener_paciente().obtener_dni(), "12345678")
        self.assertEqual(receta.obtener_medico().obtener_matricula(), "M12345")
        self.assertEqual(receta.obtener_fecha(), "15/07/2025")
        self.assertEqual(receta.obtener_medicamentos(), self.medicamentos)
        self.assertEqual(receta.obtener_indicaciones(), self.indicaciones)

    def test_crear_receta_sin_paciente(self):
        with self.assertRaises(DatosInvalidosException):
            Receta(
                None, self.medico, "15/07/2025", self.medicamentos, self.indicaciones
            )

        with self.assertRaises(DatosInvalidosException):
            Receta(
                "No es paciente",
                self.medico,
                "15/07/2025",
                self.medicamentos,
                self.indicaciones,
            )

    def test_crear_receta_sin_medico(self):
        with self.assertRaises(DatosInvalidosException):
            Receta(
                self.paciente, None, "15/07/2025", self.medicamentos, self.indicaciones
            )

        with self.assertRaises(DatosInvalidosException):
            Receta(
                self.paciente,
                "No es médico",
                "15/07/2025",
                self.medicamentos,
                self.indicaciones,
            )

    def test_crear_receta_fecha_invalida(self):
        with self.assertRaises(DatosInvalidosException):
            Receta(self.paciente, self.medico, "", self.medicamentos, self.indicaciones)

        with self.assertRaises(DatosInvalidosException):
            Receta(
                self.paciente,
                self.medico,
                "2025-07-15",
                self.medicamentos,
                self.indicaciones,
            )

        with self.assertRaises(DatosInvalidosException):
            Receta(
                self.paciente,
                self.medico,
                "32/07/2025",
                self.medicamentos,
                self.indicaciones,
            )

    def test_crear_receta_sin_medicamentos(self):
        with self.assertRaises(DatosInvalidosException):
            Receta(self.paciente, self.medico, "15/07/2025", [], self.indicaciones)

        with self.assertRaises(DatosInvalidosException):
            Receta(self.paciente, self.medico, "15/07/2025", None, self.indicaciones)

    def test_crear_receta_medicamentos_invalidos(self):
        with self.assertRaises(DatosInvalidosException):
            Receta(
                self.paciente,
                self.medico,
                "15/07/2025",
                "Paracetamol",
                self.indicaciones,
            )

        with self.assertRaises(DatosInvalidosException):
            Receta(
                self.paciente,
                self.medico,
                "15/07/2025",
                ["", "Ibuprofeno"],
                self.indicaciones,
            )

        with self.assertRaises(DatosInvalidosException):
            Receta(
                self.paciente,
                self.medico,
                "15/07/2025",
                [None, "Ibuprofeno"],
                self.indicaciones,
            )

    def test_crear_receta_sin_indicaciones(self):
        with self.assertRaises(DatosInvalidosException):
            Receta(self.paciente, self.medico, "15/07/2025", self.medicamentos, "")

        with self.assertRaises(DatosInvalidosException):
            Receta(self.paciente, self.medico, "15/07/2025", self.medicamentos, None)

    def test_obtener_medicamentos_copia(self):
        receta = Receta(
            self.paciente,
            self.medico,
            "15/07/2025",
            self.medicamentos,
            self.indicaciones,
        )

        medicamentos_obtenidos = receta.obtener_medicamentos()
        medicamentos_obtenidos.append("Aspirina")

        self.assertEqual(len(receta.obtener_medicamentos()), 2)
        self.assertNotIn("Aspirina", receta.obtener_medicamentos())

    def test_receta_con_un_medicamento(self):
        receta = Receta(
            self.paciente,
            self.medico,
            "15/07/2025",
            ["Paracetamol 500mg"],
            self.indicaciones,
        )

        medicamentos = receta.obtener_medicamentos()
        self.assertEqual(len(medicamentos), 1)
        self.assertEqual(medicamentos[0], "Paracetamol 500mg")

    def test_receta_con_multiples_medicamentos(self):
        medicamentos_multiples = [
            "Paracetamol 500mg",
            "Ibuprofeno 400mg",
            "Vitamina C",
            "Omega 3",
        ]
        receta = Receta(
            self.paciente,
            self.medico,
            "15/07/2025",
            medicamentos_multiples,
            self.indicaciones,
        )

        medicamentos = receta.obtener_medicamentos()
        self.assertEqual(len(medicamentos), 4)
        self.assertIn("Vitamina C", medicamentos)
        self.assertIn("Omega 3", medicamentos)

    def test_representacion_receta(self):
        receta = Receta(
            self.paciente,
            self.medico,
            "15/07/2025",
            self.medicamentos,
            self.indicaciones,
        )
        representacion = str(receta)

        self.assertIn("15/07/2025", representacion)
        self.assertIn("Juan Cruz", representacion)
        self.assertIn("12345678", representacion)
        self.assertIn("Dr. Juan García", representacion)
        self.assertIn("Paracetamol 500mg", representacion)
        self.assertIn("Ibuprofeno 400mg", representacion)


if __name__ == "__main__":
    unittest.main()