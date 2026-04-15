import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEMP_DIR = PROJECT_ROOT / "data" / "temperatura_municipio"
RESULTADOS_DIR = PROJECT_ROOT / "data" / "resultados"
RESULTADOS_DIR.mkdir(parents=True, exist_ok=True)

# 1. Cargar el dataframe (sustituye 'tu_archivo.csv' por el nombre real de tu resultado del spatial join)
# Si ya lo tienes en memoria en Colab, puedes saltar este paso.
df_clima = pd.read_csv(TEMP_DIR / 'municipios_temperatura_final.csv')

def limpiar_datos_clima(df):
    # Crear copia para no afectar el original
    df_clean = df.copy()

    # 2. Generar Clave Municipal de 5 dígitos (01001)
    # Esto corrige el problema de que '1008' deba ser '01008'
    df_clean['cve_mun_full'] = (
        df_clean['CVE_ENT'].astype(str).str.zfill(2) + 
        df_clean['CVE_MUN'].astype(str).str.zfill(3)
    )

    # 3. Convertir Rango de Temperatura (TEM_C) a Valor Numérico Promedio
    # Maneja casos como "14 - 16" -> 15.0
    def parse_temp(rango):
        try:
            if '-' in str(rango):
                partes = [float(x.strip()) for x in str(rango).split('-')]
                return sum(partes) / len(partes)
            return float(rango)
        except:
            return None

    df_clean['temp_media_anual'] = df_clean['TEM_C'].apply(parse_temp)

    # 4. Limpieza de nombres de municipios (Quitar caracteres extraños de codificación)
    # La imagen mostraba "TepezalÃfÂ¡", esto intenta corregir errores comunes de encoding
    def corregir_texto(texto):
        if pd.isna(texto): return texto
        try:
            # Intento de corregir doble codificación común en archivos de CONABIO/INEGI
            return texto.encode('latin-1').decode('utf-8')
        except:
            return texto

    df_clean['NOM_MUN_CLEAN'] = df_clean['NOM_MUN'].apply(corregir_texto)

    # 5. Seleccionar solo las columnas necesarias para el merge final
    # Mantenemos ZON_TER para tener el contexto de "Semicálido", "Templado", etc.
    columnas_finales = [
        'cve_mun_full', 
        'NOM_MUN_CLEAN', 
        'temp_media_anual', 
        'ZON_TER'
    ]
    
    return df_clean[columnas_finales]

# Ejecutar limpieza
df_clima_final = limpiar_datos_clima(df_clima)

# 6. Guardar el archivo listo para el Merge Final
df_clima_final.to_csv(RESULTADOS_DIR / 'clima_municipal.csv', index=False, encoding='utf-8-sig')

print(f"Archivo '{RESULTADOS_DIR / 'clima_municipal.csv'}' generado.")
print(df_clima_final.head())