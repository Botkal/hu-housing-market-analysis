import requests
import os

RAW_DIR = "data/raw"
os.makedirs(RAW_DIR, exist_ok=True)

DATASETS = {
    "lak0036_arindex_negyedev": "https://www.ksh.hu/stadat_files/lak/hu/lak0036.xlsx",
    "lak0051_atlagár_regio_telepulestipus": "https://www.ksh.hu/stadat_files/lak/hu/lak0051.xlsx",
    "lak0054_atlagár_regio_epulettipus": "https://www.ksh.hu/stadat_files/lak/hu/lak0054.xlsx",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

for name, url in DATASETS.items():
    print(f"Letöltés: {name}...")
    response = requests.get(url, headers=headers, timeout=30)
    if response.status_code == 200:
        filepath = os.path.join(RAW_DIR, f"{name}.xlsx")
        with open(filepath, "wb") as f:
            f.write(response.content)
        print(f"  ✓ Mentve: {filepath}")
    else:
        print(f"  ✗ Hiba: {response.status_code}")

print("\nKész!")
