import duckdb
import os

os.makedirs("tableau", exist_ok=True)

con = duckdb.connect("housing_analysis/dev.duckdb")

tables = {
    "mart_lakaspiac": "tableau/mart_lakaspiac.csv",
    "atlagár_regio_telepulestipus": "tableau/atlagár_regio_telepulestipus.csv",
    "atlagár_regio_epulettipus": "tableau/atlagár_regio_epulettipus.csv",
}

for table, path in tables.items():
    df = con.execute(f"SELECT * FROM {table}").df()
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"OK: {path} ({len(df)} sor)")

con.close()
print("\nKesz!")