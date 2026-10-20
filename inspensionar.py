
import pandas as pd
from pathlib import Path

arquivo = Path(
    "microdados_censo_escolar_2025_v2/dados/"
    "Tabela_Escola_2025_V2.csv"
)

if not arquivo.exists():
    raise FileNotFoundError(f"Arquivo não encontrado: {arquivo}")

print("Lendo a tabela completa...")

# Lê somente as colunas necessárias para esta análise.
colunas = [
    "CO_ENTIDADE",
    "NO_UF",
    "SG_UF",
    "NO_MUNICIPIO",
    "TP_DEPENDENCIA",
    "TP_LOCALIZACAO",
]

df = pd.read_csv(
    arquivo,
    sep=";",
    encoding="latin1",
    usecols=colunas,
    dtype={
        "CO_ENTIDADE": "string",
        "SG_UF": "string",
    },
    low_memory=False
)

print("\n=== RESUMO GERAL ===")
print(f"Total de registros: {len(df):,}")
print(f"Códigos de escola únicos: {df['CO_ENTIDADE'].nunique():,}")
print(f"Códigos ausentes: {df['CO_ENTIDADE'].isna().sum():,}")
print(
    "Códigos duplicados em registros: "
    f"{df['CO_ENTIDADE'].duplicated().sum():,}"
)

print("\n=== ESCOLAS POR ESTADO ===")
print(
    df.groupby(["SG_UF", "NO_UF"], dropna=False)
    .size()
    .sort_values(ascending=False)
    .to_string()
)

print("\n=== ESCOLAS POR DEPENDÊNCIA ADMINISTRATIVA ===")
print(df["TP_DEPENDENCIA"].value_counts(dropna=False).to_string())

print("\n=== ESCOLAS POR LOCALIZAÇÃO ===")
print(df["TP_LOCALIZACAO"].value_counts(dropna=False).to_string())

print("\n=== CINCO MUNICÍPIOS COM MAIS REGISTROS ===")
print(df["NO_MUNICIPIO"].value_counts().head(5).to_string())

print("\n=== REGISTROS SEM IDENTIFICAÇÃO GEOGRÁFICA ===")

sem_uf = df[df["SG_UF"].isna()]

if sem_uf.empty:
    print("Nenhum registro sem UF.")
else:
    print(sem_uf.to_string(index=False))

print("\n=== VERIFICAÇÃO DOS CÓDIGOS INEP ===")

print(
    "Todos os códigos estão preenchidos:",
    df["CO_ENTIDADE"].notna().all()
)

print(
    "Todos os códigos são únicos:",
    df["CO_ENTIDADE"].is_unique
)
