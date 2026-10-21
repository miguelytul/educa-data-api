
from django.db import models


class School(models.Model):
    codigo_inep = models.CharField(
        max_length=8,
        unique=True,
    )
    nome = models.CharField(max_length=255)
    uf = models.CharField(max_length=2, null=True, blank=True)
    municipio = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    dependencia_administrativa = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )
    localizacao = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "escolas"
        ordering = ["nome"]

    def __str__(self):
        return f"{self.nome} ({self.codigo_inep})"
