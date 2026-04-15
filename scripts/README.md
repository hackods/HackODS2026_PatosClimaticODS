# HackODS - Guia de Reproduccion del Ambiente y Pipeline de Datos

Este proyecto unifica 3 fuentes de datos para construir una tabla final por municipio:
- Atlas (indicadores educativos e infraestructura)
- Matricula escolar
- Clima/temperatura municipal

## 1) Replicar el ambiente virtual con uv

Este proyecto se puede replicar con uv, sin necesidad de activar el entorno manualmente.

### Opcion A: entorno uv dentro del proyecto (recomendado)
1. Abrir terminal en `C:\Users\ASUS\Documents\HackODS\Proyecto`
2. Crear entorno:
   - `uv venv .venv`
3. Instalar dependencias:
   - `uv pip install -r requirements.txt`

### Opcion B: entorno uv en otra carpeta (externo)
1. Crear entorno externo (ejemplo):
   - `uv venv C:\envs\hackods-uv`
2. Instalar dependencias del proyecto en ese entorno:
   - `uv pip install --python C:\envs\hackods-uv\Scripts\python.exe -r C:\Users\ASUS\Documents\HackODS\Proyecto\requirements.txt`

Nota: aunque el entorno este en otra carpeta, los scripts funcionan igual si ejecutas con el Python de ese entorno.

## 2) Flujo de procesamiento de las 3 bases

## Base A: Atlas (PDF)
Archivo fuente:
- `C:\Users\ASUS\Documents\HackODS\0000_Atlas_completo.pdf`

Script:
- `C:\Users\ASUS\Documents\HackODS\procesamiento - copia.py`

Ejecucion:
1. Activar entorno (opcional) o usar Python del entorno uv
2. Ejecutar:
   - `C:\Users\ASUS\Documents\HackODS\Proyecto\.venv\Scripts\python.exe "C:\Users\ASUS\Documents\HackODS\procesamiento - copia.py"`

Salida esperada:
- `C:\Users\ASUS\Documents\HackODS\Proyecto\Datos_Atlas_Final.xlsx`

## Base B: Matricula
Archivos fuente:
- `C:\Users\ASUS\Documents\HackODS\matricula\salida (2).xls` ... `salida (33).xls`

Script:
- `C:\Users\ASUS\Documents\HackODS\matricula\matricula_procesamiento.py`

Ejecucion:
1. Activar entorno (opcional) o usar Python del entorno uv
2. Ejecutar:
   - `C:\Users\ASUS\Documents\HackODS\Proyecto\.venv\Scripts\python.exe C:\Users\ASUS\Documents\HackODS\matricula\matricula_procesamiento.py`

Salida esperada:
- `C:\Users\ASUS\Documents\HackODS\matricula\matricula_unificada_final.csv`

## Base C: Clima / Temperatura
Archivo fuente:
- `C:\Users\ASUS\Documents\HackODS\tman13gw\municipios_temperatura_final.csv`

Script:
- `C:\Users\ASUS\Documents\HackODS\tman13gw\procesamiento_temperatura2.py`

Ejecucion:
1. Activar entorno (opcional) o usar Python del entorno uv
2. Cambiar a la carpeta de clima (para respetar rutas relativas del script):
   - `cd C:\Users\ASUS\Documents\HackODS\tman13gw`
3. Ejecutar:
   - `C:\Users\ASUS\Documents\HackODS\Proyecto\.venv\Scripts\python.exe procesamiento_temperatura2.py`

Salida esperada:
- `C:\Users\ASUS\Documents\HackODS\tman13gw\clima_municipal_listo.csv`

## 3) Unificacion final (merge por clave municipal)

La llave comun es `cve_mun_full`.

Ejemplo rapido de merge final en Python:

```python
import pandas as pd

# Matricula
mat = pd.read_csv(r"C:\Users\ASUS\Documents\HackODS\matricula\matricula_unificada_final.csv", dtype={"cve_mun_full": str})

# Clima
clima = pd.read_csv(r"C:\Users\ASUS\Documents\HackODS\tman13gw\clima_municipal_listo.csv", dtype={"cve_mun_full": str})

# Atlas (ajusta a tu estructura final del xlsx)
atlas = pd.read_excel(r"C:\Users\ASUS\Documents\HackODS\Proyecto\Datos_Atlas_Final.xlsx", dtype={"CVEGEO": str})
atlas = atlas.rename(columns={"CVEGEO": "cve_mun_full"})

# Merge
final = mat.merge(clima, on="cve_mun_full", how="left")
final = final.merge(atlas, on="cve_mun_full", how="left")

final.to_csv(r"C:\Users\ASUS\Documents\HackODS\tabla_final_historia.csv", index=False, encoding="utf-8-sig")
print("OK: tabla_final_historia.csv")
```

## 4) Regenerar requirements

Si instalas paquetes nuevos y quieres congelar versiones:
- `uv pip freeze --python C:\Users\ASUS\Documents\HackODS\Proyecto\.venv\Scripts\python.exe > C:\Users\ASUS\Documents\HackODS\Proyecto\requirements.txt`

Ubicacion recomendada de requirements:
- `C:\Users\ASUS\Documents\HackODS\Proyecto\requirements.txt`
