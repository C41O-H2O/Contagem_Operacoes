"""
misteriosas.py — Funções misteriosas RECEBIDAS de outra equipe (Seção 4 do enunciado).

Como usar:
  1. Cole cada função recebida abaixo, mantendo a linha marcada com  # ←  (é ela que se conta).
  2. Instrumente: a função deve devolver (resultado, contagem).
  3. Registre em FUNCOES: nome -> (função, palpite_de_classe_lendo_o_codigo).
  4. Rode `python tema_3.py`: o teste do dobro de cada uma entra na saída e no CSV.

Exemplo de instrumentação (apenas modelo, não é uma das funções recebidas):
"""


def exemplo_modelo(n):
    contagem = 0
    i = n
    while i >= 1:
        contagem += 1                           # ← linha contada
        i //= 2
    return None, contagem


# nome -> (função, "previsão feita lendo o código")
FUNCOES = {
    # "misteriosa_1": (misteriosa_1, "linear"),
    # "misteriosa_2": (misteriosa_2, "n log n"),
}


def executar(dados):
    from trabalho_base import teste_do_dobro
    if not FUNCOES:
        print("\nFunções misteriosas: nenhuma cadastrada ainda (ver misteriosas.py).")
        return
    for nome, (funcao, previsao) in FUNCOES.items():
        teste_do_dobro(f"MISTERIOSA {nome} (previsão: {previsao})",
                       lambda n, f=funcao: f(n)[1],
                       versao=nome, dados=dados)
