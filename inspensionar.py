
import pandas as pd
from pathlib import Path

arquivo = Path("microdados_censo_escolar_2025_v2/dados/Tabela_Escola_2025_V2.csv")

# Lê somente as primeiras linhas
df = pd.read_csv(
    arquivo,
    sep=";",
    encoding="latin1",
    nrows=5,
    low_memory=False
)

print("\n=== COLUNAS DA TABELA ===")
print(df.columns.tolist())

print("\n=== PRIMEIRAS 5 LINHAS ===")
print(df.to_string(index=False))

print("\n=== QUANTIDADE DE COLUNAS ===")
print(len(df.columns))
