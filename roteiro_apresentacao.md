# Roteiro da apresentação — Tema 3 (10 min: 7 de exposição + 3 de arguição)

Máximo de 8 slides; **todos os integrantes falam**; demonstração ao vivo obrigatória.
Sugestão de falantes pelos papéis; troquem à vontade.

| # | Slide | Conteúdo | Quem | Tempo |
|---|---|---|---|---|
| 1 | O problema | Cenário das duplas de estudo; entrada, saída, operação contada | Integrante 1 | 0:40 |
| 2 | Duas versões | Pseudocódigo lado a lado: todos os pares × ordenar e olhar vizinhos | Integrantes 1 e 2 | 1:00 |
| 3 | Contagem à mão | `n(n−1)/2`; árvore de recursão do mergesort; `n − 1` da varredura | Integrante 4 | 1:10 |
| 4 | Melhor e pior caso | A ingênua não tem melhor caso diferente; entradas construídas da esperta; prova dos vizinhos | Integrante 4 | 0:50 |
| 5 | **Demo ao vivo** + teste do dobro | `python tema_3.py --demo`; ×4 contra ≈ ×2; razões que estabilizam | Integrante 3 | 1:10 |
| 6 | Peso das fases | 84 % → 94 % da esperta é ordenação; erro clássico de contar só a varredura | Integrante 2 | 0:50 |
| 7 | Misteriosas | Previsão × medição das funções recebidas; onde errou | Integrante 5 | 0:40 |
| 8 | Conclusão | Classes, limites (notas 0–100), declaração de IA | Integrante 5 | 0:40 |

## Roteiro da demonstração ao vivo (≈ 1 min)

1. `python tema_3.py --demo`.
2. Apontar a coluna **dobro** da ingênua (→ 4,00) e `c/n²` (→ 0,5).
3. Apontar a da esperta (→ 2,2, descendo devagar) e `c/(n lg n)` (≈ 1).
4. Mostrar a terceira tabela (só a varredura: `c/n = 1,000`) e perguntar: "por que ela
   não define a classe?".

## Perguntas prováveis da arguição

- Por que o par mais próximo, numa lista ordenada, é sempre de vizinhos? (prova na seção iv)
- Por que a ingênua não tem melhor caso diferente do pior?
- Como foi construída a entrada de pior caso do mergesort?
- Por que a coluna dobro da esperta é 2,2 e não 2?
- O que mudaria se a nota fosse um ponto (AV1, AV2)?
- Por que as 30 execuções, se a ingênua conta sempre o mesmo?
