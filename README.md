# Compresor de Texto - Codificación Huffman

Este es un proyecto educativo de escritorio desarrollado en Python utilizando la librería **Tkinter** para la interfaz gráfica. Implementa el algoritmo de **Codificación Huffman** para la compresión y descompresión de archivos de texto (`.txt`), ofreciendo una trazabilidad completa paso a paso de las métricas de compresión, tablas de frecuencias y estructuras de árbol generadas.

## 🚀 Características

- **Carga de Archivos:** Lectura directa de archivos de texto plano (`.txt`) con soporte de codificación UTF-8.
- **Visualización en Tiempo Real:** - Tabla de frecuencias detallada de cada carácter.
  - Representación en texto estructurado del Árbol de Huffman resultante.
  - Tabla de códigos binarios asignados a cada símbolo.
  - Vista previa de la cadena de bits codificada.
- **Métricas Avanzadas:** Cálculo y visualización dinámica de los bits originales, bits comprimidos y el porcentaje exacto de reducción de tamaño.
- **Compresión Eficiente:** Exportación del texto codificado en un formato binario propietario (`.huf`) que optimiza el espacio mediante empaquetamiento de bytes y manejo de alineación (*padding*).
- **Descompresión Precisa:** Capacidad de restaurar completamente el texto original a partir del archivo `.huf` empleando los metadatos y la tabla de frecuencias incrustados en su cabecera JSON.

## 📁 Estructura del Proyecto

El código fuente está modularizado de la siguiente manera:

- `main.py`: Punto de entrada que inicializa y ejecuta el bucle principal de la aplicación gráfica.
- `ui.py`: Define la interfaz de usuario moderna basada en `tkinter.ttk`, gestionando los paneles de entrada, pestañas de desarrollo paso a paso y diálogos de archivos.
- `controller.py`: Funciona como mediador (*Controller*) entre la interfaz de usuario y la lógica de compresión, manteniendo el estado de los últimos resultados y formateando las tablas informativas.
- `huffman.py`: Contiene el núcleo matemático del algoritmo (construcción del árbol con `heapq`, generación de diccionarios de códigos, funciones recursivas de exploración, codificación y decodificación).
- `utils.py`: Provee herramientas auxiliares para el manejo de cadenas especiales (como espacios o saltos de línea), así como la lógica de bajo nivel para serializar, escribir y leer los archivos binarios `.huf` con su firma mágica (`HUF1`).

## 🛠️ Requisitos

- **Python 3.7 o superior**
- **Tkinter** (normalmente incluido en la instalación estándar de Python).
  - *Nota para usuarios de Linux (Ubuntu/Debian):* Si experimentas problemas al abrir la interfaz, puedes instalarlo manualmente ejecutando:
    ```bash
    sudo apt-get install python3-tk
    ```

## 💻 Instalación y Uso

1. **Clonar o descargar** todos los archivos fuente en un mismo directorio local:
   ```text
   mi_proyecto_huffman/
   ├── main.py
   ├── ui.py
   ├── controller.py
   ├── huffman.py
   └── utils.py
   ```
2. Abrir una terminal y navegar hasta la ubicación de la carpeta:
 ```Bash
   cd ruta/a/tu/carpeta/mi_proyecto_huffman
 ```
3. Ejecutar la aplicación con el intérprete de Python:

  En Windows:
 ```Bash
  python main.py
 ```
  En Mac / Linux:
  ```Bash
  python3 main.py
 ```
📄 Formato del Archivo Comprimido (.huf)
Los archivos de salida se guardan con una estructura binaria optimizada:

Firma Mágica (4 bytes): Constante HUF1 para validación de formato.

Longitud de Cabecera (4 bytes): Entero de 32 bits (big-endian) que indica el tamaño en bytes de los metadatos.

Cabecera JSON: Contiene el diccionario mapeado de frecuencias y el número de bits de relleno (padding) aplicados al último byte.

Cuerpo de Datos (Payload): Flujo binario empaquetado correspondiente al texto codificado.

Desarrollado como un proyecto práctico de Estructuras de Datos y Algoritmos de Compresión.
