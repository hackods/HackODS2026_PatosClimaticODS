import pypdf
import pandas as pd
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTADOS_DIR = PROJECT_ROOT / "data" / "resultados"
RESULTADOS_DIR.mkdir(parents=True, exist_ok=True)

pdf_candidates = [
    PROJECT_ROOT / "data" / "atlas" / "0000_Atlas_completo.pdf",
    PROJECT_ROOT / "data" / "0000_Atlas_completo.pdf",
    PROJECT_ROOT / "0000_Atlas_completo.pdf",
]

pdf_path = next((p for p in pdf_candidates if p.exists()), None)
if pdf_path is None:
    raise FileNotFoundError(
        "No se encontro 0000_Atlas_completo.pdf. Colocalo en data/atlas/, data/ o raiz del proyecto."
    )

nombre_archivo = RESULTADOS_DIR / "atlas_datos_unificado.xlsx"

# Configuración con páginas del índice (el script resta 1 automáticamente)
mapeo_entidades = {
    "01": {"edu": ["54"], "inf": ["55"]},
    "02": {"edu": ["68"], "inf": ["69"]},
    "03": {"edu": ["82"], "inf": ["83"]},
    "04": {"edu": ["96"], "inf": ["97"]},
    "05": {"edu": ["110"], "inf": ["111"]},
    "06": {"edu": ["124"], "inf": ["125"]},
    "07": {"edu": ["138", "139", "140"], "inf": ["141", "142", "143", "144", "145"]},
    "08": {"edu": ["157", "158"], "inf": ["159", "160", "161"]},
    "09": {"edu": ["173"], "inf": ["174", "175"]},
    "10": {"edu": ["187", "188", "189", "190"], "inf": ["188", "189", "190"]},
    "11": {"edu": ["202", "203"], "inf": ["204", "205", "206"]},
    "12": {"edu": ["218", "219", "220"], "inf": ["221", "222", "223", "224"]},
    "13": {"edu": ["236", "237", "238"], "inf": ["239", "240", "241", "242"]},
    "14": {"edu": ["254", "255", "256", "257"], "inf": ["258", "259", "260", "261", "262"]},
    "15": {"edu": ["274", "275", "276"], "inf": ["277", "278", "279", "280", "281"]},
    "16": {"edu": ["293", "294", "295"], "inf": ["296", "297", "298", "299"]},
    "17": {"edu": ["311"], "inf": ["312", "313"]},
    "18": {"edu": ["325", "326", "327"], "inf": ["326", "327"]},
    "19": {"edu": ["339", "340"], "inf": ["341", "342", "343"]},
    "20": {"edu": ["355", "356", "357", "358", "359", "360", "361", "362", "363", "364", "365", "366", "367", "368", "369", "370", "371", "372"], "inf": ["373", "374", "375", "376", "377", "378", "379", "380", "381", "382", "383", "384", "385", "386", "387", "388", "389", "390", "391", "392", "393"]},
    "21": {"edu": ["405", "406", "407", "408", "409", "410"], "inf": ["411", "412", "413", "414", "415", "416", "417"]},
    "22": {"edu": ["429"], "inf": ["430", "431"]},
    "23": {"edu": ["443"], "inf": ["444", "445"]},
    "24": {"edu": ["457", "458"], "inf": ["459", "460", "461"]},
    "25": {"edu": ["473"], "inf": ["474", "475"]},
    "26": {"edu": ["487", "488"], "inf": ["489", "490", "491"]},
    "27": {"edu": ["503"], "inf": ["504", "505"]},
    "28": {"edu": ["517"], "inf": ["518", "519", "520"]},
    "29": {"edu": ["532", "533"], "inf": ["534", "535", "536"]},
    "30": {"edu": ["548", "549", "550", "551", "552"], "inf": ["553", "554", "555", "556", "557", "558", "559"]},
    "31": {"edu": ["571", "572", "573"], "inf": ["574", "575", "576", "577"]},
    "32": {"edu": ["589", "590"], "inf": ["591", "592", "593"]},
}

def procesar_atlas():
    datos_totales = []
    reader = pypdf.PdfReader(str(pdf_path))

    for ent_id, tipos in mapeo_entidades.items():
        for tipo, pags in tipos.items():
            for p_str in pags:
                # Ajuste automático de página
                idx_pag = int(p_str) - 2
                if ent_id == "32" and (idx_pag < 0 or idx_pag >= len(reader.pages)):
                    continue
                page = reader.pages[idx_pag]
                lineas = page.extract_text().split('\n')
                
                municipio_pendiente = None
                
                for linea in lineas:
                    linea = linea.strip()
                    if not linea or "Fuente:" in linea: continue

                    # Detectar inicio de municipio por los 3 dígitos
                    match_clave = re.match(r'^(\d{3})\s+(.*)', linea)
                    
                    if match_clave:
                        clave = match_clave.group(1)
                        cvegeo = f"{ent_id}{clave}"
                        resto = match_clave.group(2).strip()
                        
                        # Buscar si hay números en esa misma línea
                        # Corta en el primer número que encuentre después del nombre
                        match_datos = re.search(r'(.+?)\s+(\d[\d\.\s,]+(?:Muy bajo|Bajo|Medio|Alto|Muy alto)?)', resto)
                        
                        if match_datos:
                            valores = match_datos.group(2).split()
                            datos_totales.append([cvegeo, tipo] + valores)
                            municipio_pendiente = None
                        else:
                            # Si no hay números, guardamos la CVEGEO y esperamos a la línea de abajo
                            municipio_pendiente = {"cvegeo": cvegeo}
                    
                    elif municipio_pendiente:
                        # Intentar capturar los números en esta línea (caso nombres largos)
                        match_solo_datos = re.search(r'(\d[\d\.\s,]+(?:Muy bajo|Bajo|Medio|Alto|Muy alto)?)', linea)
                        if match_solo_datos:
                            valores = match_solo_datos.group(1).split()
                            datos_totales.append([municipio_pendiente["cvegeo"], tipo] + valores)
                            municipio_pendiente = None

    # Limpieza de etiquetas de marginación (une "Muy" con "bajo")
    for fila in datos_totales:
        if "Muy" in fila:
            idx = fila.index("Muy")
            if idx + 1 < len(fila):
                fila[idx] = f"Muy {fila[idx+1]}"
                fila.pop(idx+1)

    # Definir columnas máximas (Infraestructura tiene 8 datos, Educación 7)
    columnas = ["CVEGEO", "Tipo", "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8"]
    datos_normalizados = []
    for fila in datos_totales:
        fila = list(fila)
        if len(fila) > len(columnas):
            fila = fila[:len(columnas)]
        elif len(fila) < len(columnas):
            fila = fila + [None] * (len(columnas) - len(fila))
        datos_normalizados.append(fila)

    df = pd.DataFrame(datos_normalizados, columns=columnas)
    
    # Sobrescribe el archivo Excel
    df.to_excel(str(nombre_archivo), index=False)
    print(f"Procesado finalizado. Archivo '{nombre_archivo}' actualizado.")

procesar_atlas()