from pathlib import Path
import geopandas as gpd
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTADOS_DIR = PROJECT_ROOT / "data" / "resultados"


def resolve_first_existing(paths: list[Path]) -> Path:
    for p in paths:
        if p.exists():
            return p
    raise FileNotFoundError("No se encontro ningun archivo en las rutas candidatas.")


def build_tmax_municipal(
    estaciones_shp: Path,
    municipios_shp: Path,
    output_csv: Path,
) -> Path:
    gdf_est = gpd.read_file(estaciones_shp)
    gdf_mun = gpd.read_file(municipios_shp)

    if "CVEGEO" not in gdf_mun.columns:
        raise ValueError("El shapefile municipal no contiene la columna CVEGEO.")

    # Homologar CRS para join espacial
    if gdf_mun.crs != gdf_est.crs:
        gdf_mun = gdf_mun.to_crs(gdf_est.crs)

    # Campos de anomalias maximas por periodo (1..12 mensual, 13 agregado)
    max_cols = [c for c in gdf_est.columns if c.startswith("A_MAX")]
    if not max_cols:
        raise ValueError("No se encontraron columnas A_MAX* en la capa de estaciones.")

    # Join espacial: cada estacion cae en un municipio
    joined = gpd.sjoin(
        gdf_est[max_cols + ["geometry"]],
        gdf_mun[["CVEGEO", "geometry"]],
        how="inner",
        predicate="within",
    )

    if joined.empty:
        raise ValueError("El join espacial no genero coincidencias entre estaciones y municipios.")

    # Agregacion municipal por promedio simple de estaciones
    agg = joined.groupby("CVEGEO", as_index=False)[max_cols].mean(numeric_only=True)

    # Renombrado legible para consumo analitico
    rename_map = {}
    for c in max_cols:
        idx = c.replace("A_MAX", "")
        if idx.isdigit() and 1 <= int(idx) <= 12:
            rename_map[c] = f"tmax_anom_m{int(idx):02d}"
        elif idx == "13":
            rename_map[c] = "tmax_anom_anual"
        else:
            rename_map[c] = f"tmax_anom_{idx.lower()}"

    agg = agg.rename(columns=rename_map)
    agg = agg.rename(columns={"CVEGEO": "cve_mun_full"})
    agg["cve_mun_full"] = agg["cve_mun_full"].astype(str).str.zfill(5)

    # Conteo de estaciones usadas por municipio para auditoria
    station_count = joined.groupby("CVEGEO", as_index=False).size().rename(columns={"size": "estaciones_count"})
    station_count["CVEGEO"] = station_count["CVEGEO"].astype(str).str.zfill(5)
    agg = agg.merge(station_count.rename(columns={"CVEGEO": "cve_mun_full"}), on="cve_mun_full", how="left")

    RESULTADOS_DIR.mkdir(parents=True, exist_ok=True)
    agg.to_csv(output_csv, index=False, encoding="utf-8-sig")
    return output_csv


def main() -> None:
    estaciones_shp = resolve_first_existing(
        [
            PROJECT_ROOT / "temperaturas_maximas" / "mensuales" / "anomalias_tmaxmean.shp",
            PROJECT_ROOT / "mensuales" / "anomalias_regionales_tmaxmean.shp",
        ]
    )

    municipios_shp = resolve_first_existing(
        [
            PROJECT_ROOT / "data" / "temperatura_municipio" / "mun21gw.shp",
            PROJECT_ROOT / "data" / "temperatura_municipio" / "mun21gw" / "mun21gw.shp",
        ]
    )

    output_csv = RESULTADOS_DIR / "temperatura_maxima_municipal_estaciones.csv"
    out = build_tmax_municipal(estaciones_shp, municipios_shp, output_csv)
    print(f"Archivo generado: {out}")


if __name__ == "__main__":
    main()
