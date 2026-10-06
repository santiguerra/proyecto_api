# Proyecto Fundamentos Básicos de Python

**Docente:** Alejandro Rodas Vásquez  
**Universidad Tecnológica de Pereira**  

---

## 1. Requerimientos Funcionales

La aplicación permite al usuario ingresar:
- **`nombre_departamento`**: Departamento que desea consultar.
- **`limite_registros`**: Número de registros que desea obtener.

El resultado se visualiza en pantalla utilizando la función `format` y contiene únicamente las siguientes columnas:
- Ciudad de ubicación
- Departamento
- Edad
- Tipo
- Estado
- País de procedencia

---

## 2. Requerimientos de la Arquitectura de Software

El software está construido aplicando el concepto de modularidad con la siguiente separación:
- **Módulo para UI (`ui/`):** Encargado de la interacción con el usuario y visualización de datos formateados.
- **Módulo API (`api/`):** Encargado de la conexión y consulta a la API de datos abiertos mediante `sodapy` y procesamiento con `pandas`.
- **`main.py`:** Archivo separado que orquesta la ejecución llamando a los módulos.

### Estructura del Proyecto
```
ProyectoAPI/
├── api/
│   ├── __init__.py
│   └── cliente.py
├── ui/
│   ├── __init__.py
│   └── interfaz.py
├── venv/
├── main.py
└── requirements.txt
```

---

## 3. Fundamento Teórico (Evidencias para la Entrega)

### ¿Qué es un Diagrama de Componentes?
Un Diagrama de Componentes es un diagrama de tipo estructural dentro del lenguaje UML (Unified Modeling Language) que describe la organización física y lógica de los componentes de un sistema de software, mostrando cómo se dividen y cómo se comunican entre sí.

### ¿Para qué se utiliza?
Se utiliza para modelar la arquitectura de software de un sistema, representar los componentes modulares (módulos, librerías, subsistemas), definir cómo interactúan a través de sus interfaces y gestionar las dependencias entre las diferentes partes del sistema.

### ¿Qué es un componente?
Un componente es una unidad modular, autónoma y reemplazable de un sistema de software que encapsula su comportamiento y estado interno, exponiendo un conjunto de interfaces bien definidas para comunicarse con otros componentes.

---

## 4. Ejecución

1. Activar el entorno virtual:
   ```bash
   source venv/bin/activate
   ```
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecutar el programa:
   ```bash
   python main.py
   ```
