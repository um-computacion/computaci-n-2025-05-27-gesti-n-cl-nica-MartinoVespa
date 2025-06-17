class ClinicaException(Exception):
    pass


class PacienteNoEncontradoException(ClinicaException):
    pass


class MedicoNoEncontradoException(ClinicaException):
    pass


class MedicoNoDisponibleException(ClinicaException):
    pass


class EspecialidadInvalidaException(ClinicaException):
    pass


class TurnoOcupadoException(ClinicaException):
    pass


class DatosInvalidosException(ClinicaException):
    pass