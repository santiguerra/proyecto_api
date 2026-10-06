"""
Módulo encargado de interactuar con la API de datos abiertos (Socrata)
y procesar la información en DataFrames de pandas.
"""

import unicodedata
import logging
import pandas as pd
from sodapy import Socrata

# Silenciar advertencias informativas de sodapy (como la advertencia de app_token ausente)
logging.getLogger().setLevel(logging.ERROR)

# Identificador del conjunto de datos de casos positivos de COVID-19 en Colombia
DATASET_ID = "gt2j-8ykr"
API_DOMAIN = "www.datos.gov.co"


def normalizar_texto(texto: str) -> str:
    """
    Normaliza el texto eliminando tildes y convirtiéndolo a mayúsculas
    para que coincida con el formato del conjunto de datos en datos.gov.co.
    """
    if not texto:
        return ""
    texto_limpio = texto.strip().upper()
    # Eliminar marcas de acentuación (tildes)
    texto_sin_tildes = "".join(
        c for c in unicodedata.normalize("NFD", texto_limpio)
        if unicodedata.category(c) != "Mn"
    )
    return texto_sin_tildes


def obtener_datos(nombre_departamento: str, limite_registros: int) -> pd.DataFrame:
    """
    Realiza la consulta a la API de datos abiertos usando sodapy y retorna
    un DataFrame con los resultados obtenidos.

    :param nombre_departamento: Nombre o código del departamento a consultar.
    :param limite_registros: Cantidad máxima de registros a solicitar.
    :return: pd.DataFrame con los datos crudos obtenidos de la API.
    """
    depto_normalizado = normalizar_texto(nombre_departamento)

    try:
        # Cliente no autenticado para datasets públicos
        client = Socrata(API_DOMAIN, None, timeout=30)

        # Si el usuario ingresó un código numérico (ej. "66"), se consulta por 'departamento'
        # De lo contrario, se consulta por 'departamento_nom'
        if depto_normalizado.isdigit():
            results = client.get(
                DATASET_ID,
                limit=limite_registros,
                departamento=depto_normalizado
            )
        else:
            results = client.get(
                DATASET_ID,
                limit=limite_registros,
                departamento_nom=depto_normalizado
            )

        client.close()

        # Si no hubo resultados por coincidencia exacta, intentar búsqueda insensible a mayúsculas
        if not results and not depto_normalizado.isdigit():
            client = Socrata(API_DOMAIN, None, timeout=30)
            where_query = f"upper(departamento_nom) = '{depto_normalizado}'"
            results = client.get(
                DATASET_ID,
                limit=limite_registros,
                where=where_query
            )
            client.close()

        # Convertir a pandas DataFrame
        if results:
            df = pd.DataFrame.from_records(results)
        else:
            df = pd.DataFrame()

        return df

    except Exception as error:
        raise RuntimeError(f"Error al conectar o consultar la API: {error}") from error


def filtrar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filtra y renombra el DataFrame para conservar únicamente las 6 columnas
    exigidas por los Requerimientos Funcionales:
    1. Ciudad de ubicación
    2. Departamento
    3. Edad
    4. Tipo
    5. Estado
    6. País de procedencia

    :param df: DataFrame con los registros crudos de la API.
    :return: DataFrame limpio con las 6 columnas requeridas.
    """
    columnas_requeridas = [
        "Ciudad de ubicación",
        "Departamento",
        "Edad",
        "Tipo",
        "Estado",
        "País de procedencia"
    ]

    if df.empty:
        return pd.DataFrame(columns=columnas_requeridas)

    df_filtrado = pd.DataFrame()

    # Mapeo de columnas con soporte para variantes de nombres en la API
    # 1. Ciudad de ubicación
    if "ciudad_municipio_nom" in df.columns:
        df_filtrado["Ciudad de ubicación"] = df["ciudad_municipio_nom"]
    elif "ciudad_municipio" in df.columns:
        df_filtrado["Ciudad de ubicación"] = df["ciudad_municipio"]
    else:
        df_filtrado["Ciudad de ubicación"] = "No reportada"

    # 2. Departamento
    if "departamento_nom" in df.columns:
        df_filtrado["Departamento"] = df["departamento_nom"]
    elif "departamento" in df.columns:
        df_filtrado["Departamento"] = df["departamento"]
    else:
        df_filtrado["Departamento"] = "No reportado"

    # 3. Edad
    if "edad" in df.columns:
        df_filtrado["Edad"] = df["edad"]
    else:
        df_filtrado["Edad"] = "N/A"

    # 4. Tipo
    if "fuente_tipo_contagio" in df.columns:
        df_filtrado["Tipo"] = df["fuente_tipo_contagio"]
    elif "tipo" in df.columns:
        df_filtrado["Tipo"] = df["tipo"]
    else:
        df_filtrado["Tipo"] = "Desconocido"

    # 5. Estado
    if "estado" in df.columns:
        df_filtrado["Estado"] = df["estado"]
    else:
        df_filtrado["Estado"] = "N/A"

    # 6. País de procedencia
    if "pais_viajo_1_nom" in df.columns:
        df_filtrado["País de procedencia"] = df["pais_viajo_1_nom"].fillna("Colombia")
    elif "pais_viajo_1_cod" in df.columns:
        df_filtrado["País de procedencia"] = df["pais_viajo_1_cod"].fillna("Colombia")
    else:
        df_filtrado["País de procedencia"] = "Colombia"

    # Normalizar valores vacíos o nulos
    df_filtrado = df_filtrado.fillna("N/A")
    df_filtrado["País de procedencia"] = df_filtrado["País de procedencia"].replace("", "Colombia")

    return df_filtrado[columnas_requeridas]
