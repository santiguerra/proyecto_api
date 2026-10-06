"""
Módulo de interfaz de usuario por consola.
Se encarga de la entrada de datos por parte del usuario y de
la visualización formateada de los resultados utilizando la función format.
"""

from typing import Tuple
import pandas as pd


def pedir_datos_usuario() -> Tuple[str, int]:
    """
    Solicita al usuario el departamento y el número de registros que desea consultar.
    Valida que los datos ingresados sean correctos.

    :return: Tupla con (nombre_departamento, limite_registros).
    """
    print("\n" + "=" * 60)
    print("       CONSULTA DE CASOS COVID-19 EN COLOMBIA")
    print("=" * 60)

    # 1. Solicitar Departamento
    while True:
        departamento = input(" Ingrese el nombre del Departamento a consultar: ").strip()
        if departamento:
            break
        print(" [!] El nombre del departamento no puede estar vacío. Intente de nuevo.")

    # 2. Solicitar Límite de registros
    print(" [i] Nota: Ingrese un valor razonable (ej. 10 a 500).")
    print("     Consultar números muy altos (>1000) puede demorar o colgar la consulta.")
    while True:
        entrada_limite = input(" Ingrese el número de registros a obtener: ").strip()
        if not entrada_limite.isdigit():
            print(" [!] Debe ingresar un número entero positivo válido.")
            continue

        limite = int(entrada_limite)
        if limite <= 0:
            print(" [!] El número de registros debe ser mayor a cero.")
            continue

        if limite > 1000:
            confirmacion = input(
                f" [?] Ha seleccionado {limite} registros (un valor alto). ¿Desea continuar? [S/N]: "
            ).strip().upper()
            if confirmacion not in ["S", "SI", "Y"]:
                print(" Ingrese un nuevo valor menor:")
                continue

        break

    return departamento, limite


def mostrar_resultados(df: pd.DataFrame, departamento: str) -> None:
    """
    Muestra los resultados obtenidos en pantalla utilizando la función de formato (str.format)
    garantizando que las columnas se encuentren alineadas y legibles.

    :param df: DataFrame con las 6 columnas requeridas.
    :param departamento: Nombre del departamento consultado.
    """
    if df.empty:
        print("\n" + "-" * 60)
        print(f" [!] No se encontraron registros para el departamento: '{departamento}'.")
        print("     Verifique la ortografía (ej. ANTIOQUIA, BOGOTA, RISARALDA, VALLE).")
        print("-" * 60)
        return

    columnas = list(df.columns)

    # Calcular el ancho óptimo de cada columna según el encabezado y sus datos
    anchos = {}
    for col in columnas:
        longitud_maxima_datos = max([len(str(val)) for val in df[col]], default=0)
        anchos[col] = max(len(col), longitud_maxima_datos) + 2

    # Construir la plantilla de formato para el encabezado y las filas usando format
    # Cada campo queda formateado con alineación izquierda '{:<ancho}'
    plantilla_fila = " | ".join(
        ["{:<" + str(anchos[col]) + "}" for col in columnas]
    )

    # Encabezado formateado con .format()
    encabezado = plantilla_fila.format(*columnas)
    separador_doble = "=" * len(encabezado)
    separador_simple = "-" * len(encabezado)

    print("\n" + separador_doble)
    print(f" RESULTADOS DE LA CONSULTA: {departamento.upper()} ({len(df)} registros)")
    print(separador_doble)
    print(encabezado)
    print(separador_doble)

    # Imprimir cada fila utilizando la función format
    for _, fila in df.iterrows():
        valores_fila = [str(fila[col]) for col in columnas]
        print(plantilla_fila.format(*valores_fila))

    print(separador_simple)
    print(f" Total de casos mostrados: {format(len(df), 'd')}")
    print(separador_doble + "\n")


def mostrar_mensaje_error(mensaje: str) -> None:
    """
    Muestra un mensaje de error estilizado en la consola.
    """
    print("\n" + "!" * 60)
    print(f" ERROR: {mensaje}")
    print("!" * 60 + "\n")
