# Tema 3 — As duas notas mais próximas

Trabalho Prático de Projeto e Análise de Algoritmos (CIESA) — contagem de operações:
lineares, quadráticos e logarítmicos.

**Problema:** dada a lista de `n` notas, devolver o par de menor diferença e essa diferença.

| Versão | Ideia | Operação contada |
|---|---|---|
| `ingenua` | diferença de todos os pares | diferenças calculadas |
| `esperta` | mergesort + diferença só entre vizinhos | diferenças da varredura + comparações da ordenação (à parte) |

## Como reproduzir tudo

```bash
python tema_3.py          # testes + todas as tabelas + CSV (~20 s)
python tema_3.py --demo   # só o teste do dobro das duas versões (~1 s, para a apresentação)
```

Requer apenas Python 3, sem dependências. A saída, em ordem:

1. testes de correção (1 011 entradas, com casos de borda, contra um oráculo);
2. teste do dobro: ingênua; esperta em melhor, pior e médio caso; cada fase da esperta
   separada; série maior até n = 100 000;
3. peso de cada fase e a discussão do melhor caso da ingênua;
4. confronto **contagem à mão × medição**;
5. extra dos pontos no plano e funções misteriosas recebidas;
6. dados brutos em `medicoes_tema3.csv` (`versao, n, contagem`).

Sementes: `42` (e `42..71` nas 30 listas do caso médio).

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `trabalho_base.py` | base comum do professor (**não alterar**) |
| `tema_3.py` | versões, testes, medições, fórmulas e confronto |
| `misteriosas.py` | funções misteriosas recebidas, instrumentadas |
| `medicoes_tema3.csv` | dados brutos gerados por `salvar_csv` |
| `RELATORIO.md` | relatório (seções i a ix) |
| `roteiro_apresentacao.md` | roteiro dos 8 slides e da demonstração ao vivo |

## Regras do enunciado cumpridas

Nenhuma solução usa `sorted`, `list.sort`, `bisect`, `set`, `dict`, `Counter` ou `in`
sobre listas. `sorted` e `itertools` aparecem **apenas** nos testes
(`oraculo` e `testar_casos` em `tema_3.py`).
