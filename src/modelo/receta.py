from datetime import datetime
from ..excepciones import DatosInvalidosException
from .paciente import Paciente
from .medico import Medico


class Receta:
    def __init__(
        self,
        paciente: Paciente,
        medico: Medico,
        fecha: str,
        medicamentos: list[str],
        indicaciones: str,
    ):

        if not isinstance(paciente, Paciente):
            raise DatosInvalidosException("Se requiere un objeto Paciente válido")
        if not isinstance(medico, Medico):
            raise DatosInvalidosException("Se requiere un objeto Médico válido")
        if not fecha or not isinstance(fecha, str):
            raise DatosInvalidosException("La fecha es requerida y debe ser texto")
        if not isinstance(medicamentos, list) or not medicamentos:
            raise DatosInvalidosException("Debe proporcionar al menos un medicamento")
        if not indicaciones or not isinstance(indicaciones, str):
            raise DatosInvalidosException(
                "Las indicaciones son requeridas y deben ser texto"
            )

        try:
            datetime.strptime(fecha, "%d/%m/%Y")
        except ValueError:
            raise DatosInvalidosException(
                f"Formato de fecha inválido: {fecha}. Use dd/mm/aaaa"
            )

        for medicamento in medicamentos:
            if not medicamento or not isinstance(medicamento, str):
                raise DatosInvalidosException(
                    "Todos los medicamentos deben ser texto válido"
                )

        self.__paciente__ = paciente
        self.__medico__ = medico
        self.__fecha__ = fecha
        self.__medicamentos__ = medicamentos.copy()
        self.__indicaciones__ = indicaciones

    def obtener_paciente(self) -> Paciente:
        return self.__paciente__

    def obtener_medico(self) -> Medico:
        return self.__medico__

    def obtener_fecha(self) -> str:
        return self.__fecha__

    def obtener_medicamentos(self) -> list[str]:
        return self.__medicamentos__.copy()

    def obtener_indicaciones(self) -> str:
        return self.__indicaciones__

    def __str__(self) -> str:
        medicamentos_str = ", ".join(self.__medicamentos__)
        return (
            f"Receta: {self.__fecha__} - "
            f"Paciente: {self.__paciente__.obtener_nombre()} (DNI: {self.__paciente__.obtener_dni()}) - "
            f"Médico: {self.__medico__.obtener_nombre()} - "
            f"Medicamentos: {medicamentos_str}"
        )