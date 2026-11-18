# Tema 3 — As duas notas mais próximas

Trabalho Prático de Projeto e Análise de Algoritmos (CIESA): contagem de operações.

Dada a lista de `n` notas, devolver o par de menor diferença e essa diferença.

| Versão | Ideia | Operação contada |
|---|---|---|
| `ingenua` | diferença de todos os pares | diferenças calculadas |
| `esperta` | mergesort + diferença só entre vizinhos | diferenças da varredura + comparações da ordenação (à parte) |

## Como reproduzir tudo

```bash
python tema_3.py
```

Requer apenas Python 3 (sem dependências), leva cerca de 20 s e faz, em ordem:

1. testes de correção (1 011 entradas, com casos de borda, contra um oráculo);
2. tabelas do teste do dobro (ingênua; esperta em melhor, pior e médio caso;
   cada fase da esperta separada; série maior até n = 100 000);
3. peso de cada fase e a discussão do melhor caso da ingênua;
4. grava os dados brutos em `medicoes_tema3.csv` (`versao, n, contagem`).

Sementes: `42` (e `42..71` nas 30 listas do caso médio). O `trabalho_base.py` é a
base comum do professor e **não deve ser alterado**.

## Contagem à mão

`tema_3.py` traz as fórmulas (`T_ingenua`, `T_varredura`, `W_ord`, `B_ord`) e a tabela
**contagem à mão × medição**. A dedução com Σ e log está em `RELATORIO.md`
(seções iii e iv).
