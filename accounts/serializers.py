from rest_framework import serializers
from .models import Account
from rest_framework.validators import UniqueValidator


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_superuser",
            "is_active",
        ]
        extra_kwargs = {
            "is_superuser": {"read_only": True},
            "password": {"write_only": True},
            "is_seller": {"required": True},
            "username": {
                "validators": [
                    UniqueValidator(
                        queryset=Account.objects.all(),
                        message="username already exists",
                    )
                ]
            },
        }

    is_active = serializers.BooleanField(default=True)
    # duas formas de resolver o problema de is active setado pra false
    # em ambiente de testes
    # ou da forma da linha 34 sobscrevendo a model e colocando serializer 
    # como default true
    # ou subscrevendo o validated_data no metodo de create
    # do jeito que esta comentado na parte abaixo
    
    def create(self, validated_data: dict) -> Account:
        # validated_data['is_active'] = True
        return Account.objects.create_user(**validated_data)
