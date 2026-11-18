# Relatório — Tema 3 (rascunho: contagem à mão)

> Seções iii e iv. As demais seções (i, ii, v a ix) entram na versão final.

## (iii) Contagem à mão

**Ingênua.** O laço externo roda `i = 0 … n−2`; para cada `i`, o interno roda `n−1−i` vezes:

$$T_{ing}(n)=\sum_{i=0}^{n-2}(n-1-i)=\sum_{k=1}^{n-1}k=\frac{n(n-1)}{2}\in\Theta(n^2)$$

**Esperta, fase 1 — ordenação (mergesort).** Cada intercalação de duas metades que somam
`m` elementos gasta entre `⌊m/2⌋` e `m−1` comparações. Na árvore de recursão, o nível `ℓ`
(`0 ≤ ℓ < lg n`) tem `2^ℓ` intercalações de `n/2^ℓ` elementos; para `n = 2^k`:

- **pior caso:** `Σ_{ℓ=0}^{k-1} (n − 2^ℓ) = nk − 2^k + 1 = n lg n − n + 1`;
- **melhor caso:** `Σ_{ℓ=0}^{k-1} n/2 = (n/2)·lg n`.

Para `n` qualquer, a recorrência `W(n) = W(⌊n/2⌋) + W(⌈n/2⌉) + n − 1` tem solução

$$W(n)=n\lceil\lg n\rceil-2^{\lceil\lg n\rceil}+1,\qquad B(n)=B(\lfloor n/2\rfloor)+B(\lceil n/2\rceil)+\lfloor n/2\rfloor.$$

**Esperta, fase 2 — varredura.** `T_var(n) = Σ_{i=0}^{n-2} 1 = n − 1`, em qualquer entrada.

**Esperta, total:** `T_esp(n) = C_ord(n) + (n − 1)`, com `C_ord ∈ Θ(n log n)`. Logo
`T_esp ∈ Θ(n log n)`. A varredura é linear e **não define a classe**: a ordenação a soma e
domina (ver pesos na seção v).

## (iv) Melhor e pior caso, e a entrada que produz cada um

| Versão | Melhor caso | Pior caso |
|---|---|---|
| Ingênua | **igual ao pior**: `n(n−1)/2`, com qualquer entrada | `n(n−1)/2`, com qualquer entrada |
| Esperta | lista **já ordenada**: `B(n) + n − 1` | entrada de **intercalação máxima**: `W(n) + n − 1` |

- **Ingênua não tem melhor caso diferente do pior.** Sem parada antecipada, os dois laços
  rodam por inteiro mesmo que o primeiro par já tenha diferença 0, pois nada garante que não
  exista par melhor. (Com uma *variante* que para em diferença 0, o melhor caso cairia para 1
  e o pior continuaria `n(n−1)/2`; para `n = 1600` a execução confirma 1 × 1 279 200. Não é a
  versão oficial: em empates o par devolvido pode diferir.)
- **Pior caso da esperta:** a permutação construída por `pior_caso_mergesort(n)` desfaz a
  intercalação alternando os elementos entre as metades, de modo que o maior elemento sempre
  fica sozinho no fim e cada intercalação gasta `m − 1` comparações. Ex.: `n = 4 → [0, 2, 1, 3]`.
- **Melhor caso da esperta:** `ordenado(n)`: em cada intercalação toda a metade esquerda é
  consumida antes de a direita começar (`⌊m/2⌋` comparações).
- **Caso médio:** 30 listas aleatórias (sementes 42 a 71). Teoricamente
  `C_ord ≈ n lg n − 1,25 n`. A varredura continua `n − 1`.

### Prova: numa lista ordenada, o par mais próximo é formado por vizinhos

Seja `a_1 ≤ a_2 ≤ … ≤ a_n` e suponha que o par mais próximo seja `(a_i, a_j)` com `j > i + 1`.
Como `a_i ≤ a_{i+1} ≤ a_j`,

```
a_j − a_i = (a_j − a_{i+1}) + (a_{i+1} − a_i)  ≥  a_{i+1} − a_i  ≥ 0
```

então o par de vizinhos `(a_i, a_{i+1})` tem diferença **menor ou igual** à de `(a_i, a_j)`.
Repetindo o argumento, existe sempre um par de vizinhos ótimo. Se vale a igualdade,
`a_j = a_{i+1}`: os dois pares têm os mesmos valores, o que justifica também a regra de
desempate. ∎

