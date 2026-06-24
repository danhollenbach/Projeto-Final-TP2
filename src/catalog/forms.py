from django import forms
from .models import SolicitacaoProduto

class SolicitacaoProdutoForm(forms.ModelForm):
    class Meta:
        model = SolicitacaoProduto
        fields = ['nome_produto', 'marca', 'codigo_barras']
        widgets = {
            'nome_produto': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: Arroz Integral 1kg'}),
            'marca': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: Marca Fictícia'}),
            'codigo_barras': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: 7891234567890'}),
        }