from pathlib import Path
import argparse
import geopandas as gpd
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def build_cve_mun_full(df: gpd.GeoDataFrame) -> pd.Series:
    ent = df["CVE_ENT"].astype(str).str.zfill(2)
    mun = df["CVE_MUN"].astype(str).str.zfill(3)
    return ent + mun


def choose_region_columns(df_reg: gpd.GeoDataFrame) -> list[str]:
    base = ["R_CLIM", "NR_CLIM"]
    metric_prefixes = ("A_P", "AS_P", "A_MAX", "AS_MAX", "A_MIN", "AS_MIN")

    cols = []
    for c in df_reg.columns:
        if c in base:
            cols.append(c)
            continue
        if any(c.startswith(pref) for pref in metric_prefixes):
            cols.append(c)

    # Keep a compact schema if some expected columns are missing.
    return cols


def assign_region_to_municipio(
    municipios: gpd.GeoDataFrame,
    regiones: gpd.GeoDataFrame,
    region_cols: list[str],
) -> gpd.GeoDataFrame:
    mun_cols = ["CVE_ENT", "CVE_MUN", "NOMGEO", "geometry"]
    mun = municipios[mun_cols].copy()
    reg = regiones[region_cols + ["geometry"]].copy()

    # Use an equal-area CRS to compare overlap areas.
    mun = mun.to_crs(epsg=6933)
    reg = reg.to_crs(epsg=6933)

    inter = gpd.overlay(mun, reg, how="intersection", keep_geom_type=False)
    if inter.empty:
        raise ValueError("No hubo interseccion entre municipios y regiones climaticas.")

    inter["_area"] = inter.geometry.area
    inter = inter.sort_values(["CVE_ENT", "CVE_MUN", "_area"], ascending=[True, True, False])
    inter = inter.drop_duplicates(subset=["CVE_ENT", "CVE_MUN"], keep="first")

    inter["cve_mun_full"] = inter["CVE_ENT"].astype(str).str.zfill(2) + inter["CVE_MUN"].astype(str).str.zfill(3)

    out_cols = ["cve_mun_full", "CVE_ENT", "CVE_MUN", "NOMGEO"] + region_cols
    out_cols = [c for c in out_cols if c in inter.columns]
    return inter[out_cols].copy()


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Asigna por interseccion espacial una region climatica INEGI a cada municipio "
            "y exporta metricas de extremos climaticos a nivel municipal."
        )
    )
    parser.add_argument(
        "--regiones-shp",
        default="mensuales/anomalias_regionales_tmaxmean.shp",
        help="Ruta relativa al shapefile regional de extremos climaticos.",
    )
    parser.add_argument(
        "--municipios-shp",
        default="data/temperatura_municipio/mun21gw.shp",
        help="Ruta relativa al shapefile municipal.",
    )
    parser.add_argument(
        "--output",
        default="data/resultados/tmax_anomalia_municipal.csv",
        help="CSV de salida a nivel municipal.",
    )
    args = parser.parse_args()

    regiones_path = PROJECT_ROOT / args.regiones_shp
    municipios_path = PROJECT_ROOT / args.municipios_shp
    output_path = PROJECT_ROOT / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not regiones_path.exists():
        raise FileNotFoundError(f"No existe shapefile regional: {regiones_path}")
    if not municipios_path.exists():
        raise FileNotFoundError(f"No existe shapefile municipal: {municipios_path}")

    regiones = gpd.read_file(regiones_path)
    municipios = gpd.read_file(municipios_path)

    if "CVE_ENT" not in municipios.columns or "CVE_MUN" not in municipios.columns:
        raise ValueError("El shapefile municipal no tiene CVE_ENT/CVE_MUN.")

    region_cols = choose_region_columns(regiones)
    if not region_cols:
        raise ValueError("No se encontraron columnas de metricas climaticas en la capa regional.")

    out = assign_region_to_municipio(municipios, regiones, region_cols)
    out.to_csv(output_path, index=False, encoding="utf-8-sig")

    print("Asignacion regional-municipal completada")
    print(f"  Regiones: {regiones_path}")
    print(f"  Municipios: {municipios_path}")
    print(f"  Salida: {output_path}")
    print(f"  Municipios con asignacion: {len(out)}")
    print(f"  Columnas exportadas: {len(out.columns)}")


if __name__ == "__main__":
    main()
