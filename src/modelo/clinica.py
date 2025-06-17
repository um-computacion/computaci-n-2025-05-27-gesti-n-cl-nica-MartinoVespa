from ..excepciones import (
    DatosInvalidosException,
    PacienteNoEncontradoException,
    MedicoNoEncontradoException,
    TurnoOcupadoException,
)
from .paciente import Paciente
from .medico import Medico
from .especialidad import Especialidad
from .turno import Turno
from .receta import Receta
from .historia_clinica import HistoriaClinica


class Clinica:

    def __init__(self):
        self.__pacientes__ = {}
        self.__medicos__ = {}
        self.__turnos__ = []
        self.__historias_clinicas__ = {}

    def registrar_paciente(
        self, nombre: str, dni: str, fecha_nacimiento: str
    ) -> Paciente:

        if dni in self.__pacientes__:
            raise DatosInvalidosException(f"Ya existe un paciente con DNI {dni}")

        paciente = Paciente(nombre, dni, fecha_nacimiento)
        self.__pacientes__[dni] = paciente

        self.__historias_clinicas__[dni] = HistoriaClinica(paciente)

        return paciente

    def registrar_medico(self, nombre: str, matricula: str) -> Medico:

        if matricula in self.__medicos__:
            raise DatosInvalidosException(
                f"Ya existe un médico con matrícula {matricula}"
            )

        medico = Medico(nombre, matricula)
        self.__medicos__[matricula] = medico

        return medico

    def agregar_especialidad_a_medico(
        self, matricula: str, tipo_especialidad: str, dias: list[str]
    ) -> Especialidad:

        if matricula not in self.__medicos__:
            raise MedicoNoEncontradoException(
                f"No existe un médico con matrícula {matricula}"
            )

        especialidad = Especialidad(tipo_especialidad, dias)

        self.__medicos__[matricula].agregar_especialidad(especialidad)

        return especialidad

    def agendar_turno(
        self,
        dni_paciente: str,
        matricula_medico: str,
        fecha: str,
        hora: str,
        especialidad: str,
    ) -> Turno:

        if dni_paciente not in self.__pacientes__:
            raise PacienteNoEncontradoException(
                f"No existe un paciente con DNI {dni_paciente}"
            )
        if matricula_medico not in self.__medicos__:
            raise MedicoNoEncontradoException(
                f"No existe un médico con matrícula {matricula_medico}"
            )

        for turno in self.__turnos__:
            if (
                turno.obtener_medico().obtener_matricula() == matricula_medico
                and turno.obtener_fecha() == fecha
                and turno.obtener_hora() == hora
                and turno.obtener_estado() != "Cancelado"
            ):
                raise TurnoOcupadoException(
                    f"El médico ya tiene un turno en {fecha} a las {hora}"
                )

        turno = Turno(
            self.__pacientes__[dni_paciente],
            self.__medicos__[matricula_medico],
            fecha,
            hora,
            especialidad,
        )

        self.__turnos__.append(turno)

        self.__historias_clinicas__[dni_paciente].agregar_turno(turno)

        return turno

    def emitir_receta(
        self,
        dni_paciente: str,
        matricula_medico: str,
        fecha: str,
        medicamentos: list[str],
        indicaciones: str,
    ) -> Receta:

        if dni_paciente not in self.__pacientes__:
            raise PacienteNoEncontradoException(
                f"No existe un paciente con DNI {dni_paciente}"
            )
        if matricula_medico not in self.__medicos__:
            raise MedicoNoEncontradoException(
                f"No existe un médico con matrícula {matricula_medico}"
            )

        receta = Receta(
            self.__pacientes__[dni_paciente],
            self.__medicos__[matricula_medico],
            fecha,
            medicamentos,
            indicaciones,
        )

        self.__historias_clinicas__[dni_paciente].agregar_receta(receta)

        return receta

    def obtener_historia_clinica(self, dni_paciente: str) -> HistoriaClinica:

        if dni_paciente not in self.__historias_clinicas__:
            raise PacienteNoEncontradoException(
                f"No existe historia clínica para el DNI {dni_paciente}"
            )

        return self.__historias_clinicas__[dni_paciente]

    def listar_pacientes(self) -> list[Paciente]:
        return list(self.__pacientes__.values())

    def listar_medicos(self) -> list[Medico]:
        return list(self.__medicos__.values())

    def buscar_paciente(self, dni: str) -> Paciente:
        if dni not in self.__pacientes__:
            raise PacienteNoEncontradoException(f"No existe un paciente con DNI {dni}")
        return self.__pacientes__[dni]

    def buscar_medico(self, matricula: str) -> Medico:
        if matricula not in self.__medicos__:
            raise MedicoNoEncontradoException(
                f"No existe un médico con matrícula {matricula}"
            )
        return self.__medicos__[matricula]