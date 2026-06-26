# Generated manually to align SolicitacaoProduto with the user request flow.

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("catalog", "0002_solicitacaoproduto"),
    ]

    operations = [
        migrations.RenameField(
            model_name="solicitacaoproduto",
            old_name="nome",
            new_name="nome_produto",
        ),
        migrations.AddField(
            model_name="solicitacaoproduto",
            name="usuario",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="solicitacoes_produto",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Usuário",
            ),
        ),
    ]
