import geopandas as gpd
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEMP_DIR = PROJECT_ROOT / "data" / "temperatura_municipio"

# 1. Cargar las capas
isotermas = gpd.read_file(TEMP_DIR / "tman13gw.shp")
municipios = gpd.read_file(TEMP_DIR / "mun21gw.shp") # Necesitas este de INEGI

# 2. Asegurar que ambos usen el mismo sistema de coordenadas (WGS84)
isotermas = isotermas.to_crs(epsg=4326)
municipios = municipios.to_crs(epsg=4326)

# 3. Spatial Join: Une municipios con la temperatura que les corresponde
# 'predicate=intersects' hace que si el municipio toca el polígono, se unan
mun_con_clima = gpd.sjoin(municipios, isotermas, how="left", predicate="intersects")

# 4. Limpieza: Si un municipio toca dos rangos, tomamos el promedio o el primero
mun_final = mun_con_clima.drop_duplicates(subset=['CVE_MUN', 'CVE_ENT'])

# 5. Exportar a CSV para tu merge con la matrícula
df_export = pd.DataFrame(mun_final.drop(columns='geometry'))
df_export.to_csv(TEMP_DIR / "municipios_temperatura_final.csv", index=False)