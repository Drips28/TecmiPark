"""
Tecmi Park - Sistema de Gestión de Estacionamiento
Módulos:
1. Registro de Ingreso de Vehículo
2. Cálculo de Tarifa por Hora y Cobro
3. Disponibilidad de Lugares en Tiempo Real
"""

import math
from datetime import datetime

# Configuración del Estacionamiento
CAPACIDAD_MAXIMA = 20
TARIFAS = {
    "auto": 25.0,     # Tarifa por hora en MXN
    "moto": 15.0,
    "camioneta": 35.0
}

# Estructura en memoria: {placa: {"tipo": str, "hora_ingreso": datetime}}
estacionamiento = {}


def mostrar_disponibilidad():
    ocupados = len(estacionamiento)
    libres = CAPACIDAD_MAXIMA - ocupados
    print("\n" + "=" * 40)
    print(f" ESTADO DE OCUPACIÓN: {ocupados}/{CAPACIDAD_MAXIMA}")
    print(f" Lugares disponibles: {libres}")
    print("=" * 40)
    return libres


def registrar_ingreso():
    if len(estacionamiento) >= CAPACIDAD_MAXIMA:
        print("\n[!] Cupo lleno. No se permiten más ingresos.")
        return

    placa = input("\nIngrese la placa del vehículo: ").strip().upper()
    if not placa:
        print("[!] La placa no puede estar vacía.")
        return

    if placa in estacionamiento:
        print(f"[!] El vehículo con placa {placa} ya se encuentra registrado.")
        return

    print("Tipos válidos: auto | moto | camioneta")
    tipo = input("Tipo de vehículo: ").strip().lower()
    if tipo not in TARIFAS:
        print("[!] Tipo inválido. Se cancela el registro.")
        return

    hora_ingreso = datetime.now()
    estacionamiento[placa] = {
        "tipo": tipo,
        "hora_ingreso": hora_ingreso
    }

    print(f"\n[OK] Ingreso exitoso: Placa {placa} ({tipo}) a las {hora_ingreso.strftime('%H:%M:%S')}")


def registrar_salida_y_cobro():
    placa = input("\nIngrese la placa del vehículo a retirar: ").strip().upper()
    if placa not in estacionamiento:
        print(f"[!] No existe registro activo para la placa {placa}.")
        return

    registro = estacionamiento.pop(placa)
    hora_ingreso = registro["hora_ingreso"]
    hora_salida = datetime.now()
    tipo = registro["tipo"]

    duracion = hora_salida - hora_ingreso
    segundos_totales = max(duracion.total_seconds(), 60)  # Mínimo 1 minuto
    horas_a_cobrar = math.ceil(segundos_totales / 3600.0)

    tarifa_base = TARIFAS[tipo]
    total_pagar = horas_a_cobrar * tarifa_base

    print("\n" + "-" * 35)
    print("           TICKET DE COBRO          ")
    print("-" * 35)
    print(f" Placa:          {placa}")
    print(f" Tipo:           {tipo.capitalize()}")
    print(f" Ingreso:        {hora_ingreso.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f" Salida:         {hora_salida.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f" Horas cobradas: {horas_a_cobrar} h")
    print(f" Tarifa x hora:  ${tarifa_base:.2f}")
    print(f" TOTAL A PAGAR:  ${total_pagar:.2f}")
    print("-" * 35)


def listar_vehiculos():
    if not estacionamiento:
        print("\nNo hay vehículos en el estacionamiento.")
        return

    print("\n--- Vehículos Estacionados ---")
    for placa, data in estacionamiento.items():
        print(f"Placa: {placa:<10} | Tipo: {data['tipo']:<10} | Ingreso: {data['hora_ingreso'].strftime('%H:%M:%S')}")


def main():
    while True:
        mostrar_disponibilidad()
        print("\n1. Registrar ingreso de vehículo")
        print("2. Registrar salida y cobro")
        print("3. Listar vehículos dentro")
        print("4. Salir")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_ingreso()
        elif opcion == "2":
            registrar_salida_y_cobro()
        elif opcion == "3":
            listar_vehiculos()
        elif opcion == "4":
            print("Cerrando sistema.")
            break
        else:
            print("[!] Opción inválida.")


if __name__ == "__main__":
    main()
