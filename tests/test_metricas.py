"""Testes do módulo de métricas (KPIs)."""

import pytest
from src.analytics import calcular_kpis


class TestCalcularKpis:
    """Testes para calcular_kpis()."""

    def test_kpis_gerais_sem_filtros(self, df_vendas_falso):
        """KPIs gerais devem retornar soma, média e total corretos."""
        resultado = calcular_kpis(df_vendas_falso)

        assert "erro" not in resultado
        assert resultado["faturamento_total"] == pytest.approx(46.0)  # 10+3+15+6+6+6
        assert resultado["ticket_medio"] == pytest.approx(46.0 / 6)
        assert resultado["total_itens_vendidos"] == 10  # 2+1+3+1+2+1

    def test_kpis_com_filtro_de_item(self, df_vendas_falso):
        """Filtrar por Item deve restringir o cálculo."""
        resultado = calcular_kpis(df_vendas_falso, filtros={"Item": "Cappuccino"})

        assert resultado["faturamento_total"] == pytest.approx(25.0)  # 10 + 15
        assert resultado["total_itens_vendidos"] == 5  # 2 + 3

    def test_kpis_com_filtro_inexistente_retorna_erro(self, df_vendas_falso):
        """Filtro que não casa com nada deve retornar dict de erro."""
        resultado = calcular_kpis(
            df_vendas_falso, filtros={"Item": "ProdutoInexistente"}
        )

        assert "erro" in resultado
        assert "Nenhum registro" in resultado["erro"]

    def test_kpis_em_dataframe_vazio_retorna_erro(self, df_vendas_vazio):
        """DataFrame vazio deve retornar erro, não quebrar."""
        resultado = calcular_kpis(df_vendas_vazio)

        assert "erro" in resultado


class TestCalcularKpisEdgeCases:
    """Casos de borda para KPIs."""

    def test_multiplos_filtros_simultaneos(self, df_vendas_falso):
        """Dois filtros devem ser aplicados com AND lógico."""
        resultado = calcular_kpis(
            df_vendas_falso,
            filtros={"Item": "Espresso", "Location": "Centro"}
        )

        # IDs 2 e 5 são Espresso + Centro → 3 + 6 = 9
        assert resultado["faturamento_total"] == pytest.approx(9.0)
        assert resultado["total_itens_vendidos"] == 3  # 1 + 2
