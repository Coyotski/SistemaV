
# Sistema Vedas

Sistema Vedas es una aplicación para la consulta de vedas pesqueras en México. Permite buscar información sobre especies, periodos y zonas de veda a partir de un archivo CSV, con una interfaz gráfica amigable.


## Estructura del proyecto

- `vedas-grafica.exe`: Ejecutable principal del sistema (versión empaquetada para Windows).
- `vedas-grafica.py`: Versión en Python del sistema, con interfaz gráfica (Tkinter).
- `VEDAS TRANSCRITAS.csv`: Archivo de datos en formato CSV con la información de vedas.
- `Manual_Vedas_Pesqueras_Windows.pdf`: Manual de usuario para el sistema.
- `Justificacion_Sistema_Vedas.pdf`: Documento de justificación del sistema.
- `_internal/`: Carpeta con librerías y dependencias necesarias para la ejecución del sistema empaquetado.


## Requisitos

- Sistema operativo: Windows
- Para `vedas-grafica.exe`: No requiere instalación de Python, ya que incluye dependencias en `_internal/`.
- Para `vedas-grafica.py`: Requiere Python 3.10+ y las librerías estándar (`tkinter`).


## Uso

### Opción 1: Ejecutar el programa empaquetado
1. Ejecuta `vedas-grafica.exe` para iniciar el sistema.
2. Consulta el manual (`Manual_Vedas_Pesqueras_Windows.pdf`) para instrucciones detalladas de uso.
3. Los datos principales se encuentran en `VEDAS TRANSCRITAS.csv`.

### Opción 2: Ejecutar desde Python
1. Asegúrate de tener Python 3.10 o superior instalado en tu sistema.
2. Ejecuta el archivo `vedas-grafica.py`:
	```powershell
	python vedas-grafica.py
	```
3. Selecciona el archivo `VEDAS TRANSCRITAS.csv` cuando la aplicación lo solicite.
4. Utiliza la interfaz gráfica para realizar consultas por tipo de veda, fecha o especie.


## Créditos

- Desarrollado por Coyotski


## Notas

- Si tienes problemas al ejecutar el sistema, revisa que todos los archivos y carpetas estén en la misma ubicación.
- Para más información, consulta los documentos PDF incluidos en el proyecto.
- El archivo `vedas-grafica.py` permite modificar y extender la funcionalidad del sistema fácilmente si tienes conocimientos de Python.

