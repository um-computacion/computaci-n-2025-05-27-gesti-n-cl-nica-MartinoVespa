import unittest
from src.modelo.especialidad import Especialidad
from src.excepciones import DatosInvalidosException


class TestEspecialidad(unittest.TestCase):

    def test_crear_especialidad_valida(self):
        especialidad = Especialidad("Pediatría", ["lunes", "miércoles", "viernes"])
        self.assertEqual(especialidad.obtener_especialidad(), "Pediatría")
        self.assertTrue(especialidad.verificar_dia("lunes"))
        self.assertTrue(especialidad.verificar_dia("miércoles"))
        self.assertTrue(especialidad.verificar_dia("viernes"))

    def test_verificar_dia_no_disponible(self):
        especialidad = Especialidad("Pediatría", ["lunes", "miércoles"])
        self.assertFalse(especialidad.verificar_dia("martes"))
        self.assertFalse(especialidad.verificar_dia("domingo"))

    def test_normalizacion_dias(self):
        especialidad = Especialidad("Pediatría", ["LUNES", "Miércoles", "viernes"])
        self.assertTrue(especialidad.verificar_dia("lunes"))
        self.assertTrue(especialidad.verificar_dia("MIÉRCOLES"))
        self.assertTrue(especialidad.verificar_dia("Viernes"))

    def test_dia_miercoles_variaciones(self):
        especialidad = Especialidad("Pediatría", ["miercoles"])
        self.assertTrue(especialidad.verificar_dia("miércoles"))
        self.assertTrue(especialidad.verificar_dia("miercoles"))

        especialidad2 = Especialidad("Pediatría", ["miércoles"])
        self.assertTrue(especialidad2.verificar_dia("miercoles"))
        self.assertTrue(especialidad2.verificar_dia("miércoles"))

    def test_dia_sabado_variaciones(self):
        especialidad = Especialidad("Pediatría", ["sabado"])
        self.assertTrue(especialidad.verificar_dia("sábado"))
        self.assertTrue(especialidad.verificar_dia("sabado"))

        especialidad2 = Especialidad("Pediatría", ["sábado"])
        self.assertTrue(especialidad2.verificar_dia("sabado"))
        self.assertTrue(especialidad2.verificar_dia("sábado"))

    def test_crear_especialidad_sin_tipo(self):
        with self.assertRaises(DatosInvalidosException):
            Especialidad("", ["lunes"])

        with self.assertRaises(DatosInvalidosException):
            Especialidad(None, ["lunes"])

    def test_crear_especialidad_sin_dias(self):
        with self.assertRaises(DatosInvalidosException):
            Especialidad("Pediatría", [])

        with self.assertRaises(DatosInvalidosException):
            Especialidad("Pediatría", None)

    def test_dia_invalido(self):
        with self.assertRaises(DatosInvalidosException):
            Especialidad("Pediatría", ["lunes", "dia_inexistente"])

    def test_tipos_datos_invalidos(self):
        with self.assertRaises(DatosInvalidosException):
            Especialidad(123, ["lunes"])

        with self.assertRaises(DatosInvalidosException):
            Especialidad("Pediatría", "lunes")

    def test_obtener_dias(self):
        dias_originales = ["lunes", "miércoles", "viernes"]
        especialidad = Especialidad("Pediatría", dias_originales)
        dias_obtenidos = especialidad.obtener_dias()

        self.assertIn("lunes", dias_obtenidos)
        self.assertIn("miércoles", dias_obtenidos)
        self.assertIn("viernes", dias_obtenidos)

        dias_obtenidos.append("domingo")
        self.assertNotIn("domingo", especialidad.obtener_dias())

    def test_representacion_especialidad(self):
        especialidad = Especialidad("Pediatría", ["lunes", "miércoles"])
        representacion = str(especialidad)
        self.assertIn("Pediatría", representacion)
        self.assertIn("lunes", representacion)
        self.assertIn("miércoles", representacion)


if __name__ == "__main__":
    unittest.main()