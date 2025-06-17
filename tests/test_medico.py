import unittest
from src.modelo.medico import Medico
from src.modelo.especialidad import Especialidad
from src.excepciones import DatosInvalidosException


class TestMedico(unittest.TestCase):

    def test_crear_medico_valido(self):
        medico = Medico("Dr. Lucas Gauna", "M12345")
        self.assertEqual(medico.obtener_matricula(), "M12345")
        self.assertEqual(medico.obtener_nombre(), "Dr. Lucas Gauna")

    def test_crear_medico_sin_nombre(self):
        with self.assertRaises(DatosInvalidosException):
            Medico("", "M12345")

        with self.assertRaises(DatosInvalidosException):
            Medico(None, "M12345")

    def test_crear_medico_sin_matricula(self):
        with self.assertRaises(DatosInvalidosException):
            Medico("Dr. Lucas Gauna", "")

        with self.assertRaises(DatosInvalidosException):
            Medico("Dr. Lucas Gauna", None)

    def test_tipos_datos_invalidos(self):
        with self.assertRaises(DatosInvalidosException):
            Medico(123, "M12345")

        with self.assertRaises(DatosInvalidosException):
            Medico("Dr. Lucas Gauna", 12345)

    def test_agregar_especialidad_valida(self):
        medico = Medico("Dr. Lucas Gauna", "M12345")
        especialidad = Especialidad("Pediatría", ["lunes", "miércoles", "viernes"])

        medico.agregar_especialidad(especialidad)

        self.assertEqual(medico.obtener_especialidad_para_dia("lunes"), "Pediatría")
        self.assertEqual(medico.obtener_especialidad_para_dia("miércoles"), "Pediatría")
        self.assertEqual(medico.obtener_especialidad_para_dia("viernes"), "Pediatría")

    def test_obtener_especialidad_dia_no_disponible(self):
        medico = Medico("Dr. Lucas Gauna", "M12345")
        especialidad = Especialidad("Pediatría", ["lunes", "miércoles"])
        medico.agregar_especialidad(especialidad)

        self.assertIsNone(medico.obtener_especialidad_para_dia("martes"))
        self.assertIsNone(medico.obtener_especialidad_para_dia("domingo"))

    def test_agregar_especialidad_duplicada(self):
        medico = Medico("Dr. Lucas Gauna", "M12345")
        especialidad1 = Especialidad("Pediatría", ["lunes"])
        especialidad2 = Especialidad("Pediatría", ["martes"])

        medico.agregar_especialidad(especialidad1)

        with self.assertRaises(DatosInvalidosException):
            medico.agregar_especialidad(especialidad2)

    def test_agregar_especialidad_tipo_invalido(self):
        medico = Medico("Dr. Lucas Gauna", "M12345")

        with self.assertRaises(DatosInvalidosException):
            medico.agregar_especialidad("Pediatría")

        with self.assertRaises(DatosInvalidosException):
            medico.agregar_especialidad(None)

    def test_multiples_especialidades(self):
        medico = Medico("Dr. Lucas Gauna", "M12345")
        pediatria = Especialidad("Pediatría", ["lunes", "miércoles"])
        cardiologia = Especialidad("Cardiología", ["martes", "jueves"])

        medico.agregar_especialidad(pediatria)
        medico.agregar_especialidad(cardiologia)

        self.assertEqual(medico.obtener_especialidad_para_dia("lunes"), "Pediatría")
        self.assertEqual(medico.obtener_especialidad_para_dia("martes"), "Cardiología")
        self.assertEqual(medico.obtener_especialidad_para_dia("miércoles"), "Pediatría")
        self.assertEqual(medico.obtener_especialidad_para_dia("jueves"), "Cardiología")

    def test_obtener_especialidades(self):
        medico = Medico("Dr. Lucas Gauna", "M12345")
        pediatria = Especialidad("Pediatría", ["lunes"])
        cardiologia = Especialidad("Cardiología", ["martes"])

        medico.agregar_especialidad(pediatria)
        medico.agregar_especialidad(cardiologia)

        especialidades = medico.obtener_especialidades()
        self.assertEqual(len(especialidades), 2)

        especialidades.clear()
        self.assertEqual(len(medico.obtener_especialidades()), 2)

    def test_representacion_medico_sin_especialidades(self):
        medico = Medico("Dr. Lucas Gauna", "M12345")
        representacion = str(medico)
        self.assertIn("Dr/a. Dr. Lucas Gauna", representacion)
        self.assertIn("M12345", representacion)
        self.assertIn("Sin especialidades asignadas", representacion)

    def test_representacion_medico_con_especialidades(self):
        medico = Medico("Dr. Lucas Gauna", "M12345")
        especialidad = Especialidad("Pediatría", ["lunes", "miércoles"])
        medico.agregar_especialidad(especialidad)

        representacion = str(medico)
        self.assertIn("Dr/a. Dr. Lucas Gauna", representacion)
        self.assertIn("M12345", representacion)
        self.assertIn("Pediatría", representacion)
        self.assertNotIn("Sin especialidades asignadas", representacion)


if __name__ == "__main__":
    unittest.main()