from datetime import datetime
from ..excepciones import DatosInvalidosException


class Paciente:

    def __init__(self, nombre: str, dni: str, fecha_nacimiento: str):

        if not nombre or not isinstance(nombre, str):
            raise DatosInvalidosException("El nombre es requerido y debe ser texto")
        if not dni or not isinstance(dni, str):
            raise DatosInvalidosException("El DNI es requerido y debe ser texto")
        if not fecha_nacimiento or not isinstance(fecha_nacimiento, str):
            raise DatosInvalidosException(
                "La fecha de nacimiento es requerida y debe ser texto"
            )

        try:
            datetime.strptime(fecha_nacimiento, "%d/%m/%Y")
        except ValueError:
            raise DatosInvalidosException(
                f"Formato de fecha inválido: {fecha_nacimiento}. Use dd/mm/aaaa"
            )

        self.__nombre__ = nombre
        self.__dni__ = dni
        self.__fecha_nacimiento__ = fecha_nacimiento

    def obtener_dni(self) -> str:
        return self.__dni__

    def obtener_nombre(self) -> str:
        return self.__nombre__

    def obtener_fecha_nacimiento(self) -> str:
        return self.__fecha_nacimiento__

    def __str__(self) -> str:
        return f"Paciente: {self.__nombre__} (DNI: {self.__dni__}, Nacimiento: {self.__fecha_nacimiento__})"