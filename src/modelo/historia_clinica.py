from ..excepciones import DatosInvalidosException
from .paciente import Paciente
from .turno import Turno
from .receta import Receta


class HistoriaClinica:
    def __init__(self, paciente: Paciente):

        if not isinstance(paciente, Paciente):
            raise DatosInvalidosException("Se requiere un objeto Paciente válido")

        self.__paciente__ = paciente
        self.__turnos__ = []
        self.__recetas__ = []

    def agregar_turno(self, turno: Turno):

        if not isinstance(turno, Turno):
            raise DatosInvalidosException("Se requiere un objeto Turno válido")

        if turno.obtener_paciente().obtener_dni() != self.__paciente__.obtener_dni():
            raise DatosInvalidosException("El turno no corresponde a este paciente")

        self.__turnos__.append(turno)

    def agregar_receta(self, receta: Receta):

        if not isinstance(receta, Receta):
            raise DatosInvalidosException("Se requiere un objeto Receta válido")

        if receta.obtener_paciente().obtener_dni() != self.__paciente__.obtener_dni():
            raise DatosInvalidosException("La receta no corresponde a este paciente")

        self.__recetas__.append(receta)

    def obtener_paciente(self) -> Paciente:
        return self.__paciente__

    def obtener_turnos(self) -> list[Turno]:
        return self.__turnos__.copy()

    def obtener_recetas(self) -> list[Receta]:
        return self.__recetas__.copy()

    def __str__(self) -> str:
        return (
            f"Historia Clínica - Paciente: {self.__paciente__.obtener_nombre()} "
            f"(DNI: {self.__paciente__.obtener_dni()}) - "
            f"{len(self.__turnos__)} turnos, {len(self.__recetas__)} recetas"
        )