import pandas as pd
import glob
import unicodedata
import re
from pathlib import Path

def normalizar_texto(valor):
    return str(valor).replace("\n", " ").strip()

def normalizar_clave(valor):
    texto = normalizar_texto(valor).lower()
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    texto = " ".join(texto.split())
    return texto

# 1. Obtener la lista de todos los archivos de salida
PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_DIR = PROJECT_ROOT / "data" / "matricula"
RESULTADOS_DIR = PROJECT_ROOT / "data" / "resultados"
RESULTADOS_DIR.mkdir(parents=True, exist_ok=True)
archivos_xls = glob.glob(str(INPUT_DIR / 'salida (*.xls'))


def extraer_num_archivo(ruta_archivo):
    match = re.search(r'\((\d+)\)', str(ruta_archivo))
    return int(match.group(1)) if match else float("inf")


# Procesar en orden real: salida (2), salida (3), ...
archivos_xls = sorted(archivos_xls, key=extraer_num_archivo)

lista_estados = []

for archivo in archivos_xls:
    try:
        # --- EXTRAER CLAVE DE ESTADO DESDE EL NOMBRE DEL ARCHIVO ---
        # Busca el número dentro de los paréntesis: 'salida (2).xls' -> 2
        match = re.search(r'\((\d+)\)', archivo)
        if not match:
            print(f"Saltando {archivo}: No se encontró número de estado en el nombre.")
            continue
        
        num_archivo = int(match.group(1))
        # Regla solicitada: cve_ent = numero de archivo - 1, con padding a 2 digitos.
        num_estado = num_archivo - 1
        if num_estado < 1:
            print(f"Saltando {archivo}: el número de estado calculado ({num_estado}) es inválido.")
            continue
        cve_ent = f"{num_estado:02d}"  # Ej: 8 -> '08', 9 -> '09', 10 -> '10'

        tablas_candidatas = []
        try:
            tablas_candidatas.append(pd.read_excel(archivo, header=None))
        except Exception:
            pass
        try:
            tablas_candidatas.extend(pd.read_html(archivo, header=None))
        except Exception:
            pass

        if not tablas_candidatas:
            raise ValueError("No se pudieron leer tablas del archivo.")

        df_limpio = None
        for df_temp in tablas_candidatas:
            if df_temp is None or df_temp.empty:
                continue

            columnas_norm = [normalizar_texto(c) for c in df_temp.columns]
            columnas_clave = [normalizar_clave(c) for c in columnas_norm]

            if 'municipio' in columnas_clave:
                df_candidate = df_temp.copy()
                df_candidate.columns = columnas_norm
            else:
                mask_municipio = df_temp.apply(
                    lambda fila: fila.astype(str).map(normalizar_clave).eq('municipio').any(), axis=1
                )
                if not mask_municipio.any():
                    continue

                idx_inicio = mask_municipio[mask_municipio].index[0]
                encabezados = [normalizar_texto(c) for c in df_temp.iloc[idx_inicio].tolist()]
                df_candidate = df_temp.iloc[idx_inicio + 1:].copy()
                df_candidate.columns = encabezados

            rename_map = {}
            for col in df_candidate.columns:
                col_norm = normalizar_clave(col)
                if col_norm == 'municipio':
                    rename_map[col] = 'Municipio'
                elif col_norm == 'escuelas':
                    rename_map[col] = 'Escuelas'
                elif col_norm == 'alumnos':
                    rename_map[col] = 'Alumnos'
                elif col_norm == 'alumnos mujeres':
                    rename_map[col] = 'Alumnos Mujeres'
                elif col_norm == 'alumnos hombres':
                    rename_map[col] = 'Alumnos Hombres'
                elif col_norm.startswith('docentes'):
                    rename_map[col] = 'Docentes¹'

            df_candidate = df_candidate.rename(columns=rename_map)

            if 'Municipio' in df_candidate.columns:
                df_limpio = df_candidate
                break

        if df_limpio is None:
            raise ValueError("No se encontró la tabla con encabezado 'Municipio'.")
        
        df_limpio = df_limpio[df_limpio['Municipio'].notna()]
        df_limpio = df_limpio[df_limpio['Municipio'].astype(str).str.strip().str.upper() != 'TOTAL']
        df_limpio = df_limpio[df_limpio['Municipio'].astype(str).str.strip().str.lower() != 'municipio']

        # Eliminar filas de notas al pie o fuentes que se cuelan como si fueran municipios.
        municipio_norm = df_limpio['Municipio'].astype(str).map(normalizar_clave)
        mascara_notas = (
            municipio_norm.str.contains(r'fuente|conjunto de individuos|sistema de estadisticas', regex=True)
            | municipio_norm.str.startswith('1 ')
            | municipio_norm.str.startswith('¹')
        )
        df_limpio = df_limpio[~mascara_notas]

        # Convertir columnas numéricas y descartar filas no numéricas (normalmente notas).
        columnas_numericas = [c for c in ['Escuelas', 'Alumnos', 'Alumnos Mujeres', 'Alumnos Hombres', 'Docentes¹'] if c in df_limpio.columns]
        for col in columnas_numericas:
            df_limpio[col] = pd.to_numeric(
                df_limpio[col].astype(str).str.replace(',', '', regex=False).str.strip(),
                errors='coerce'
            )
        if columnas_numericas:
            df_limpio = df_limpio.dropna(subset=columnas_numericas, how='all')
        
        # --- GENERAR CLAVE DE MUNICIPIO SECUENCIAL ---
        df_limpio = df_limpio.reset_index(drop=True)
        # Crea clave de 5 dígitos: Estado(2) + Municipio(3)
        df_limpio['cve_mun_full'] = df_limpio.index.map(lambda i: f"{cve_ent}{i+1:03d}")
        
        cols_interes = ['cve_mun_full', 'Municipio', 'Escuelas', 'Alumnos', 'Alumnos Mujeres', 'Alumnos Hombres', 'Docentes¹']
        cols_presentes = [c for c in cols_interes if c in df_limpio.columns]
        
        df_limpio = df_limpio[cols_presentes]
        lista_estados.append(df_limpio)
        print(f"Procesado exitosamente: {archivo} (Estado: {cve_ent})")
        
    except Exception as e:
        print(f"Error en {archivo}: {e}")

if not lista_estados:
    print("No se encontraron tablas válidas para concatenar.")
else:
    df_matricula_nacional = pd.concat(lista_estados, ignore_index=True)

    if 'Municipio' in df_matricula_nacional.columns:
        df_matricula_nacional['Municipio'] = df_matricula_nacional['Municipio'].astype(str).str.upper().str.strip()

    print(f"\nUnificación terminada. Total de registros: {len(df_matricula_nacional)}")
    ruta_guardado = RESULTADOS_DIR / "matricula_unificada_final.csv"
    df_matricula_nacional.to_csv(ruta_guardado, index=False, encoding='utf-8-sig')
    print(f"Archivo guardado exitosamente en: {ruta_guardado}")