"""
Programa Principal (main.py)
Orquestador de la Arquitectura de Software Modular para la consulta
de datos abiertos de COVID-19 en Colombia.

Autor: Santiago Guerra
Materia: Programación 3
Universidad Tecnológica de Pereira
"""

import sys
from api.cliente import obtener_datos, filtrar_datos
from ui.interfaz import (
    pedir_datos_usuario,
    mostrar_resultados,
    mostrar_mensaje_error,
)


def ejecutar_aplicacion() -> None:
    """
    Función que coordina la interacción entre el módulo UI y el módulo API.
    """
    print("\n************************************************************")
    print("*  SISTEMA DE CONSULTA COVID-19 COLOMBIA (DATOS ABIERTOS)  *")
    print("************************************************************")

    while True:
        try:
            # 1. Módulo UI: Captura de parámetros requeridos del usuario
            departamento, limite = pedir_datos_usuario()

            print(f"\n[+] Consultando los últimos {limite} casos para '{departamento}' en datos.gov.co...")

            # 2. Módulo API: Obtención de datos mediante sodapy
            df_crudo = obtener_datos(
                nombre_departamento=departamento,
                limite_registros=limite
            )

            # 3. Módulo API: Filtrado de las 6 columnas funcionales requeridas
            df_filtrado = filtrar_datos(df_crudo)

            # 4. Módulo UI: Presentación de datos formateados con la función format
            mostrar_resultados(df_filtrado, departamento)

        except KeyboardInterrupt:
            print("\n\n[!] Programa interrumpido por el usuario.")
            break
        except Exception as error:
            mostrar_mensaje_error(str(error))

        # Preguntar si desea realizar otra consulta
        opcion = input("¿Desea realizar otra consulta? (S/N): ").strip().upper()
        if opcion not in ["S", "SI", "Y"]:
            print("\nGracias por utilizar el sistema de consulta. ¡Hasta pronto!\n")
            break


def main():
    try:
        ejecutar_aplicacion()
    except Exception as error:
        print(f"\nOcurrió un error inesperado en la ejecución: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
