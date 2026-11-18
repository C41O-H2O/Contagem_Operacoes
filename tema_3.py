"""
tema_3.py — Tema 3: As duas notas mais próximas
Projeto e Análise de Algoritmos — CIESA — Trabalho Prático de Contagem de Operações

Problema: dada a lista de n notas, devolver o par de notas de menor diferença
e essa diferença.

Versões (toda função instrumentada devolve (resultado, contagem)):
    ingenua  — calcula a diferença de todos os pares            -> n(n-1)/2
    esperta  — mergesort + diferença só entre vizinhos          -> Θ(n log n)

Operação contada: diferenças calculadas (e, na esperta, as comparações da
ordenação, contadas à parte).

Uso:  python tema_3.py
      (roda os testes de correção, imprime as tabelas e grava medicoes_tema3.csv)
"""
from functools import lru_cache
import itertools
import math
import random
import sys
from trabalho_base import (
    mergesort,
    aleatorio,
    distintos,
    ordenado,
    invertido,
    teste_do_dobro,
    salvar_csv,
)

SEMENTE = 42  # semente fixa e registrada (roteiro do experimento, item 4)


# =================================================================
# 1. Versão ingênua — calcula a diferença de todos os pares
# =================================================================
def ingenua(v):
    """Calcula |a - b| para todo par (i < j) e guarda o menor.

    Devolve (resultado, contagem):
      resultado = ((menor_valor, maior_valor), diferença), ou None se len(v) < 2
      contagem  = diferenças calculadas
    Desempate: entre pares de mesma diferença vence o de menor (lo, hi);
    assim a versão esperta devolve exatamente o mesmo resultado.
    """
    n = len(v)
    if n < 2:
        return None, 0
    melhor_d = float("inf")
    melhor_par = None
    contagem = 0
    for i in range(n - 1):
        a = v[i]
        for j in range(i + 1, n):
            contagem += 1                       # ← diferença calculada
            d = abs(a - v[j])
            if d < melhor_d:
                melhor_d = d
                melhor_par = (a, v[j]) if a <= v[j] else (v[j], a)
            elif d == melhor_d:
                par = (a, v[j]) if a <= v[j] else (v[j], a)
                if par < melhor_par:
                    melhor_par = par
    return (melhor_par, melhor_d), contagem


# =================================================================
# Testes de correção (a lista vazia, o 1 elemento, os iguais e os repetidos
# são casos de borda; sorted/itertools aparecem só aqui, como oráculo)
# =================================================================
def oraculo(v):
    """Oráculo SÓ para testes: força bruta com itertools, conferida por sorted."""
    if len(v) < 2:
        return None
    d, lo, hi = min((abs(a - b), min(a, b), max(a, b))
                    for a, b in itertools.combinations(v, 2))
    s = sorted(v)
    assert d == min(y - x for x, y in zip(s, s[1:])), "oráculo inconsistente"
    return (lo, hi), d


def listas_de_teste(quantidade=1000, semente=SEMENTE):
    """Casos de borda + `quantidade` listas aleatórias (tamanho 0..30,
    notas em 0..100 ou 0..10 para forçar muitos repetidos)."""
    casos = [[], [7], [3, 3], [5, 5, 5, 5], [0, 100], [100, 0, 50],
             [1, 2, 3, 4, 5], [5, 4, 3, 2, 1], [10, 20, 10, 20],
             [0, 100, 0, 100, 50], [50, 10, 11, 90, 12, 10]]
    gerador = random.Random(semente)
    for _ in range(quantidade):
        n = gerador.randint(0, 30)
        topo = gerador.choice([10, 100])
        casos.append([gerador.randint(0, topo) for _ in range(n)])
    return casos


def testar_ingenua():
    casos = listas_de_teste()
    for v in casos:
        copia = list(v)
        resultado, c = ingenua(v)
        assert resultado == oraculo(v), (v, resultado)
        assert v == copia, "a entrada foi alterada"
        assert c == len(v) * (len(v) - 1) // 2, (v, c)
    print(f"[ok] ingênua: {len(casos)} entradas conferidas com o oráculo")


# =================================================================
# 2. Versão esperta — ordena e compara apenas vizinhos
# =================================================================
def esperta_fases(v):
    """Ordena com o mergesort da base e varre os vizinhos.

    Devolve (resultado, comparações_da_ordenação, diferenças_da_varredura),
    para contar cada fase à parte (roteiro do experimento, item 3).
    """
    ordenada, c_ord = mergesort(v)
    n = len(ordenada)
    if n < 2:
        return None, c_ord, 0
    melhor_d = float("inf")
    melhor_par = None
    c_var = 0
    for i in range(n - 1):
        c_var += 1                              # ← diferença calculada
        d = ordenada[i + 1] - ordenada[i]
        if d < melhor_d:                        # '<' estrito: fica o 1º (menor lo)
            melhor_d = d
            melhor_par = (ordenada[i], ordenada[i + 1])
    return (melhor_par, melhor_d), c_ord, c_var


def esperta(v):
    """Mesma convenção da base: (resultado, contagem total = ordenação + varredura)."""
    resultado, c_ord, c_var = esperta_fases(v)
    return resultado, c_ord + c_var


def testar_esperta():
    casos = listas_de_teste()
    for v in casos:
        copia = list(v)
        resultado, c_ord, c_var = esperta_fases(v)
        assert resultado == oraculo(v), (v, resultado)
        assert resultado == ingenua(v)[0], (v, "ingênua e esperta discordam")
        assert v == copia, "a entrada foi alterada"
        assert c_ord == mergesort(v)[1]
        assert c_var == max(len(v) - 1, 0), (v, c_var)
        assert esperta(v)[1] == c_ord + c_var
    print(f"[ok] esperta: {len(casos)} entradas; concorda com a ingênua e com o oráculo")


# =================================================================
# 3. Entradas de melhor/pior caso, caso médio e teste do dobro
# =================================================================
TAMANHOS = (100, 200, 400, 800, 1600)
TAMANHOS_GRANDES = (12_500, 25_000, 50_000, 100_000)  # só para a esperta
EXECUCOES = 30                                       # listas aleatórias no caso médio


def pior_caso_mergesort(n):
    """Permutação de 0..n-1 que força o mergesort da base ao máximo de
    comparações: desfaz a intercalação, alternando os elementos entre as duas
    metades, de modo que cada intercalação gasta (tamanho - 1) comparações."""
    def desfazer(v):
        if len(v) <= 1:
            return list(v)
        if len(v) % 2 == 0:
            esquerda, direita = v[0::2], v[1::2]
        else:                                   # a metade esquerda do mergesort é a menor
            direita, esquerda = v[0::2], v[1::2]
        return desfazer(esquerda) + desfazer(direita)
    return desfazer(list(range(n)))


def ingenua_com_parada(v):
    """Variante SÓ para a discussão do melhor caso: para ao achar diferença 0.
    (Não é a versão oficial: em empates o par pode diferir da esperta.)"""
    n = len(v)
    contagem = 0
    melhor = None
    for i in range(n - 1):
        for j in range(i + 1, n):
            contagem += 1
            d = abs(v[i] - v[j])
            if melhor is None or d < melhor[1]:
                melhor = ((min(v[i], v[j]), max(v[i], v[j])), d)
            if d == 0:
                return melhor, contagem
    return melhor, contagem


def media_ingenua(n):
    """Média das diferenças calculadas em EXECUCOES listas aleatórias."""
    total = 0
    for k in range(EXECUCOES):
        total += ingenua(aleatorio(n, 0, 100, SEMENTE + k))[1]
    return total / EXECUCOES


@lru_cache(maxsize=None)
def media_fases(n):
    """(média das comparações da ordenação, média das diferenças da varredura)
    em EXECUCOES listas aleatórias, sementes SEMENTE .. SEMENTE + 29."""
    soma_ord = soma_var = 0
    for k in range(EXECUCOES):
        _, c_ord, c_var = esperta_fases(aleatorio(n, 0, 100, SEMENTE + k))
        soma_ord += c_ord
        soma_var += c_var
    return soma_ord / EXECUCOES, soma_var / EXECUCOES


def testar_casos():
    # ingênua: a contagem não depende da entrada (sem parada antecipada)
    for n in (2, 3, 50, 400):
        for v in (ordenado(n), invertido(n), distintos(n, SEMENTE), [7] * n):
            assert ingenua(v)[1] == n * (n - 1) // 2
    # a construção do pior caso é uma permutação e é pior que os outros casos
    for n in (1, 2, 3, 10, 100, 1600):
        pior = pior_caso_mergesort(n)
        assert sorted(pior) == list(range(n))        # oráculo
    n = 1600
    c_pior = esperta_fases(pior_caso_mergesort(n))[1]
    c_med = esperta_fases(aleatorio(n, 0, 100, SEMENTE))[1]
    c_melhor = esperta_fases(ordenado(n))[1]
    assert c_melhor < c_med < c_pior, (c_melhor, c_med, c_pior)
    # a varredura é sempre n-1, qualquer que seja a entrada
    for v in (ordenado(n), pior_caso_mergesort(n), aleatorio(n)):
        assert esperta_fases(v)[2] == n - 1
    print("[ok] casos: contagens e construções de melhor/pior caso conferidas")


def medir_tudo(dados):
    # ---- ingênua -------------------------------------------------
    teste_do_dobro("INGÊNUA — melhor = pior caso (qualquer entrada): diferenças",
                   lambda n: ingenua(distintos(n, SEMENTE))[1],
                   TAMANHOS, "ingenua_melhor_pior", dados)
    teste_do_dobro(f"INGÊNUA — caso médio ({EXECUCOES} listas aleatórias): diferenças",
                   media_ingenua, TAMANHOS, "ingenua_medio", dados)

    # ---- esperta: tamanhos do roteiro e série maior --------------
    for tamanhos, rotulo in ((TAMANHOS, "n do roteiro"), (TAMANHOS_GRANDES, "série grande")):
        teste_do_dobro(f"ESPERTA — melhor caso (lista já ordenada), total [{rotulo}]",
                       lambda n: esperta(ordenado(n))[1],
                       tamanhos, "esperta_melhor", dados)
        teste_do_dobro(f"ESPERTA — pior caso (intercalação máxima), total [{rotulo}]",
                       lambda n: esperta(pior_caso_mergesort(n))[1],
                       tamanhos, "esperta_pior", dados)
        teste_do_dobro(f"ESPERTA — caso médio ({EXECUCOES} listas), total [{rotulo}]",
                       lambda n: sum(media_fases(n)),
                       tamanhos, "esperta_medio", dados)
        teste_do_dobro(f"ESPERTA — só a ORDENAÇÃO, caso médio [{rotulo}]",
                       lambda n: media_fases(n)[0],
                       tamanhos, "esperta_so_ordenacao", dados)
        teste_do_dobro(f"ESPERTA — só a VARREDURA, caso médio [{rotulo}]",
                       lambda n: media_fases(n)[1],
                       tamanhos, "esperta_so_varredura", dados)

    peso_das_fases()
    demo_melhor_caso_ingenua()


def peso_das_fases():
    print("\nPESO DE CADA FASE NA ESPERTA (caso médio)")
    print(f"{'n':>8} {'ordenação':>11} {'varredura':>10} {'total':>11} {'% ordenação':>12}")
    for n in TAMANHOS + TAMANHOS_GRANDES:
        c_ord, c_var = media_fases(n)
        total = c_ord + c_var
        print(f"{n:>8} {c_ord:>11.1f} {c_var:>10.0f} {total:>11.1f} {100 * c_ord / total:>11.2f}%")


def demo_melhor_caso_ingenua(n=1600):
    print(f"\nA ingênua tem melhor caso diferente do pior? (n = {n})")
    com_zero = [5, 5] + list(range(10, 10 + n - 2))     # a 1ª diferença já é 0
    sem_zero = distintos(n, SEMENTE)                    # nenhum par com diferença 0
    print(f"  versão oficial (sem parada):  {ingenua(com_zero)[1]} (com par igual no início) "
          f"| {ingenua(sem_zero)[1]} (sem par igual)")
    print(f"  variante com parada em zero:  {ingenua_com_parada(com_zero)[1]} (com par igual no início) "
          f"| {ingenua_com_parada(sem_zero)[1]} (sem par igual)")


# =================================================================
# 4. Contagem à mão (fórmulas) e confronto com a medição
# =================================================================
def T_ingenua(n):
    """Σ_{i=0}^{n-2} (n-1-i) = n(n-1)/2."""
    return n * (n - 1) // 2


def T_varredura(n):
    """Σ_{i=0}^{n-2} 1 = n-1."""
    return max(n - 1, 0)


def W_ord(n):
    """Pior caso do mergesort: W(n) = W(⌊n/2⌋) + W(⌈n/2⌉) + n - 1,
    com solução fechada n·⌈log2 n⌉ − 2^⌈log2 n⌉ + 1."""
    if n <= 1:
        return 0
    k = (n - 1).bit_length()                    # ⌈log2 n⌉
    return n * k - 2 ** k + 1


@lru_cache(maxsize=None)
def B_ord(n):
    """Melhor caso (lista ordenada): B(n) = B(⌊n/2⌋) + B(⌈n/2⌉) + ⌊n/2⌋.
    Para n = 2^k: (n/2)·log2 n."""
    if n <= 1:
        return 0
    return B_ord(n // 2) + B_ord(n - n // 2) + n // 2


def M_ord_aprox(n):
    """Caso médio do mergesort em permutações: ≈ n·log2 n − 1,25·n."""
    return n * math.log2(n) - 1.25 * n


def testar_contagens():
    for n in range(1, 301):                     # fórmulas × medição, todos os n pequenos
        assert esperta_fases(pior_caso_mergesort(n))[1] == W_ord(n), n
        assert esperta_fases(ordenado(n))[1] == B_ord(n), n
    for n in (12_500, 100_000):
        assert esperta_fases(pior_caso_mergesort(n))[1] == W_ord(n), n
    for n in (2, 4, 1024, 4096):
        assert B_ord(n) == (n // 2) * int(math.log2(n))      # fórmula para n = 2^k
    for n in TAMANHOS:
        assert ingenua(distintos(n, SEMENTE))[1] == T_ingenua(n)
    print("[ok] contagens: as fórmulas coincidem exatamente com as medições")


def confronto(tamanhos=(100, 1024, 1600, 12_500)):
    """Calculado à mão × medido, em pelo menos três valores de n."""
    print("\nCONFRONTO: contagem à mão × medição")
    print(f"{'n':>7} {'item':<34} {'à mão':>12} {'medido':>12} {'diferença':>10}")
    for n in tamanhos:
        medido_ing = ingenua(distintos(n, SEMENTE))[1] if n <= 1600 else None
        linhas = [
            ("ingênua: n(n-1)/2", T_ingenua(n), medido_ing),
            ("varredura: n-1", T_varredura(n), esperta_fases(ordenado(n))[2]),
            ("ordenação, pior: n⌈lg n⌉−2^⌈lg n⌉+1", W_ord(n), esperta_fases(pior_caso_mergesort(n))[1]),
            ("ordenação, melhor: recorrência", B_ord(n), esperta_fases(ordenado(n))[1]),
            ("ordenação, média: ≈ n lg n − 1,25n", M_ord_aprox(n), media_fases(n)[0]),
        ]
        for nome, calc, med in linhas:
            if med is None:
                continue
            print(f"{n:>7} {nome:<34} {calc:>12.1f} {med:>12.1f} {med - calc:>10.1f}")
        print()


# =================================================================
# 5. Extra e funções misteriosas
# =================================================================
def demo_pontos_2d():
    """Extra: 'ordenar e olhar vizinhos' NÃO serve para pontos (AV1, AV2).
    Ordenando por AV1, os vizinhos podem estar longe um do outro,
    enquanto o par realmente mais próximo fica separado na lista."""
    pontos = [(0, 0), (1, 100), (2, 1)]            # já em ordem de AV1

    def dist2(p, q):
        return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2

    vizinhos = min((dist2(pontos[i], pontos[i + 1]), pontos[i], pontos[i + 1])
                   for i in range(len(pontos) - 1))
    todos = min((dist2(p, q), p, q) for p, q in itertools.combinations(pontos, 2))
    print("\nEXTRA — pontos no plano (distância ao quadrado)")
    print(f"  melhor entre vizinhos da lista ordenada: {vizinhos[1]} e {vizinhos[2]}  -> {vizinhos[0]}")
    print(f"  par realmente mais próximo:              {todos[1]} e {todos[2]}  -> {todos[0]}")
    assert todos[0] < vizinhos[0]


def demo_ao_vivo():
    """Demonstração rápida (~1 s) para a apresentação: python tema_3.py --demo"""
    teste_do_dobro("INGÊNUA (melhor = pior caso): diferenças",
                   lambda n: ingenua(distintos(n, SEMENTE))[1])
    teste_do_dobro("ESPERTA (pior caso): ordenação + varredura",
                   lambda n: esperta(pior_caso_mergesort(n))[1])
    teste_do_dobro("ESPERTA — só a varredura (parece linear, mas não é a história toda)",
                   lambda n: esperta_fases(pior_caso_mergesort(n))[2])


def rodar_misteriosas(dados):
    """Executa as funções misteriosas recebidas (ver misteriosas.py)."""
    import misteriosas
    misteriosas.executar(dados)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demo_ao_vivo()
        return
    dados = []
    testar_ingenua()
    testar_esperta()
    testar_casos()
    medir_tudo(dados)
    testar_contagens()
    confronto()
    demo_pontos_2d()
    rodar_misteriosas(dados)
    salvar_csv(dados, "medicoes_tema3.csv")


if __name__ == "__main__":
    main()
