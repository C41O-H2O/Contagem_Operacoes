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
import itertools
import random
from trabalho_base import (
    mergesort,
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


def main():
    testar_ingenua()
    testar_esperta()


if __name__ == "__main__":
    main()
