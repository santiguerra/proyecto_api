"""
Módulo API para consulta de datos abiertos de COVID-19 en Colombia.
"""

from .cliente import obtener_datos, filtrar_datos

__all__ = ["obtener_datos", "filtrar_datos"]
