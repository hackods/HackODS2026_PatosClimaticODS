from pathlib import Path
import argparse
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INFIED_DIR = PROJECT_ROOT / "data" / "INFIED"
RESULTADOS_DIR = PROJECT_ROOT / "data" / "resultados"


def read_csv_with_fallback(path: Path) -> pd.DataFrame:
    encodings = ["utf-8", "utf-8-sig", "latin-1"]
    last_err = None
    for enc in encodings:
        try:
            return pd.read_csv(path, encoding=enc)
        except Exception as exc:
            last_err = exc
    raise RuntimeError(f"No se pudo leer {path} con codificaciones comunes: {last_err}")


def normalize_cct(series: pd.Series) -> pd.Series:
    return (
        series.astype(str)
        .str.upper()
        .str.strip()
        .replace({"NAN": pd.NA, "": pd.NA})
    )


def normalize_code(series: pd.Series, width: int) -> pd.Series:
    digits = series.astype(str).str.replace(r"\D", "", regex=True)
    digits = digits.replace({"": pd.NA, "NAN": pd.NA})
    return digits.str.zfill(width).str[-width:]


def numeric_ratio(series: pd.Series) -> float:
    digits = series.astype(str).str.replace(r"\D", "", regex=True)
    valid = digits.replace({"": pd.NA, "NAN": pd.NA}).notna().sum()
    total = len(series)
    return (valid / total) if total else 0.0


def choose_geo_code_columns(df_911: pd.DataFrame) -> tuple[str, str]:
    candidate_pairs = [
        ("ENTIDAD", "MUNICIPIO"),
        ("C_ENTIDAD", "C_MUNICIPIO"),
        ("N_ENTIDAD", "N_MUNICIPI"),
    ]

    available_pairs = [
        (ent_col, mun_col)
        for ent_col, mun_col in candidate_pairs
        if ent_col in df_911.columns and mun_col in df_911.columns
    ]

    if not available_pairs:
        raise ValueError(
            "No se encontraron columnas de códigos de entidad/municipio en el archivo 911."
        )

    best_pair = None
    best_score = -1.0
    for ent_col, mun_col in available_pairs:
        score = numeric_ratio(df_911[ent_col]) + numeric_ratio(df_911[mun_col])
        if score > best_score:
            best_pair = (ent_col, mun_col)
            best_score = score

    assert best_pair is not None
    return best_pair


def build_911_lookup(df_911: pd.DataFrame) -> pd.DataFrame:
    required = ["CLAVECCT"]
    missing = [c for c in required if c not in df_911.columns]
    if missing:
        raise ValueError(f"El archivo 911 no contiene columnas requeridas: {missing}")

    ent_col, mun_col = choose_geo_code_columns(df_911)

    # Detectar columna de sostenimiento (público/privado)
    sostenimiento_col = None
    for col_candidate in ["CONTROL", "sostenimiento", "SOSTENIMIENTO", "SUBCONTROL"]:
        if col_candidate in df_911.columns:
            sostenimiento_col = col_candidate
            break

    # Construir lista de columnas a incluir
    lookup_cols = ["CLAVECCT", ent_col, mun_col]
    if sostenimiento_col:
        lookup_cols.append(sostenimiento_col)

    lookup = df_911[lookup_cols].copy()
    lookup["cct_norm"] = normalize_cct(lookup["CLAVECCT"])
    lookup["cve_ent"] = normalize_code(lookup[ent_col], 2)
    lookup["cve_mun"] = normalize_code(lookup[mun_col], 3)
    lookup["cve_mun_full"] = lookup["cve_ent"] + lookup["cve_mun"]

    lookup = lookup.dropna(subset=["cct_norm", "cve_ent", "cve_mun"])
    
    # Si existe columna de sostenimiento, priorizar PRIVADO sobre PÚBLICO en duplicados
    if sostenimiento_col:
        # Mapear PRIVADO a 0, PÚBLICO a 1 para que PRIVADO sea "primero" (menor valor)
        lookup["_sostenimiento_order"] = lookup[sostenimiento_col].map(
            lambda x: 0 if x == "PRIVADO" else (1 if x == "PÚBLICO" else 2)
        )
        lookup = lookup.sort_values("_sostenimiento_order").drop_duplicates(
            subset=["cct_norm"], keep="first"
        )
        lookup = lookup.drop(columns=["_sostenimiento_order"])
    else:
        lookup = lookup.drop_duplicates(subset=["cct_norm"], keep="first")

    # Retornar con sostenimiento si existe
    return_cols = ["cct_norm", "cve_ent", "cve_mun", "cve_mun_full"]
    if sostenimiento_col:
        return_cols.append(sostenimiento_col)

    return lookup[return_cols]


def normalize_municipal_key(series: pd.Series) -> pd.Series:
    return normalize_code(series, 5)


def flag_contains(series: pd.Series, pattern: str) -> pd.Series:
    return series.astype(str).str.contains(pattern, case=False, regex=True, na=False)


def aggregate_infied_to_municipio(df_school: pd.DataFrame) -> pd.DataFrame:
    df = df_school.copy()
    df = df[df["cve_mun_full"].notna()].copy()

    if df.empty:
        return pd.DataFrame(columns=[
            "cve_mun_full",
            "escuelas_infied",
            "luz_con_pct_infied",
            "agua_red_pct_infied",
            "bebederos_con_pct_infied",
            "techumbre_con_pct_infied",
            "ambito_urbano_pct_infied",
            "ambito_rural_pct_infied",
            "ambito_predominante_infied",
            "control_predominante_infied",
        ])

    df["cve_mun_full"] = normalize_municipal_key(df["cve_mun_full"])

    df["luz_con_flag"] = flag_contains(df["CON_LUZ"], r"\bCON\s+LUZ\b") if "CON_LUZ" in df.columns else False
    df["agua_red_flag"] = flag_contains(df["ALIMENTACION_AGUA"], r"\bRED\s+MUNICIPAL\b") if "ALIMENTACION_AGUA" in df.columns else False
    df["bebederos_con_flag"] = flag_contains(df["BEBEDEROS"], r"\bCON\s+BEBEDERO\b") if "BEBEDEROS" in df.columns else False
    df["techumbre_con_flag"] = flag_contains(df["CUBIERTA_TECHUMBRE_EXT"], r"\bCON\s+TECHUMBRE\b") if "CUBIERTA_TECHUMBRE_EXT" in df.columns else False
    df["ambito_urbano_flag"] = flag_contains(df["AMBITO"], r"\bURBANO\b") if "AMBITO" in df.columns else False
    df["ambito_rural_flag"] = flag_contains(df["AMBITO"], r"\bRURAL\b") if "AMBITO" in df.columns else False

    grouped = df.groupby("cve_mun_full", as_index=False).agg(
        escuelas_infied=("CCT", "count"),
        luz_con_pct_infied=("luz_con_flag", "mean"),
        agua_red_pct_infied=("agua_red_flag", "mean"),
        bebederos_con_pct_infied=("bebederos_con_flag", "mean"),
        techumbre_con_pct_infied=("techumbre_con_flag", "mean"),
        ambito_urbano_pct_infied=("ambito_urbano_flag", "mean"),
        ambito_rural_pct_infied=("ambito_rural_flag", "mean"),
    )

    pct_cols = [
        "luz_con_pct_infied",
        "agua_red_pct_infied",
        "bebederos_con_pct_infied",
        "techumbre_con_pct_infied",
        "ambito_urbano_pct_infied",
        "ambito_rural_pct_infied",
    ]
    for col in pct_cols:
        grouped[col] = (grouped[col] * 100).round(2)

    if "AMBITO" in df.columns:
        ambito_mode = (
            df.groupby("cve_mun_full")["AMBITO"]
            .agg(lambda s: s.mode().iat[0] if not s.mode().empty else pd.NA)
            .rename("ambito_predominante_infied")
            .reset_index()
        )
        grouped = grouped.merge(ambito_mode, on="cve_mun_full", how="left")
    else:
        grouped["ambito_predominante_infied"] = pd.NA

    if "CONTROL" in df.columns:
        control_mode = (
            df.groupby("cve_mun_full")["CONTROL"]
            .agg(lambda s: s.mode().iat[0] if not s.mode().empty else pd.NA)
            .rename("control_predominante_infied")
            .reset_index()
        )
        grouped = grouped.merge(control_mode, on="cve_mun_full", how="left")
    else:
        grouped["control_predominante_infied"] = pd.NA

    return grouped


def select_infied_columns(df_infied: pd.DataFrame) -> pd.DataFrame:
    base_cols = [
        "ANIO",
        "ENTIDAD_FEDERATIVA",
        "MUNICIPIO",
        "LOCALIDAD",
        "CCT",
        "NOMBRE",
        "AMBITO",
        "NIVEL",
    ]

    # Servicios e infraestructura prioritaria (incluye techumbre)
    service_cols = [
        "ALIMENTACION_AGUA",
        "BEBEDEROS",
        "DESCARGA_AGUA_RESIDUAL",
        "CON_LUZ",
        "TELEFONIA_FIJA",
        "INTERNET",
        "NIVEL_ACCESIBILIDAD",
        "WC_ALUMNOS",
        "WC_ALUMNAS",
        "WC_DISCAPACITADOS",
        "WC_DOCENTES",
        "CONDICION_FIS_WC",
        "NUM_AULAS",
        "ESTRUCTURAS_ATIPICAS",
        "NUM_EDIFICIOS",
        "PLAN_PROTECCION_CIVIL",
        "CANCHA_DEPORTIVA",
        "CUBIERTA_TECHUMBRE_EXT",
    ]

    # Mobiliario/activos que se excluyen por solicitud
    mobiliario_excluir = {
        "MESA_BINARIA",
        "MESA",
        "SILLA",
        "SILLA_PALETA",
        "MESA_BANCO",
        "MESA_BANCO_BINARIO",
        "PIZARRON",
        "COMPUTADORA",
        "LAPTOP",
    }

    present_base = [c for c in base_cols if c in df_infied.columns]
    present_service = [c for c in service_cols if c in df_infied.columns and c not in mobiliario_excluir]

    selected = present_base + present_service
    if "CCT" not in selected:
        raise ValueError("El archivo INIFED no contiene la columna CCT.")

    return df_infied[selected].copy()


def procesar_infied(
    infied_file: str,
    base911_file: str,
    output_file: str,
) -> Path:
    RESULTADOS_DIR.mkdir(parents=True, exist_ok=True)

    infied_path = INFIED_DIR / infied_file
    base911_path = INFIED_DIR / base911_file
    output_path = RESULTADOS_DIR / output_file

    if not infied_path.exists():
        raise FileNotFoundError(f"No existe archivo INIFED: {infied_path}")
    if not base911_path.exists():
        raise FileNotFoundError(f"No existe archivo 911: {base911_path}")

    df_infied_raw = read_csv_with_fallback(infied_path)
    df_911_raw = read_csv_with_fallback(base911_path)

    df_infied = select_infied_columns(df_infied_raw)
    df_infied["cct_norm"] = normalize_cct(df_infied["CCT"])

    ent_col, mun_col = choose_geo_code_columns(df_911_raw)
    print(f"Columnas de clave geográfica detectadas en 911: {ent_col} (entidad), {mun_col} (municipio)")
    lookup_911 = build_911_lookup(df_911_raw)

    df_out = df_infied.merge(lookup_911, on="cct_norm", how="left")
    df_out = df_out.drop(columns=["cct_norm"])

    total = len(df_out)
    matched = df_out["cve_mun_full"].notna().sum()
    unmatched = total - matched
    match_rate = (matched / total * 100) if total else 0.0

    ordered_cols = [
        "cve_ent",
        "cve_mun",
        "cve_mun_full",
        "AMBITO",
    ]
    # Agregar sostenimiento si existe en el output
    if "CONTROL" in df_out.columns:
        ordered_cols.insert(4, "CONTROL")
    remaining = [c for c in df_out.columns if c not in ordered_cols]
    df_out = df_out[[c for c in ordered_cols if c in df_out.columns] + remaining]

    df_out.to_csv(output_path, index=False, encoding="utf-8-sig")

    unmatched_path = RESULTADOS_DIR / (Path(output_file).stem + "_cct_sin_match.csv")
    df_out[df_out["cve_mun_full"].isna()].to_csv(unmatched_path, index=False, encoding="utf-8-sig")

    # Agregar INIFED a nivel municipal
    df_infied_municipio = aggregate_infied_to_municipio(df_out)
    infied_mun_path = RESULTADOS_DIR / "infied_municipio.csv"
    df_infied_municipio.to_csv(infied_mun_path, index=False, encoding="utf-8-sig")

    print("Procesamiento INIFED completado")
    print(f"  INIFED: {infied_path}")
    print(f"  911: {base911_path}")
    print(f"  Salida: {output_path}")
    print(f"  Total registros: {total}")
    print(f"  Con cve_mun_full: {matched}")
    print(f"  Sin match CCT: {unmatched}")
    print(f"  Match rate: {match_rate:.2f}%")
    print(f"  Reporte sin match: {unmatched_path}")
    print(f"  INIFED municipal: {infied_mun_path}")

    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Procesa INIFED + 911 por CCT, estandariza claves (2+3 dígitos) "
            "y genera salida en data/resultados."
        )
    )
    parser.add_argument(
        "--infied-file",
        default="INIFED_2020-2022_CSV.csv",
        help="Nombre del archivo INIFED dentro de data/INFIED",
    )
    parser.add_argument(
        "--base911-file",
        default="ESTANDAR_BASICA_I2324.csv",
        help="Nombre del archivo 911 dentro de data/INFIED",
    )
    parser.add_argument(
        "--output-file",
        default="infied_servicios_con_clave_municipio.csv",
        help="Nombre del CSV de salida en data/resultados",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    procesar_infied(args.infied_file, args.base911_file, args.output_file)


if __name__ == "__main__":
    main()
