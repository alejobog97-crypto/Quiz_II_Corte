import os
import pandas as pd

DATA_PATH = "data/raw/encuestas_demo.csv"
OUT_DIR = "reports"
OUT_FILE = os.path.join(OUT_DIR, "quiz_result.xlsx")

# --- Helpers ---
def ensure_dirs():
    os.makedirs(OUT_DIR, exist_ok=True)

def load_data(path: str) -> pd.DataFrame:
    """TODO(1): Carga el CSV y retorna un DataFrame."""
    df = pd.read_csv(path)
    return df

def clean_columns(df: pd.DataFrame) -> pd.DataFrame:
    """TODO(2): Copia con columnas en minúsculas y espacios -> '_'."""
    out = df.copy()
    out.columns = [str(c).strip().lower().replace(" ", "_") for c in out.columns]
    return out

def dist_departamento(df: pd.DataFrame) -> pd.DataFrame:
    """TODO(3): Conteo por 'departamento' (desc), columna 'count'."""
    return (
        df["departamento"]
        .value_counts(dropna=False)
        .rename_axis("departamento")
        .reset_index(name="count")
        .sort_values("count", ascending=False, ignore_index=True)
    )

def top5_municipio(df: pd.DataFrame) -> pd.DataFrame:
    """TODO(4): Top 5 municipios por cantidad (desc)."""
    t = (
        df["municipio"]
        .value_counts(dropna=False)
        .rename_axis("municipio")
        .reset_index(name="count")
    )
    return t.nlargest(5, "count").reset_index(drop=True)

def gasto_promedio_por_servicio(df: pd.DataFrame) -> pd.DataFrame:
    """TODO(5): Promedio de 'gasto_estimado' por 'servicio' (desc)."""
    tmp = df.copy()
    tmp["gasto_estimado"] = pd.to_numeric(tmp["gasto_estimado"], errors="coerce")
    out = (
        tmp.groupby("servicio", dropna=False)["gasto_estimado"]
        .mean()
        .reset_index()
        .rename(columns={"gasto_estimado": "gasto promedio"})
        .sort_values("gasto promedio", ascending=False, ignore_index=True)
    )
    return out

def pivot_municipio_x_punto(df: pd.DataFrame) -> pd.DataFrame:
    """TODO(6): Conteos municipio x punto_atencion como tabla dinámica."""
    pt = pd.pivot_table(
        df,
        index="municipio",
        columns="punto_atencion",
        values="id",
        aggfunc="count",
        fill_value=0
    )
    return pt.reset_index()

def export_excel(tables: dict, out_file: str):
    """TODO(7): Exporta a Excel con una hoja por cada clave del dict."""
    with pd.ExcelWriter(out_file, engine="openpyxl") as xw:
        for sheet, tdf in tables.items():
            tdf.to_excel(xw, sheet_name=sheet, index=False)

# --- Main ---
def main():
    ensure_dirs()
    df = load_data(DATA_PATH)
    df = clean_columns(df)
    t1 = dist_departamento(df)
    t2 = top5_municipio(df)
    t3 = gasto_promedio_por_servicio(df)
    t4 = pivot_municipio_x_punto(df)

    tables = {
        "dist_departamento": t1,
        "top5_municipio": t2,
        "gasto_promedio_por_servicio": t3,
        "pivot_municipio_x_punto": t4,
    }

    export_excel(tables, OUT_FILE)
    print(f"[OK] Entregable generado: {os.path.abspath(OUT_FILE)}")

if __name__ == "__main__":
    main()
