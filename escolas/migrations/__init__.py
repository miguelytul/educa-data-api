
from pathlib import Path

import pandas as pd
from django.core.management.base import BaseCommand, CommandError

from escolas.models import School


class Command(BaseCommand):
    help = "Importa escolas do Censo Escolar para o banco de dados"

    def handle(self, *args, **options):
        arquivo = (
            Path("microdados_censo_escolar_2025_v2")
            / "dados"
            / "Tabela_Escola_2025_V2.csv"
        )

        if not arquivo.exists():
            raise CommandError(
                f"Arquivo não encontrado: {arquivo.resolve()}"
            )

        colunas = [
            "CO_ENTIDADE",
            "NO_ENTIDADE",
            "SG_UF",
            "NO_MUNICIPIO",
            "TP_DEPENDENCIA",
            "TP_LOCALIZACAO",
        ]

        total = 0

        try:
            blocos = pd.read_csv(
                arquivo,
                sep=";",
                encoding="latin1",
                usecols=colunas,
                dtype={"CO_ENTIDADE": "string"},
                chunksize=10_000,
            )

            for bloco in blocos:
                escolas = []

                for row in bloco.itertuples(index=False):
                    if pd.isna(row.CO_ENTIDADE):
                        continue

                    escolas.append(
                        School(
                            codigo_inep=str(row.CO_ENTIDADE),
                            nome=(
                                str(row.NO_ENTIDADE)
                                if not pd.isna(row.NO_ENTIDADE)
                                else "Nome não informado"
                            ),
                            uf=(
                                str(row.SG_UF)
                                if not pd.isna(row.SG_UF)
                                else None
                            ),
                            municipio=(
                                str(row.NO_MUNICIPIO)
                                if not pd.isna(row.NO_MUNICIPIO)
                                else None
                            ),
                            dependencia_administrativa=(
                                int(row.TP_DEPENDENCIA)
                                if not pd.isna(row.TP_DEPENDENCIA)
                                else None
                            ),
                            localizacao=(
                                int(row.TP_LOCALIZACAO)
                                if not pd.isna(row.TP_LOCALIZACAO)
                                else None
                            ),
                        )
                    )

                School.objects.bulk_create(
                    escolas,
                    batch_size=1000,
                    ignore_conflicts=True,
                )

                total += len(escolas)
                self.stdout.write(f"Registros processados: {total}")

        except ValueError as erro:
            raise CommandError(
                f"Erro ao ler as colunas do CSV: {erro}"
            ) from erro

        self.stdout.write(
            self.style.SUCCESS(
                f"Importação finalizada. Registros processados: {total}"
            )
        )
