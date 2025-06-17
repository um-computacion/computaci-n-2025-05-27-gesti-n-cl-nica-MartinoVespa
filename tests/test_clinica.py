import unittest
from src.modelo.clinica import Clinica
from src.excepciones import (
    DatosInvalidosException,
    PacienteNoEncontradoException,
    MedicoNoEncontradoException,
    TurnoOcupadoException,
)


class TestClinica(unittest.TestCase):

    def setUp(self):
        self.clinica = Clinica()

    def test_registrar_paciente_valido(self):
        paciente = self.clinica.registrar_paciente(
            "Juan Cruz", "12345678", "03/02/1980"
        )

        self.assertEqual(paciente.obtener_dni(), "12345678")
        self.assertEqual(paciente.obtener_nombre(), "Juan Cruz")

        historia = self.clinica.obtener_historia_clinica("12345678")
        self.assertEqual(historia.obtener_paciente().obtener_dni(), "12345678")

    def test_registrar_paciente_dni_duplicado(self):
        self.clinica.registrar_paciente("Juan Cruz", "12345678", "03/02/1980")

        with self.assertRaises(DatosInvalidosException):
            self.clinica.registrar_paciente("Martina Arias", "12345678", "15/05/1980")

    def test_registrar_medico_valido(self):
        medico = self.clinica.registrar_medico("Dr. Juan García", "M12345")

        self.assertEqual(medico.obtener_matricula(), "M12345")
        self.assertEqual(medico.obtener_nombre(), "Dr. Juan García")

    def test_registrar_medico_matricula_duplicada(self):
        self.clinica.registrar_medico("Dr. Juan García", "M12345")

        with self.assertRaises(DatosInvalidosException):
            self.clinica.registrar_medico("Dr. Lucas Gauna", "M12345")

    def test_agregar_especialidad_medico_existente(self):
        self.clinica.registrar_medico("Dr. Juan García", "M12345")

        especialidad = self.clinica.agregar_especialidad_a_medico(
            "M12345", "Pediatría", ["lunes", "miércoles", "viernes"]
        )

        self.assertEqual(especialidad.obtener_especialidad(), "Pediatría")

        medico = self.clinica.buscar_medico("M12345")
        self.assertEqual(medico.obtener_especialidad_para_dia("lunes"), "Pediatría")

    def test_agregar_especialidad_medico_inexistente(self):
        """Verifica que no se pueda agregar especialidad a médico inexistente"""
        with self.assertRaises(MedicoNoEncontradoException):
            self.clinica.agregar_especialidad_a_medico("M99999", "Pediatría", ["lunes"])

    def test_agendar_turno_valido(self):

        self.clinica.registrar_paciente("Juan Cruz", "12345678", "03/02/1980")
        self.clinica.registrar_medico("Dr. Juan García", "M12345")
        self.clinica.agregar_especialidad_a_medico(
            "M12345", "Pediatría", ["lunes", "miércoles", "viernes"]
        )

        turno = self.clinica.agendar_turno(
            "12345678", "M12345", "16/07/2025", "10:30", "Pediatría"
        )

        self.assertEqual(turno.obtener_fecha(), "16/07/2025")
        self.assertEqual(turno.obtener_hora(), "10:30")
        self.assertEqual(turno.obtener_especialidad(), "Pediatría")

        historia = self.clinica.obtener_historia_clinica("12345678")
        self.assertEqual(len(historia.obtener_turnos()), 1)

    def test_agendar_turno_paciente_inexistente(self):
        self.clinica.registrar_medico("Dr. Juan García", "M12345")

        with self.assertRaises(PacienteNoEncontradoException):
            self.clinica.agendar_turno(
                "99999999", "M12345", "16/07/2025", "10:30", "Pediatría"
            )

    def test_agendar_turno_medico_inexistente(self):
        self.clinica.registrar_paciente("Juan Cruz", "12345678", "03/02/1980")

        with self.assertRaises(MedicoNoEncontradoException):
            self.clinica.agendar_turno(
                "12345678", "M99999", "16/07/2025", "10:30", "Pediatría"
            )

    def test_agendar_turno_ocupado(self):
        self.clinica.registrar_paciente("Juan Cruz", "12345678", "02/02/1980")
        self.clinica.registrar_paciente("Martina Arias", "87654321", "15/05/1980")
        self.clinica.registrar_medico("Dr. Juan García", "M12345")
        self.clinica.agregar_especialidad_a_medico(
            "M12345", "Pediatría", ["lunes", "miércoles", "viernes"]
        )

        self.clinica.agendar_turno(
            "12345678", "M12345", "16/07/2025", "10:30", "Pediatría"
        )

        with self.assertRaises(TurnoOcupadoException):
            self.clinica.agendar_turno(
                "87654321", "M12345", "16/07/2025", "10:30", "Pediatría"
            )

    def test_emitir_receta_valida(self):
        self.clinica.registrar_paciente("Juan Cruz", "12345678", "03/02/1980")
        self.clinica.registrar_medico("Dr. Juan García", "M12345")

        receta = self.clinica.emitir_receta(
            "12345678",
            "M12345",
            "15/07/2025",
            ["Paracetamol 500mg", "Ibuprofeno 400mg"],
            "Tomar según indicaciones",
        )

        self.assertEqual(receta.obtener_fecha(), "15/07/2025")
        self.assertIn("Paracetamol 500mg", receta.obtener_medicamentos())

        historia = self.clinica.obtener_historia_clinica("12345678")
        self.assertEqual(len(historia.obtener_recetas()), 1)

    def test_emitir_receta_paciente_inexistente(self):
        self.clinica.registrar_medico("Dr. Juan García", "M12345")

        with self.assertRaises(PacienteNoEncontradoException):
            self.clinica.emitir_receta(
                "99999999",
                "M12345",
                "15/07/2025",
                ["Paracetamol 500mg"],
                "Tomar según indicaciones",
            )

    def test_emitir_receta_medico_inexistente(self):
        self.clinica.registrar_paciente("Juan Cruz", "12345678", "03/02/1980")

        with self.assertRaises(MedicoNoEncontradoException):
            self.clinica.emitir_receta(
                "12345678",
                "M99999",
                "15/07/2025",
                ["Paracetamol 500mg"],
                "Tomar según indicaciones",
            )

    def test_obtener_historia_clinica_paciente_inexistente(self):
        with self.assertRaises(PacienteNoEncontradoException):
            self.clinica.obtener_historia_clinica("99999999")

    def test_listar_pacientes(self):
        self.assertEqual(len(self.clinica.listar_pacientes()), 0)

        self.clinica.registrar_paciente("Juan Cruz", "12345678", "02/02/1980")
        self.clinica.registrar_paciente("Martina Arias", "87654321", "15/05/1980")

        pacientes = self.clinica.listar_pacientes()
        self.assertEqual(len(pacientes), 2)

        dnis = [p.obtener_dni() for p in pacientes]
        self.assertIn("12345678", dnis)
        self.assertIn("87654321", dnis)

    def test_listar_medicos(self):
        self.assertEqual(len(self.clinica.listar_medicos()), 0)

        self.clinica.registrar_medico("Dr. Juan García", "M12345")
        self.clinica.registrar_medico("Dr. Lucas Gauna", "M67890")

        medicos = self.clinica.listar_medicos()
        self.assertEqual(len(medicos), 2)

        matriculas = [m.obtener_matricula() for m in medicos]
        self.assertIn("M12345", matriculas)
        self.assertIn("M67890", matriculas)

    def test_buscar_paciente_existente(self):
        self.clinica.registrar_paciente("Juan Cruz", "12345678", "03/02/1980")

        paciente = self.clinica.buscar_paciente("12345678")
        self.assertEqual(paciente.obtener_nombre(), "Juan Cruz")

    def test_buscar_paciente_inexistente(self):
        with self.assertRaises(PacienteNoEncontradoException):
            self.clinica.buscar_paciente("99999999")

    def test_buscar_medico_existente(self):
        self.clinica.registrar_medico("Dr. Juan García", "M12345")

        medico = self.clinica.buscar_medico("M12345")
        self.assertEqual(medico.obtener_nombre(), "Dr. Juan García")

    def test_buscar_medico_inexistente(self):
        with self.assertRaises(MedicoNoEncontradoException):
            self.clinica.buscar_medico("M99999")


if __name__ == "__main__":
    unittest.main()