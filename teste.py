# teste do analisador léxico
# funções de teste para o analisador léxico,
# cobrindo entradas válidas e inválidas.

#python testes.py

from main import parseExpressao

# Contadores de testes
total_testes = 0
testes_ok = 0
testes_falha = 0

def verificar(descricao, entrada, esperado):
    """
    Função auxiliar que testa uma entrada no parseExpressao
    e compara o resultado com o esperado.
    """
    global total_testes, testes_ok, testes_falha
    total_testes += 1

    resultado = parseExpressao(entrada)

    if resultado == esperado:
        testes_ok += 1
        status = "PASSOU"
    else:
        testes_falha += 1
        status = "FALHOU"

    print(f"  {status} | {descricao}")
    if resultado != esperado:
        print(f"           Entrada:   '{entrada}'")
        print(f"           Esperado:  {esperado}")
        print(f"           Obtido:    {resultado}")

# teste de entradas válidas
def teste_numeros_inteiros():
    """Testa reconhecimento de números inteiros."""
    print("\n--- Números Inteiros ---")
    verificar(
        "Soma de inteiros simples",
        "(5 3 +)",
        ['(', '5', '3', '+', ')']
    )
    verificar(
        "Inteiros grandes",
        "(100 999 *)",
        ['(', '100', '999', '*', ')']
    )
    verificar(
        "Inteiro zero",
        "(0 5 +)",
        ['(', '0', '5', '+', ')']
    )


def teste_numeros_reais():
    """Testa reconhecimento de números reais."""
    print("\n--- Números Reais ---")
    verificar(
        "Número real simples",
        "(3.14 2.0 *)",
        ['(', '3.14', '2.0', '*', ')']
    )
    verificar(
        "Número real com muitas decimais",
        "(1.23456 7.89 +)",
        ['(', '1.23456', '7.89', '+', ')']
    )
    verificar(
        "Real começando com zero",
        "(0.5 0.25 +)",
        ['(', '0.5', '0.25', '+', ')']
    )


def teste_operadores():
    """Testa todos os operadores válidos da linguagem"""
    print("\n--- Operadores ---")
    verificar("Adição", "(1 2 +)", ['(', '1', '2', '+', ')'])
    verificar("Subtração", "(5 3 -)", ['(', '5', '3', '-', ')'])
    verificar("Multiplicação", "(4 3 *)", ['(', '4', '3', '*', ')'])
    verificar("Divisão real", "(10 3 /)", ['(', '10', '3', '/', ')'])
    verificar("Divisão inteira", "(10 3 //)", ['(', '10', '3', '//', ')'])
    verificar("Resto", "(10 3 %)", ['(', '10', '3', '%', ')'])
    verificar("Potenciação", "(2 3 ^)", ['(', '2', '3', '^', ')'])


def teste_comandos_especiais():
    """Testa os comandos especiais MEM e RES."""
    print("\n--- Comandos Especiais ---")
    verificar(
        "Armazenamento MEM",
        "(10 MEM)",
        ['(', '10', 'MEM', ')']
    )
    verificar(
        "Recuperação MEM",
        "(MEM)",
        ['(', 'MEM', ')']
    )
    verificar(
        "Comando RES com índice",
        "(0 RES)",
        ['(', '0', 'RES', ')']
    )
    verificar(
        "RES dentro de expressão",
        "(0 RES 5 +)",
        ['(', '0', 'RES', '5', '+', ')']
    )
    verificar(
        "MEM em minúscula (deve converter para maiúscula)",
        "(10 mem)",
        ['(', '10', 'MEM', ')']
    )
    verificar(
        "RES em minúscula",
        "(0 res)",
        ['(', '0', 'RES', ')']
    )


def teste_parenteses():
    """Testa expressões com parênteses simples e aninhados"""
    print("\n--- Parênteses ---")
    verificar(
        "Parênteses simples",
        "(5 3 +)",
        ['(', '5', '3', '+', ')']
    )
    verificar(
        "Aninhamento duplo",
        "((5 3 +) (2 4 *) -)",
        ['(', '(', '5', '3', '+', ')', '(', '2', '4', '*', ')', '-', ')']
    )
    verificar(
        "Aninhamento triplo",
        "(((8 2 /) (3 1 +)) *)",
        ['(', '(', '(', '8', '2', '/', ')', '(', '3', '1', '+', ')', ')', '*', ')']
    )


def teste_espacos():
    """Testa tratamento de espaços variados"""
    print("\n--- Espaços ---")
    verificar(
        "Sem espaços",
        "(5 3+)",
        ['(', '5', '3', '+', ')']
    )
    verificar(
        "Espaços extras",
        "(  5   3   +  )",
        ['(', '5', '3', '+', ')']
    )


# teste de entradas inválidas

def teste_numeros_malformados():
    """Testa rejeição de números com formato inválido"""
    print("\n--- Números Malformados (devem retornar None) ---")
    verificar(
        "Dois pontos decimais: 3.14.5",
        "(3.14.5 2 +)",
        None
    )
    verificar(
        "Dois pontos decimais: 15.5.5",
        "(15.5.5 3 +)",
        None
    )
    verificar(
        "Pontos consecutivos: 1..5",
        "(1..5 2 *)",
        None
    )
    verificar(
        "Ponto triplo: 3.14.15",
        "(3.14.15 2 +)",
        None
    )


def teste_caracteres_invalidos():
    """Testa rejeição de caracteres que não pertencem a linguagem"""
    print("\n--- Caracteres Inválidos (devem retornar None) ---")
    verificar(
        "Caractere &",
        "(5 3 &)",
        None
    )
    verificar(
        "Caractere $",
        "(5 3 $)",
        None
    )
    verificar(
        "Caractere @",
        "(@ 5 *)",
        None
    )
    verificar(
        "Caractere #",
        "(5 3 #)",
        None
    )
    verificar(
        "Caractere !",
        "(! 2 3)",
        None
    )


def teste_comandos_desconhecidos():
    """Testa rejeição de palavras que não são MEM nem RES"""
    print("\n--- Comandos Desconhecidos (devem retornar None) ---")
    verificar(
        "Comando MAX",
        "(MAX 5 +)",
        None
    )
    verificar(
        "Comando MEMO (parecido com MEM)",
        "(MEMO 10 +)",
        None
    )
    verificar(
        "Comando RESULT (parecido com RES)",
        "(RESULT 2 +)",
        None
    )
    verificar(
        "Comando SAVE",
        "(SAVE 10)",
        None
    )



if __name__ == "__main__":
    print("=" * 60)
    print("TESTES DO ANALISADOR LÉXICO")
    print("=" * 60)

    # Testes de entradas válidas
    print("\n ENTRADAS VÁLIDAS     ")
    teste_numeros_inteiros()
    teste_numeros_reais()
    teste_operadores()
    teste_comandos_especiais()
    teste_parenteses()
    teste_espacos()

    # Testes de entradas inválidas
    print("\n ENTRADAS INVÁLIDAS ")
    teste_numeros_malformados()
    teste_caracteres_invalidos()
    teste_comandos_desconhecidos()

    #Aqui o resumo do teste
    print("\n" + "=" * 60)
    print(f"RESUMO: {testes_ok}/{total_testes} passaram, {testes_falha} falharam")
    print("=" * 60)

    if testes_falha == 0:
        print("Todos os testes passaram")
    else:
        print(f"ATENÇÃO: {testes_falha} testes falharam")