
from rest_framework import serializers

from .models import School


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = [
            "codigo_inep",
            "nome",
            "uf",
            "municipio",
            "dependencia_administrativa",
            "localizacao",
        ]

        
