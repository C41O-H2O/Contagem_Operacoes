# Trabalho Prático — Contagem de Operações
## Tema 3 — As duas notas mais próximas

Projeto e Análise de Algoritmos · CIESA · Equipe: **[NOMES DOS INTEGRANTES]**
Semente fixa: 42 · Python 3 · Repositório: **[LINK DO GIT]**

## (i) Cenário e formato da entrada

A coordenação quer formar duplas de estudo equilibradas: os dois alunos com a **menor
diferença de nota final** da turma.

- **Entrada:** lista `v` de `n` notas inteiras de 0 a 100, com repetidos possíveis (`n ≥ 0`).
- **Saída:** `((menor, maior), diferença)`; `None` se `n < 2`.
- **Desempate:** entre pares de mesma diferença, vence o de menor `(menor, maior)`. Assim as
  duas versões devolvem exatamente o mesmo resultado (o que o teste de correção confere).
- **Geradores** (`trabalho_base.py`): `aleatorio(n, 0, 100, semente)` para o caso médio,
  `distintos` e `ordenado`; sementes 42 a 71.
- **Operação básica:** *diferença calculada* (ingênua e varredura da esperta); a ordenação
  conta *comparações do mergesort*, sempre à parte.

## (ii) Pseudocódigo comentado

```
INGÊNUA(v)                                   ESPERTA(v)
  se n < 2: devolve nada                       s ← MERGESORT(v)          # c_ord comparações
  para i de 0 até n-2:                         se n < 2: devolve nada
    para j de i+1 até n-1:                     para i de 0 até n-2:
      d ← |v[i] − v[j]|      # conta 1           d ← s[i+1] − s[i]      # conta 1
      se d < melhor: guarda (par, d)             se d < melhor: guarda (par, d)
  devolve melhor                               devolve melhor
```

A ingênua não tem parada antecipada: ela precisa olhar todos os pares porque só no fim sabe
qual é o menor. A esperta troca "olhar todos os pares" por "ordenar e olhar `n − 1` vizinhos";
a prova de que isso basta está na seção (iv).

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

## (v) Teste do dobro: tabelas e razão que estabiliza

Tabelas completas na saída de `python tema_3.py` e no CSV. Resumo (n = 100 → 1 600; série
grande até 100 000):

| Versão / caso | Razão que estabiliza | Valor | Coluna dobro |
|---|---|---|---|
| Ingênua (qualquer entrada) | `c/n²` | 0,495 → **0,4997** (→ ½) | 4,02 → **4,00** |
| Esperta, pior caso | `c/(n lg n)` | 1,011 → 1,007 (1,005 em 100 000) | 2,30 → 2,21 → 2,13 |
| Esperta, caso médio | `c/(n lg n)` | 0,964 → 0,976 (0,983 em 100 000) | 2,31 → 2,21 → 2,13 |
| Esperta, melhor caso | `c/(n lg n)` | 0,625 → 0,579 (0,551 em 100 000) | 2,24 → 2,18 → 2,12 |
| Só a varredura | `c/n` | **1,000** | 2,00 |
| Só a ordenação (médio) | `c/(n lg n)` | 0,815 → 0,882 (0,923 em 100 000) | 2,37 → 2,24 → 2,14 |

- A ingênua dobra **×4**: quadrática, e a razão `c/n²` é exatamente `½ − 1/(2n)`.
- Na esperta a coluna dobro **não é 2 de cara**: `c(2n)/c(n) = 2(1 + 1/lg n)`, que vale 2,12
  em n = 100 000 e tende a 2 devagar. É a assinatura de `n log n`: quem olhasse só um `n`
  poderia confundir com linear ou com algo pior (erro clássico do enunciado).
- No pior caso da esperta, `c/(n lg n) ≈ 1`: o `−n` da ordenação é compensado pelo `+n − 1`
  da varredura.

**Peso de cada fase na esperta (caso médio):**

| n | ordenação | varredura | % ordenação |
|---|---|---|---|
| 100 | 541,2 | 99 | 84,5 % |
| 1 600 | 15 021,5 | 1 599 | 90,4 % |
| 12 500 | 154 245,2 | 12 499 | 92,5 % |
| 100 000 | 1 532 397,8 | 99 999 | **93,9 %** |

**Quanto a esperta ganha:** em n = 1 600, 1 279 200 ÷ 16 620,5 ≈ **77×** menos diferenças;
em n = 100 000, `n(n−1)/2 = 4 999 950 000` contra ≈ 1 632 397, cerca de **3 060×** (a ingênua
não foi executada nesse tamanho; vale a fórmula, já validada de 100 a 1 600).

### Confronto: contagem à mão × medição

| n | Item | À mão | Medido | Diferença |
|---|---|---|---|---|
| 100 | ingênua `n(n−1)/2` | 4 950 | 4 950 | 0 |
| 100 | ordenação, pior `W(n)` | 573 | 573 | 0 |
| 100 | ordenação, melhor `B(n)` | 316 | 316 | 0 |
| 100 | ordenação, média `≈ n lg n − 1,25n` | 539,4 | 541,2 | +1,8 |
| 1 024 | ordenação, pior `W(n)` | 9 217 | 9 217 | 0 |
| 1 024 | ordenação, melhor `(n/2) lg n` | 5 120 | 5 120 | 0 |
| 1 024 | ordenação, média | 8 960,0 | 8 937,5 | −22,5 |
| 1 600 | ingênua | 1 279 200 | 1 279 200 | 0 |
| 1 600 | ordenação, pior `W(n)` | 15 553 | 15 553 | 0 |
| 1 600 | ordenação, média | 15 030,2 | 15 021,5 | −8,7 |
| 12 500 | ordenação, pior `W(n)` | 158 617 | 158 617 | 0 |
| 12 500 | ordenação, média | 154 495,5 | 154 245,2 | −250,3 |

As fórmulas **exatas** (ingênua, varredura, pior e melhor da ordenação) batem em todos os `n`
(o teste confere de 1 a 300 e nos tamanhos grandes). Só o **caso médio** diverge, porque é
uma aproximação: ignora termos de ordem menor, e as notas de 0 a 100 têm muitos repetidos,
o que muda levemente as comparações. A diferença é de 0,06 % a 0,33 %. Para `n` que não é
potência de 2 (100, 1 600, 12 500) os pisos e tetos do log importam: por isso a fórmula
usa `⌈lg n⌉`, e `n lg n − n + 1` valeria só para `n = 2^k`.

## (vi) Funções misteriosas recebidas

**[PREENCHER quando a equipe receber as funções do professor.]** Para cada uma: código com a
linha `# ←`, previsão lida no código (T(n) e classe), tabela do teste do dobro (saída de
`python tema_3.py`, via `misteriosas.py`), T(n) e classe medidos, e onde a previsão acertou ou errou.

| Função | Previsão (lendo o código) | Medido (razão que estabiliza) | Acertou? |
|---|---|---|---|
| misteriosa 1 | | | |
| misteriosa 2 | | | |

## (vii) Conclusão crítica

1. **Classes:** ingênua `Θ(n²)` (melhor = pior, sem parada antecipada); esperta `Θ(n log n)`.
   A decisão veio da razão que estabiliza ao longo de várias dobras, não de um único `n`.
2. **A ordenação define a classe da esperta.** Ela responde por 84 % a 94 % das operações
   e cresce com `n`. Contar só a varredura daria `c/n = 1,000` e uma conclusão errada:
   "linear". É o erro clássico apontado no enunciado.
3. **Correção antes de medir:** as duas versões concordam em 1 011 entradas (borda,
   repetidos, todos iguais), e o desempate por `(menor, maior)` evita discordância só de par.
4. **Limite do modelo:** as notas são inteiros de 0 a 100. Para `n ≥ 102` o princípio da
   casa dos pombos garante um par repetido (diferença 0), e um vetor de 101 contadores
   resolveria em `Θ(n)`, sem ordenar. A análise acima vale para notas em um intervalo
   grande ou desconhecido, que é o caso geral do problema.
5. **Limitações:** a construção do pior caso é específica do mergesort da base; o caso médio
   usa uma fórmula aproximada; não medimos tempo em segundos (opcional no enunciado).
6. **Extra:** para pontos `(AV1, AV2)` no plano, ordenar por uma coordenada **não** basta.
   Com `(0,0), (1,100), (2,1)` o melhor par de vizinhos tem distância² 9 802, mas o par
   realmente mais próximo `(0,0)–(2,1)` tem 5. Exige outra técnica (divisão e conquista).

## (viii) Declaração de uso de IA generativa

> **[AJUSTAR com o que a equipe realmente fez; este texto é um rascunho.]**

Foi usada a IA generativa **Claude (Anthropic)** como apoio:

- **O que foi pedido:** estrutura e primeira versão do código do Tema 3 (versões ingênua e
  esperta, testes de correção, medições, fórmulas), do relatório, do roteiro de apresentação
  e a organização do histórico de commits.
- **O que foi aproveitado:** o código e o texto foram revisados, executados e [ALTERADOS /
  mantidos — descrever] pela equipe. Todos os integrantes conseguem explicar qualquer linha
  e qualquer contador, como exige a arguição.

## (ix) Referências

- Enunciado e `trabalho_base.py` do Trabalho Prático de PAA (CIESA); Aula 03 (busca binária)
  e Aula 04 (mergesort).
- CORMEN, T. H. et al. *Algoritmos: teoria e prática* / *Introduction to Algorithms* (análise
  do mergesort e árvore de recursão).
- KNUTH, D. E. *The Art of Computer Programming*, vol. 3: *Sorting and Searching* (número de
  comparações do mergesort).
- Documentação do Python 3 (`random`, `functools`, `itertools`).
