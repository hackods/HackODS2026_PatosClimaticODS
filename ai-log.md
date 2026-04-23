# AI Log - HackODS UNAM 2026

## Herramientas utilizadas
- GitHub Copilot Chat (GPT-5.3-Codex)
- GitHub Copilot en VS Code

## Filosofia de uso
La IA se uso como apoyo tecnico para depuracion, instalacion de dependencias, estructuracion de scripts, generacion inicial de graficas con librerias como `plotly` y documentacion operativa. Las decisiones finales de contenido, pipeline, narrativa y validacion de resultados fueron tomadas por el equipo.

## Registro de uso

### 2026-04-23 | GitHub Copilot Chat | Integracion INIFED-911 y agregacion municipal
- **Tarea**: Construir pipeline para integrar datos de INIFED con 911 por CCT y generar salida a nivel municipal.
- **Prompts**: Solicitudes para estandarizar `cve_ent/cve_mun/cve_mun_full`, unir por CCT, incluir sostenimiento (publico/privado), y conservar variables de infraestructura (bebederos, techumbre, luz, agua, ambito).
- **Resultado**: Se creo `scripts/procesamiento_infied.py` con lectura robusta de CSV, normalizacion de claves, merge por CCT, reporte de no coincidencias y agregacion municipal en `data/resultados/infied_municipio.csv`.
- **Modificacion del equipo**: Se decidio que la unificacion final con la base maestra se ejecute en Quarto, no dentro del script de INIFED.
- **Decision propia**: Mantener separadas la capa de procesamiento (script) y la capa de integracion narrativa (Quarto) para mejorar trazabilidad y control.

### 2026-04-23 | GitHub Copilot Chat | Quarto con doble salida de datos
- **Tarea**: Generar automaticamente dos salidas municipales desde `dashboard/index.qmd`.
- **Prompts**: Solicitud para producir una base completa integrada y otra base tematica de infraestructura.
- **Resultado**: En Quarto se agrego un bloque de merge que genera:
	- `data/resultados/base_datos_final_con_infied.csv`
	- `data/resultados/base_infraestructura_municipal.csv`
- **Modificacion del equipo**: Se validaron llaves municipales y cobertura de municipios con datos INIFED antes de usar los archivos en narrativa.
- **Decision propia**: Adoptar estrategia hibrida (base maestra + base tematica) para balancear analisis integral y rapidez de visualizacion.

### 2026-04-23 | GitHub Copilot Chat | Limpieza de commit y sincronizacion con GitHub
- **Tarea**: Resolver fallo de push por archivos mayores a 100 MB y ordenar commits.
- **Prompts**: Solicitudes para identificar conflicto de sync, limpiar `.gitignore`, quitar artefactos pesados y rehacer commit con mensaje en espanol.
- **Resultado**: Se excluyeron archivos grandes crudos/derivados de INIFED del versionado, se rehizo el commit sin archivos bloqueantes y se completo el push exitoso a `origin/main`.
- **Modificacion del equipo**: Se pidio evitar la firma `Co-authored-by` y conservar mensajes de commit en espanol.
- **Decision propia**: Priorizar commits reproducibles y ligeros, documentando en README como regenerar localmente los archivos no versionados.

### 2026-04-13 | GitHub Copilot Chat | Instalacion de dependencias en el entorno
- **Tarea**: Instalar `plotly` para ejecutar el notebook Quarto.
- **Prompt**: El entorno mostraba `ModuleNotFoundError: No module named 'plotly'`.
- **Resultado**: Se instalo `plotly` en el entorno virtual del proyecto.
- **Modificacion del equipo**: Se volvio a ejecutar el notebook usando el Python del `.venv`.
- **Decision propia**: Se acepto la sugerencia porque resolvia una dependencia faltante sin cambiar el codigo del proyecto.

### 2026-04-13 | GitHub Copilot Chat | Apoyo con graficas en Plotly
- **Tarea**: Generar la estructura base de graficas para el tablero usando `plotly`.
- **Prompt**: Se pidio apoyo para crear codigo base de visualizaciones en `plotly.express`.
- **Resultado**: Se propusieron graficas base y la configuracion inicial de librerias para el tablero.
- **Modificacion del equipo**: Cada grafica fue verificada manualmente, ajustando titulos, colores, ejes y etiquetas para asegurar que los datos se reflejaran de forma consistente.
- **Decision propia**: Se acepto solo el esqueleto tecnico; la interpretacion visual y la consistencia final fueron revisadas por el equipo.

### 2026-04-13 | GitHub Copilot Chat | Configuracion de Quarto para usar el entorno
- **Tarea**: Hacer que Quarto usara el Python correcto desde VS Code.
- **Prompt**: Se pidio configurar el entorno para ejecutar las celdas del archivo `Proyecto.qmd`.
- **Resultado**: Se agrego configuracion en `_quarto.yml` y luego se corrigio el flujo para que Quarto ejecutara con el interprete del proyecto.
- **Modificacion del equipo**: Se ajustaron rutas y se verifico el render con el entorno activado.
- **Decision propia**: Se mantuvo la estructura del documento y solo se corrigio la configuracion de ejecucion.

### 2026-04-14 | GitHub Copilot Chat | Depuracion de procesamiento de PDF y Excel
- **Tarea**: Resolver errores de `tabula`, `pypdf`, `openpyxl` y mismatches de columnas en scripts de procesamiento.
- **Prompt**: Se compartieron trazas como `ModuleNotFoundError`, `IndexError` y `ValueError` de pandas.
- **Resultado**: Se instalaron dependencias faltantes y se agregaron validaciones de pagina, normalizacion de filas y filtros de notas/fuentes.
- **Modificacion del equipo**: Se conservaron las reglas de negocio del pipeline y solo se endurecio la lectura/parsing de datos.
- **Decision propia**: Se aceptaron los cambios porque resolvian fallas reales sin alterar el objetivo analitico.

### 2026-04-14 | GitHub Copilot Chat | Unificacion de matricula y clima
- **Tarea**: Preparar la unificacion de bases por `cve_mun_full` y ordenar el procesamiento de archivos.
- **Prompt**: Se pidio ordenar archivos `salida (x).xls`, crear un `requirements.txt`, documentar el pipeline y explicar el uso de `uv`.
- **Resultado**: Se generaron scripts, README y la lista de dependencias para reproducir el entorno.
- **Modificacion del equipo**: El equipo decidio que la narrativa final y la integracion entre fuentes quedaran escritas manualmente.
- **Decision propia**: Se acepto la automatizacion para tareas repetitivas, pero no para la narrativa del tablero.

### 2026-04-14 | GitHub Copilot Chat | Verificacion manual de consistencia de datos
- **Tarea**: Revisar que las graficas y tablas no mezclaran valores incorrectos al integrar las bases.
- **Prompt**: Se pidio ayuda para detectar errores de columnas, claves y orden de procesamiento.
- **Resultado**: Se corrigieron problemas de lectura, orden y llaves de union.
- **Modificacion del equipo**: El equipo inspecciono manualmente muestras de salida para confirmar consistencia entre municipios, estados y claves generadas.
- **Decision propia**: Se mantuvo el criterio humano en la validacion final porque la coherencia analitica no puede delegarse por completo a la IA.

## Decisiones propias
- La narrativa final del proyecto fue redactada por el equipo.
- Las claves de union y el orden de procesamiento se ajustaron segun la estructura real de los archivos fuente.
- Las dependencias se fijaron en `requirements.txt` para replicabilidad.
- Las graficas fueron construidas con apoyo de IA, pero cada salida fue revisada manualmente antes de integrarla al tablero.
- La consistencia de datos entre las tres bases se valido por muestreo y revision del equipo.
- Se agrego una estrategia de dos salidas municipales: base maestra integrada y base tematica de infraestructura.
- Se decidio no versionar insumos/salidas pesadas de INIFED por limites de GitHub, dejando su regeneracion documentada.

## NO se uso IA para
- La interpretacion final de los hallazgos del proyecto.
- La seleccion conceptual de las variables que sostienen la historia.
- La redaccion final de la narrativa del tablero.
