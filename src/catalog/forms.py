"""Formulários do catálogo."""

from django import forms

from src.catalog.models import SolicitacaoProduto


class SolicitacaoProdutoForm(forms.ModelForm):
    """Formulário para usuário solicitar cadastro de novo produto."""

    class Meta:
        model = SolicitacaoProduto
        fields = [
            "nome_produto",
            "marca",
            "categoria",
            "codigo_barras",
            "quantidade",
            "unidade_medida",
            "descricao",
        ]
        widgets = {
            "nome_produto": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: Arroz branco",
                }
            ),
            "marca": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: Tio João",
                }
            ),
            "categoria": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: Alimentos",
                }
            ),
            "codigo_barras": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: 7891234567890",
                }
            ),
            "quantidade": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: 1",
                    "step": "0.01",
                }
            ),
            "unidade_medida": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ex: kg, g, L, un",
                }
            ),
            "descricao": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Informações adicionais sobre o produto.",
                    "rows": 3,
                }
            ),
        }



from src.catalog.models import SolicitacaoProduto, AvaliacaoProduto


class AvaliacaoProdutoForm(forms.ModelForm):
    """Formulário para avaliar um produto cadastrado."""

    class Meta:
        model = AvaliacaoProduto
        fields = ["nota", "comentario"]
        widgets = {
            "nota": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "1",
                    "max": "5",
                    "placeholder": "De 1 a 5",
                }
            ),
            "comentario": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Deixe sua opinião sobre o produto (opcional).",
                    "rows": 3,
                }
            ),
        }