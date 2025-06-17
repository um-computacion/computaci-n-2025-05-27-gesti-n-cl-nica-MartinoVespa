from datetime import datetime
from ..excepciones import (
    DatosInvalidosException,
    MedicoNoDisponibleException,
    EspecialidadInvalidaException,
)
from .paciente import Paciente
from .medico import Medico


class Turno:
    def __init__(
        self,
        paciente: Paciente,
        medico: Medico,
        fecha: str,
        hora: str,
        especialidad: str,
    ):

        if not isinstance(paciente, Paciente):
            raise DatosInvalidosException("Se requiere un objeto Paciente válido")
        if not isinstance(medico, Medico):
            raise DatosInvalidosException("Se requiere un objeto Médico válido")
        if not fecha or not isinstance(fecha, str):
            raise DatosInvalidosException("La fecha es requerida y debe ser texto")
        if not hora or not isinstance(hora, str):
            raise DatosInvalidosException("La hora es requerida y debe ser texto")
        if not especialidad or not isinstance(especialidad, str):
            raise DatosInvalidosException(
                "La especialidad es requerida y debe ser texto"
            )

        try:
            fecha_obj = datetime.strptime(fecha, "%d/%m/%Y")
            dia_semana = [
                "lunes",
                "martes",
                "miércoles",
                "jueves",
                "viernes",
                "sábado",
                "domingo",
            ][fecha_obj.weekday()]

            esp_disponible = medico.obtener_especialidad_para_dia(dia_semana)
            if not esp_disponible:
                raise MedicoNoDisponibleException(
                    f"El médico no atiende los {dia_semana}"
                )
            if esp_disponible != especialidad:
                raise EspecialidadInvalidaException(
                    f"El médico atiende {esp_disponible} los {dia_semana}, no {especialidad}"
                )
        except ValueError:
            raise DatosInvalidosException(
                f"Formato de fecha inválido: {fecha}. Use dd/mm/aaaa"
            )

        try:
            datetime.strptime(hora, "%H:%M")
        except ValueError:
            raise DatosInvalidosException(
                f"Formato de hora inválido: {hora}. Use HH:MM"
            )

        self.__paciente__ = paciente
        self.__medico__ = medico
        self.__fecha__ = fecha
        self.__hora__ = hora
        self.__especialidad__ = especialidad
        self.__estado__ = "Programado"

    def obtener_paciente(self) -> Paciente:
        return self.__paciente__

    def obtener_medico(self) -> Medico:
        return self.__medico__

    def obtener_fecha(self) -> str:
        return self.__fecha__

    def obtener_hora(self) -> str:
        return self.__hora__

    def obtener_especialidad(self) -> str:
        return self.__especialidad__

    def obtener_estado(self) -> str:
        return self.__estado__

    def marcar_completado(self):
        self.__estado__ = "Completado"

    def marcar_cancelado(self):
        self.__estado__ = "Cancelado"

    def __str__(self) -> str:
        return (
            f"Turno: {self.__fecha__} a las {self.__hora__} - "
            f"Paciente: {self.__paciente__.obtener_nombre()} (DNI: {self.__paciente__.obtener_dni()}) - "
            f"Médico: {self.__medico__.obtener_nombre()} - "
            f"Especialidad: {self.__especialidad__} - Estado: {self.__estado__}"
        )