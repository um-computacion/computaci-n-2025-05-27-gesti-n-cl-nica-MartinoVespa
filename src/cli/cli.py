from ..modelo import Clinica, Paciente, Medico, Especialidad, Turno, Receta
from ..excepciones import ClinicaException


class CLI:

    def __init__(self):
        self.clinica = Clinica()
        self.opciones = {
            "1": ("Registrar paciente", self.registrar_paciente),
            "2": ("Registrar médico", self.registrar_medico),
            "3": ("Agregar especialidad a médico", self.agregar_especialidad),
            "4": ("Agendar turno", self.agendar_turno),
            "5": ("Emitir receta", self.emitir_receta),
            "6": ("Ver historia clínica", self.ver_historia_clinica),
            "7": ("Listar pacientes", self.listar_pacientes),
            "8": ("Listar médicos", self.listar_medicos),
            "9": ("Salir", lambda: "salir"),
        }

    def mostrar_menu(self):
        print("\n" + "=" * 50)
        print("     SISTEMA DE GESTIÓN CLÍNICA")
        print("=" * 50)
        for key in self.opciones:
            print(f"{key}. {self.opciones[key][0]}")
        print("=" * 50)
        return input("\nSeleccione una opción: ")

    def ejecutar(self):
        print("¡Bienvenido al Sistema de Gestión de Clínica!")
        opcion = ""
        while opcion != "salir":
            try:
                opcion = self.mostrar_menu()
                if opcion in self.opciones:
                    resultado = self.opciones[opcion][1]()
                    if resultado == "salir":
                        break
                else:
                    print("\nOpción inválida. Intente nuevamente.")
            except ClinicaException as e:
                print(f"\nERROR: {str(e)}")
            except KeyboardInterrupt:
                print("\n\n¡Hasta luego!")
                break
            except Exception as e:
                print(f"\nError inesperado: {str(e)}")

    def registrar_paciente(self):
        print("\n" + "-" * 30)
        print("   REGISTRAR PACIENTE")
        print("-" * 30)
        try:
            nombre = input("Nombre completo: ").strip()
            dni = input("DNI: ").strip()
            fecha_nacimiento = input("Fecha de nacimiento (dd/mm/aaaa): ").strip()

            paciente = self.clinica.registrar_paciente(nombre, dni, fecha_nacimiento)
            print(f"\nPaciente registrado exitosamente:")
            print(f"   {paciente}")
        except Exception as e:
            print(f"Error al registrar paciente: {str(e)}")

    def registrar_medico(self):
        print("\n" + "-" * 30)
        print("   REGISTRAR MÉDICO")
        print("-" * 30)
        try:
            nombre = input("Nombre completo: ").strip()
            matricula = input("Matrícula profesional: ").strip()

            medico = self.clinica.registrar_medico(nombre, matricula)
            print(f"\nMédico registrado exitosamente:")
            print(f"   {medico}")
            print("\nRecuerde agregar especialidades al médico usando la opción 3.")
        except Exception as e:
            print(f"Error al registrar médico: {str(e)}")

    def agregar_especialidad(self):
        print("\n" + "-" * 40)
        print("   AGREGAR ESPECIALIDAD A MÉDICO")
        print("-" * 40)
        try:
            medicos = self.clinica.listar_medicos()
            if not medicos:
                print("No hay médicos registrados. Registre un médico primero.")
                return

            print("\nMédicos disponibles:")
            for i, medico in enumerate(medicos, 1):
                print(f"{i}. {medico}")

            matricula = input("\nMatrícula del médico: ").strip()
            tipo_especialidad = input("Nombre de la especialidad: ").strip()

            print(
                "\nDías disponibles: lunes, martes, miércoles, jueves, viernes, sábado, domingo"
            )
            print("Ingrese los días de atención separados por coma")
            dias_input = input("Días: ").strip()
            dias = [dia.strip() for dia in dias_input.split(",")]

            especialidad = self.clinica.agregar_especialidad_a_medico(
                matricula, tipo_especialidad, dias
            )
            print(f"\nEspecialidad agregada exitosamente:")
            print(f"   {especialidad}")

            medico = self.clinica.buscar_medico(matricula)
            print(f"\nMédico actualizado:")
            print(f"   {medico}")
        except Exception as e:
            print(f"Error al agregar especialidad: {str(e)}")

    def agendar_turno(self):
        print("\n" + "-" * 30)
        print("   AGENDAR TURNO")
        print("-" * 30)
        try:
            pacientes = self.clinica.listar_pacientes()
            medicos = self.clinica.listar_medicos()

            if not pacientes:
                print("No hay pacientes registrados. Registre un paciente primero.")
                return
            if not medicos:
                print("No hay médicos registrados. Registre un médico primero.")
                return

            print("\nPacientes disponibles:")
            for i, paciente in enumerate(pacientes, 1):
                print(f"{i}. {paciente}")

            print("\nMédicos disponibles:")
            for i, medico in enumerate(medicos, 1):
                print(f"{i}. {medico}")

            dni_paciente = input("\nDNI del paciente: ").strip()
            matricula_medico = input("Matrícula del médico: ").strip()

            try:
                medico = self.clinica.buscar_medico(matricula_medico)
                print(
                    f"\nEspecialidades disponibles para Dr/a. {medico.obtener_nombre()}:"
                )
                for especialidad in medico.obtener_especialidades():
                    print(f"- {especialidad}")
            except:
                pass

            fecha = input("\nFecha del turno (dd/mm/aaaa): ").strip()
            hora = input("Hora del turno (HH:MM): ").strip()
            especialidad = input("Especialidad para el turno: ").strip()

            turno = self.clinica.agendar_turno(
                dni_paciente, matricula_medico, fecha, hora, especialidad
            )
            print(f"\nTurno agendado exitosamente:")
            print(f"   {turno}")
        except Exception as e:
            print(f"Error al agendar turno: {str(e)}")

    def emitir_receta(self):
        print("\n" + "-" * 30)
        print("   EMITIR RECETA")
        print("-" * 30)
        try:
            pacientes = self.clinica.listar_pacientes()
            medicos = self.clinica.listar_medicos()

            if not pacientes:
                print("No hay pacientes registrados.")
                return
            if not medicos:
                print("No hay médicos registrados.")
                return

            print("\nPacientes disponibles:")
            for i, paciente in enumerate(pacientes, 1):
                print(f"{i}. {paciente}")

            print("\nMédicos disponibles:")
            for i, medico in enumerate(medicos, 1):
                print(f"{i}. {medico}")

            dni_paciente = input("\nDNI del paciente: ").strip()
            matricula_medico = input("Matrícula del médico: ").strip()
            fecha = input("Fecha de la receta (dd/mm/aaaa): ").strip()

            print("\nIngrese los medicamentos separados por coma")
            medicamentos_input = input("Medicamentos: ").strip()
            medicamentos = [med.strip() for med in medicamentos_input.split(",")]

            indicaciones = input("Indicaciones: ").strip()

            receta = self.clinica.emitir_receta(
                dni_paciente, matricula_medico, fecha, medicamentos, indicaciones
            )
            print(f"\nReceta emitida exitosamente:")
            print(f"   {receta}")
            print(f"   Medicamentos: {', '.join(receta.obtener_medicamentos())}")
            print(f"   Indicaciones: {receta.obtener_indicaciones()}")
        except Exception as e:
            print(f"Error al emitir receta: {str(e)}")

    def ver_historia_clinica(self):
        print("\n" + "-" * 35)
        print("   VER HISTORIA CLÍNICA")
        print("-" * 35)
        try:
            pacientes = self.clinica.listar_pacientes()
            if not pacientes:
                print("No hay pacientes registrados.")
                return

            print("\nPacientes disponibles:")
            for i, paciente in enumerate(pacientes, 1):
                print(f"{i}. {paciente}")

            dni_paciente = input("\nDNI del paciente: ").strip()

            historia = self.clinica.obtener_historia_clinica(dni_paciente)

            print(f"\n{historia}")
            print("\n" + "=" * 60)

            turnos = historia.obtener_turnos()
            if turnos:
                print("TURNOS:")
                print("-" * 60)
                for i, turno in enumerate(turnos, 1):
                    print(f"{i}. {turno}")
            else:
                print("No hay turnos registrados")

            print("\n" + "=" * 60)

            recetas = historia.obtener_recetas()
            if recetas:
                print("RECETAS:")
                print("-" * 60)
                for i, receta in enumerate(recetas, 1):
                    print(f"{i}. {receta}")
                    print(
                        f"    Medicamentos: {', '.join(receta.obtener_medicamentos())}"
                    )
                    print(f"    Indicaciones: {receta.obtener_indicaciones()}")
                    print()
            else:
                print("No hay recetas registradas")

        except Exception as e:
            print(f"Error al consultar historia clínica: {str(e)}")

    def listar_pacientes(self):
        print("\n" + "-" * 30)
        print("   LISTAR PACIENTES")
        print("-" * 30)
        try:
            pacientes = self.clinica.listar_pacientes()
            if not pacientes:
                print("No hay pacientes registrados")
                return

            print(f"\nTotal de pacientes: {len(pacientes)}")
            print("-" * 50)
            for i, paciente in enumerate(pacientes, 1):
                print(f"{i}. {paciente}")
        except Exception as e:
            print(f"Error al listar pacientes: {str(e)}")

    def listar_medicos(self):
        print("\n" + "-" * 30)
        print("   LISTAR MÉDICOS")
        print("-" * 30)
        try:
            medicos = self.clinica.listar_medicos()
            if not medicos:
                print(" No hay médicos registrados")
                return

            print(f"\nTotal de médicos: {len(medicos)}")
            print("-" * 50)
            for i, medico in enumerate(medicos, 1):
                print(f"{i}. {medico}")
        except Exception as e:
            print(f"Error al listar médicos: {str(e)}")