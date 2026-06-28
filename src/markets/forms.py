"""Fomulário para mercados"""

from django import forms
from src.markets.models import Mercado

class MercadoForm (forms.ModelForm):
    class Meta:
        model = Mercado
        fields = ["nome", "endereco", "latitude", "longitude"]
        widgets = {
            "nome": forms.TextInput(
                attrs = {"class": "form-control", "placeholder":"Ex: Supermercado Êta"}
            ),
            "endereco": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Ex: Asa Norte, Brasília"}
            ),
            "latitude": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.000001"}
            ),
            "longitude": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.000001"}
            ),
        }