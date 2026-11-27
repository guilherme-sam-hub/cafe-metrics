"""
Estruturas de dados auxiliares para a camada de analytics.
"""

from __future__ import annotations

from typing import Any, List, Tuple


class PilhaRelatorios:
    """
    Pilha (LIFO) que mantém o histórico de relatórios gerados pelo menu,
    permitindo ao usuário "voltar" ao relatório anterior.

    Justificativa: a pilha modela a navegação "voltar" — o último relatório
    gerado é o primeiro a ser recuperado (LIFO).

    Observações de contrato:
      - ``desempilhar()`` em pilha vazia retorna ``None`` (não levanta exceção).
      - ``listar()`` devolve os títulos do MAIS RECENTE para o MAIS ANTIGO.

    Complexidade: empilhar/desempilhar/topo/vazia/limpar = O(1); listar/len = O(n).
    """

    def __init__(self) -> None:
        self._dados: List[Tuple[str, Any]] = []

    def empilhar(self, titulo: str, resultado: Any) -> None:
        """Adiciona um relatório ao topo da pilha. O(1) amortizado."""
        self._dados.append((titulo, resultado))

    def desempilhar(self) -> Tuple[str, Any] | None:
        """
        Remove e retorna o relatório do topo.
        Retorna ``None`` se a pilha estiver vazia (não levanta exceção).
        """
        if self._dados:
            return self._dados.pop()
        return None

    def topo(self) -> Tuple[str, Any] | None:
        """Retorna o relatório do topo sem removê-lo, ou ``None`` se vazia."""
        return self._dados[-1] if self._dados else None

    def vazia(self) -> bool:
        """``True`` se não há relatórios na pilha."""
        return not self._dados

    def limpar(self) -> None:
        """Remove todos os relatórios da pilha. O(1)."""
        self._dados.clear()

    def listar(self) -> List[str]:
        """
        Lista os títulos do MAIS RECENTE para o MAIS ANTIGO (ordem de pop).
        """
        return [titulo for titulo, _ in reversed(self._dados)]

    def __len__(self) -> int:
        return len(self._dados)

    def __repr__(self) -> str:
        return f"PilhaRelatorios({self.listar()!r})"
