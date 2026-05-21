import pandas as pd
import os

RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
os.makedirs(PROCESSED_DIR, exist_ok=True)

# 1. Arindex negyedevenként (lak0036)
df_idx = pd.read_excel(f"{RAW_DIR}/lak0036_arindex_negyedev.xlsx", sheet_name=0, header=None)
df_idx.columns = df_idx.iloc[1].tolist()
df_idx = df_idx.iloc[3:].reset_index(drop=True)
df_idx.columns = ["ev", "negyedev", "osszetetes_haszn", "tiszta_haszn", "teljes_haszn",
                  "osszetetes_uj", "tiszta_uj", "teljes_uj", "osszevont_index"]
df_idx["ev"] = df_idx["ev"].ffill()
df_idx["ev"] = df_idx["ev"].astype(str).str.replace(".", "").str.strip()
df_idx["negyedev"] = df_idx["negyedev"].astype(str).str.strip()
df_idx["idoszak"] = df_idx["ev"] + " " + df_idx["negyedev"]
df_idx.to_csv(f"{PROCESSED_DIR}/arindex_negyedev.csv", index=False, encoding="utf-8-sig")
print("OK: arindex_negyedev.csv", df_idx.shape)

def wide_to_long(filepath, col2_name):
    df = pd.read_excel(filepath, sheet_name=0, header=None)

    # Negyedev nevek a 2. sorban, 3. oszloptol
    negyedevek = df.iloc[1, 2:].tolist()

    # Lakastipus sorok: col0 nem NaN, col1 NaN (pl. "Hasznalt lakasok")
    lakastipus_mask = df.iloc[:, 1].isna() & df.iloc[:, 0].notna()

    # Lakastipus forward fill
    lakastipus_col = df.iloc[:, 0].where(lakastipus_mask).ffill()

    # Adatsorok: col1 nem NaN es col0 nem a fejlec
    data_mask = df.iloc[:, 1].notna() & (df.iloc[:, 0] != "Régió")
    df_data = df[data_mask].copy()
    df_data["lakastipus"] = lakastipus_col[data_mask].values

    # Wide to long
    result_rows = []
    for _, row in df_data.iterrows():
        regio = row.iloc[0]
        col2 = row.iloc[1]
        lakastipus = row["lakastipus"]
        for i, negyedev in enumerate(negyedevek):
            val = row.iloc[i + 2]
            result_rows.append({
                "regio": regio,
                col2_name: col2,
                "lakastipus": lakastipus,
                "idoszak": str(negyedev).strip(),
                "atlagár_mFt": val if str(val) != "nan" else None
            })
    return pd.DataFrame(result_rows)

# 2. Atlagár regio + telepulestipus (lak0051)
df_tel = wide_to_long(
    f"{RAW_DIR}/lak0051_atlagár_regio_telepulestipus.xlsx",
    "telepulestipus"
)
df_tel.to_csv(f"{PROCESSED_DIR}/atlagár_regio_telepulestipus.csv", index=False, encoding="utf-8-sig")
print("OK: atlagár_regio_telepulestipus.csv", df_tel.shape)
print(df_tel.head(6).to_string())

# 3. Atlagár regio + epulettipus (lak0054)
df_ep = wide_to_long(
    f"{RAW_DIR}/lak0054_atlagár_regio_epulettipus.xlsx",
    "epulettipus"
)
df_ep.to_csv(f"{PROCESSED_DIR}/atlagár_regio_epulettipus.csv", index=False, encoding="utf-8-sig")
print("OK: atlagár_regio_epulettipus.csv", df_ep.shape)
print(df_ep.head(6).to_string())

print("\nKesz!")