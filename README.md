# PatosClimaticODS
## HackODS - Pipeline de Procesamiento y Reproduccion (uv)

Este repositorio integra 3 fuentes de datos para construir una base final para el analisis de resiliencia educativa ante el cambio climatico:

- Atlas (educacion e infraestructura municipal)
- Matricula escolar municipal (SICEE/911)
- Clima y temperatura por municipio (CONABIO/CONAGUA)

## Ejecución rápida 

```bash
# 1. Configura el entorno reprodusible con uv
uv sync

# 2. Ejecuta los scripts de procesamiento de datos (en orden):
python scripts/procesamiento_temperatura.py
python scripts/procesamiento_temperatura2.py
python scripts/matricula_procesamiento.py
python scripts/procesamiento -copia.py
python scripts/procesamiento_infied.py

# 3. Abre la narrativa interactiva en Jupyter:
jupyter notebook dashboard/HackODS.ipynb
```

**Resultado:** Dashboard con secciones narrativas, análisis y visualizaciones en `dashboard/HackODS.ipynb`

## Datos del equipo

- Nombre del equipo: PatosClimaticODS
- ODS elegidos:
	- ODS 4: Educacion de Calidad (Meta 4.a: Instalaciones educativas adecuadas)
	- ODS 13: Accion por el Clima (Meta 13.1: Resiliencia y adaptacion)
- URL del repositorio: 

## Pregunta central del proyecto

- Problema:
	Mexico ha logrado niveles historicos de acceso a la educacion, pero la infraestructura fisica de las aulas no esta adaptada al aumento de temperaturas extremas, comprometiendo el confort termico necesario para el aprendizaje.
- Pregunta principal:
	Cuentan las escuelas primarias en Mexico con las condiciones fisicas y servicios basicos necesarios para garantizar el confort termico y la permanencia escolar frente al estres climatico?
- Audiencia objetivo:
	Tomadores de decisiones en infraestructura educativa (SEP/INIFED), gobiernos municipales y organismos de adaptacion climatica.
- Impacto esperado:
	Identificar brechas criticas donde la falta de servicios basicos (agua/luz/sombra) y el calor extremo coinciden, permitiendo priorizar inversiones en las zonas de mayor vulnerabilidad educativa.

### Narrativa: Del acceso a las condiciones adecuadas

**El problema:** México expandió el acceso a la educación, eso es cierto. Pero mientras tanto, el cambio climático está elevando temperaturas en regiones enteras. Ampliar acceso a más escuelas no resolve el problema real: ¿tienen esas aulas las condiciones para que los estudiantes aprendan?

**El concepto que lo explica todo: Confort térmico**  
Confort térmico son las condiciones de temperatura en las que una persona puede concentrarse y desempeñarse adecuadamente. Cuando hay 40°C afuera y el aula no tiene ventilación, agua potable ni servicios básicos, estudiantes y docentes viven bajo estrés por calor. No decimos que la temperatura mata el aprendizaje directamente, pero podemos definir condiciones básicas para que este se lleve a cabo: ventilación cruzada, acceso a agua potable, techos que reduzcan el calor. Lo que vemos es que faltan los servicios necesarios para que el aprendizaje pueda ocurrir en lugares con calor extremo.

**El cruce que cuenta la verdad:**  
Tomamos datos de INEGI sobre infraestructura escolar (agua, electricidad, servicios) y los cruzamos con temperaturas de CONAGUA. El resultado: zonas donde el calor extremo coincide exactamente con escuelas sin lo básico. Eso es lo que queremos mostrar.

**Por qué los ODS entran aquí:**  
- **ODS 4.a** pide instalaciones educativas "adecuadas" ¿Pero adecuado a qué? A climas normales de antes. Hoy necesitamos que mantengan confort térmico bajo calor extremo.
- **ODS 13** pide que nos adaptemos al cambio climático. Las escuelas son infraestructura pública. Deben ser resilientes para afrontar las nuevas temperaturas.

**Al final:**  
La pregunta es simple: ¿cuáles son esas zonas donde el calor más la falta de servicios se juntan? Ahí es donde hay que invertir primero. No es negar que México avanzó. Es decir que ahora hay que asegurar que esas escuelas realmente funcionen en el clima que tenemos.

# Metadatos de datasets

## 1. Atlas (Educación e Infraestructura)

**Fuente oficial:** SEP - Dirección General de Planeación, Programación y Estadística Educativa (DGPPyEE).

**URL:** https://www.planeacion.sep.gob.mx/principalescifras/

**Fecha de descarga:** 14 de abril de 2026.

**Licencia:** Términos de Libre Uso de Información de la Administración Pública Federal.

### Variables usadas

### Infraestructura

- % Agua potable  
- % Electricidad  
- % Drenaje  
- % Pavimentación  
- % Internet  
- % Recolección de basura  

### Variables sociales

- Grado de escolaridad  
- Índice de marginación  
- Asistencia escolar (6-11, 12-14, 15-17 años)  

---

## 2. Matrícula (SICEE / Formato 911)

**Fuente oficial:** SEP - Sistema de Estadísticas Continuas de Educación del Formato 911.

**URL:** https://www.planeacion.sep.gob.mx/principalescifras/

**Fecha de descarga:** 14 de abril de 2026.

**Licencia:** Libre uso (Datos Abiertos México).

### Variables usadas

- Alumnos total  
- Alumnos mujeres  
- Alumnos hombres  
- Docentes  
- Escuelas  

---

## 3. Temperatura municipal (Clima)

**Fuente oficial:** CONABIO / CONAGUA (Servicio Meteorológico Nacional).

**URL:**  
http://geoportal.conabio.gob.mx/metadatos/doc/html/tman13gw.html  
https://datos.conagua.gob.mx/

**Fecha de descarga:** 14 de abril de 2026.

**Licencia:** Creative Commons Attribution (CC BY).

### Variables usadas

- Temperatura media anual  
- Temperatura máxima  
- Zona térmica (ZON_TER)  

---

## 4. Infraestructura física (INIFED / SIGED)

**Fuente oficial:** SEP - Sistema de Información y Gestión Educativa (SIGED).

**URL:** https://siged.sep.gob.mx/SIGED/datos_abiertos.html

**Fecha de descarga:** 14 de abril de 2026.

**Licencia:** Libre uso (Datos Abiertos México).

### Variables usadas

- CUBIERTA_TECHUMBRE_EXT (indicador de sombra)  
- ESTRUCTURAS_ATIPICAS (precariedad de materiales)  
- BEBEDEROS  
- NUM_AULAS  

---

## 5. Climatología y Geografía (INEGI)

**Fuente oficial:** Instituto Nacional de Estadística y Geografía (INEGI).

**URL:** https://www.inegi.org.mx/temas/climatologia/#descargas

**Fecha de descarga:** 14 de abril de 2026.

**Licencia:** Términos de libre uso de información del INEGI.

### Uso

Datos vectoriales de tipos de clima, isotermas y entorno geográfico para discernir entre zonas urbanas y rurales.

---

## 6. Marco Teórico y Referencia Científica (SciELO)

**Fuente:** SciELO México / Revista de Arquitectura y Urbanismo.

**Referencia:**  
*"Confort térmico y eficiencia energética en el diseño de infraestructura"*

**URL:** https://www.scielo.org.mx/scielo.php?script=sci_arttext&pid=S2594-19252022000400105

### Uso

Fundamentación científica para la definición de confort térmico y selección de variables de materialidad y habitabilidad escolar.

---

## Nota sobre interoperabilidad

El repositorio utiliza la **Clave Geoelectoral Municipal (CVEGEO)** a 5 dígitos como llave primaria para el cruce de las bases educativas, climáticas y de infraestructura.

## Declaratoria IA (modulo A5)

Este repositorio incluye:
- Declaratoria y reglamento de uso de IA
- ai-log.md con trazabilidad de uso

Uso reportado: apoyo para depuracion de scripts, normalizacion de datos y estructura base de visualizaciones. La narrativa final y la interpretacion de hallazgos fueron validadas por el equipo.

## Licencia (modulo A1)

Este proyecto está bajo licencia **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)**.  
Ver archivo [`LICENSE`](LICENSE) en la raíz del repositorio.

## Narrativa completa (Jupyter Notebook)

**Archivo principal:** [`dashboard/HackODS.ipynb`](dashboard/HackODS.ipynb)

El notebook contiene la narrativa estructurada en secciones Markdown + visualizaciones:
- Problema y contexto (ODS 4 vs ODS 13)
- Introducción a confort térmico
- Análisis de desigualdades territoriales
- Visualizaciones de vulnerabilidad térmica educativa
- Recomendaciones accionables para tomadores de decisión

**Para ver el análisis completo:**
```bash
jupyter notebook dashboard/HackODS.ipynb
```

---

## 1) Estructura del proyecto

- `pyproject.toml`: configuracion del proyecto Python.
- `uv.lock`: lockfile de dependencias para `uv`.
- `scripts/procesamiento - copia.py`: procesa el PDF del Atlas y genera tabla unificada.
- `scripts/matricula_procesamiento.py`: procesa los archivos `salida (x).xls` de matricula.
- `scripts/procesamiento_temperatura.py`: cruza shapefiles (join espacial) y genera clima por municipio.
- `scripts/procesamiento_temperatura2.py`: limpia/estandariza clima para merge final.
- `scripts/procesamiento_infied.py`: integra INIFED con 911 por CCT y genera salida por escuela y agregada por municipio.
- `dashboard/index.qmd`: documento Quarto principal con carga de datos, validaciones y merges municipales.
- `dashboard/styles.css`: estilos del dashboard Quarto.
- `data/matricula/`: archivos fuente de matricula (`salida (2).xls` ... `salida (33).xls`).
- `data/temperatura_municipio/`: insumos de clima (SHP/DBF/PRJ/SHX y CSV).
- `data/resultados/`: salidas finales/intermedias de analisis.
- `dashboards/`: espacio para visualizaciones/tableros.

---

## 2) Ambiente virtual con uv

Ejecuta esto en la raiz del repo (`hackODS`):

```bash
uv venv .venv
uv sync
```

El proyecto usa `pyproject.toml` + `uv.lock` como fuente principal de dependencias.

Puedes correr todo sin activar entorno usando `uv run ...`.

### Dependencias para GitHub (recomendado)
- Versionadas: `pyproject.toml` y `uv.lock`.
- Al clonar: `uv sync`.

### Si tambien quieres requirements.txt
Exportar (desde este entorno):

```bash
uv pip freeze --python .venv/Scripts/python.exe > requirements.txt
```

Instalar desde requirements con uv:

```bash
uv pip install -r requirements.txt
```

---

## 3) Orden recomendado de ejecucion

## Paso A. Matricula

### Insumos
- `data/matricula/salida (2).xls` ... `data/matricula/salida (33).xls`

### Ejecucion

```bash
uv run python "scripts/matricula_procesamiento.py"
```

### Salida esperada
- `data/resultados/matricula_unificada_final.csv`

---

## Paso B. Clima (join espacial)

### Insumos
Dentro de `data/temperatura_municipio/` deben existir:
- `tman13gw.shp` (+ `.dbf`, `.prj`, `.shx`)
- `mun21gw.shp` (+ `.dbf`, `.prj`, `.shx`)

### Ejecucion

```bash
uv run python scripts/procesamiento_temperatura.py
uv run python scripts/procesamiento_temperatura2.py
```

### Salidas esperadas
- `data/temperatura_municipio/municipios_temperatura_final.csv`
- `data/resultados/clima_municipal.csv`

---

## Paso C. Atlas

### Insumo
- `data/0000_Atlas_completo.pdf` (tu configuracion actual)

### Ejecucion

```bash
uv run python "scripts/procesamiento - copia.py"
```

### Salida esperada
- `data/resultados/atlas_datos_unificado.xlsx`

---

## Paso D. INIFED + 911 (por CCT)

### Insumos
- `data/INFIED/INIFED_2020-2022_CSV.csv`
- `data/INFIED/ESTANDAR_BASICA_I2324.csv`

### Ejecucion

```bash
uv run python scripts/procesamiento_infied.py
```

### Salidas esperadas
- `data/resultados/infied_servicios_con_clave_municipio.csv` (nivel escuela con cve_mun_full)
- `data/resultados/infied_servicios_con_clave_municipio_cct_sin_match.csv` (reporte sin match)
- `data/resultados/infied_municipio.csv` (agregado municipal de infraestructura)

---

## Paso E. Salidas duales desde Quarto

Al renderizar `dashboard/index.qmd` se generan dos bases municipales:

- `data/resultados/base_datos_final_con_infied.csv` (base maestra integrada)
- `data/resultados/base_infraestructura_municipal.csv` (base tematica de infraestructura)

Ejecucion:

```bash
uv run quarto render dashboard/index.qmd
```

---

## 4) Unificacion final para analisis

Llave comun entre fuentes:
- `cve_mun_full`

Fuentes ya procesadas:
- Matricula: `data/resultados/matricula_unificada_final.csv`
- Clima: `data/resultados/clima_municipal.csv`
- Atlas: `data/resultados/atlas_datos_unificado.xlsx` (columna `CVEGEO` -> renombrar a `cve_mun_full`)

Puedes generar una tabla final (ej. `data/resultados/base_datos_final.csv`) con un merge por `cve_mun_full`.

Desde la version actual, el merge con INIFED a nivel municipal se automatiza en Quarto y produce una base maestra y una base tematica.

---

## 5) Resultados finales sugeridos

Ubicar salidas finales en `data/resultados/`:

- `matricula_unificada_final.csv`
- `clima_municipal.csv`
- `atlas_datos_unificado.xlsx`
- `base_datos_final.csv`
- `base_datos_final_con_infied.csv`
- `base_infraestructura_municipal.csv`
- `MASTER_DB_HACKODS_2026.csv`

### Nota sobre archivos pesados

Por limites de tamano de GitHub, los archivos GeoJSON de gran tamano en `data/resultados/` no se versionan. Los insumos geoespaciales de `data/temperatura_municipio/` si forman parte del repositorio para facilitar la reproducibilidad del cruce espacial. El pipeline incluye scripts para regenerar resultados derivados localmente.

Adicionalmente, por limite de 100 MB de GitHub y para mantener commits limpios:

- No se versionan los insumos crudos grandes de INIFED en `data/INFIED/`.
- No se versionan salidas derivadas de INIFED en `data/resultados/infied_*.csv`.

Si estos archivos no aparecen en GitHub, se regeneran localmente con:

```bash
uv run python scripts/procesamiento_infied.py
uv run quarto render dashboard/index.qmd
```

---

## 6) Solucion de problemas comunes

- `ModuleNotFoundError`: instala paquete faltante con `uv pip install <paquete>`.
- `No objects to concatenate`: revisar que se hayan detectado archivos `salida (x).xls`.
- `Import lxml failed`: `uv pip install lxml`.
- `PermissionError` al guardar CSV: cerrar el archivo si esta abierto en Excel.



