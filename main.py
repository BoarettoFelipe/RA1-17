#Integrantes
#Felipe Boaretto - GitHub: BoarettoFelipe
#Igor Mamus - GitHub: igormamus1703
#Grupo Canvas: RA1 17

import sys

def lerArquivo(nomeArquivo):
    linhas = []  #Aqui guardamos as expressões matemáticas
    try:
        with open(nomeArquivo, 'r', encoding='utf-8') as arquivo:
            for linha in arquivo:
                linha_limpa = linha.strip()  #Strip para varrer todos os espaços em branco no começo e final de cada linha
                if linha_limpa:
                    linhas.append(linha_limpa)   #Após a varredura, checa se sobrou texto e ignora linhas vazias
        return linhas
    except FileNotFoundError:
        print(f"Erro arquivo '{nomeArquivo}' não encontrado.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro na leitura: {e}")
        sys.exit(1)

#Aqui iniciamos o Autômato Finito Determinístico
def parseExpressao(linha):
    tokens = []            # Lista que armazenará as palavras válidas
    pos = 0
    tamanho = len(linha)

    def estado_inicial(p):
        if p >= tamanho:
            return None, p      #Rodamos o estado inicial até a linha chegar em seu último caractere

        c = linha[p]    #itera sobre os caracter ao longo da linha
        if c.isspace():
            return estado_inicial(p + 1)   #se o caractere for um espaço, apenas vai ao próximo
        elif c in '()+-*^%':
            return c, p + 1                #se o caractere for algum operador, retorna o operador mais a posição do proximo caractere
        elif c == '/':
            return estado_divisao(p + 1)   #se o caractere for um operador de divisão, checamos se é divisão dupla ou simples
        elif c.isdigit():
            return estado_numero(p, p)     #se o caracte for um número, vamos a função para ver qual numero e seu tamanho
        elif c.isalpha():
            return estado_palavra(p, p)    #se o caracte for uma palavra, vamos a função para ver qual palavra e seu tamanho
        else:
            raise ValueError(f"Caractere inválido: '{c}'")    #Se não cair em nenhuma condição, o caractere é inválido e 'cancela' a linha

    def estado_divisao(p):
        if p < tamanho and linha[p] == '/':
            return '//', p + 1
        return '/', p

    def estado_numero(p, inicio):
        ponto = False          #aqui já tratamos o '.' dos numeros reais, definindo como verdadeiro caso encontremos na string
        while p < tamanho:
            c = linha[p]
            if c.isdigit():
                p += 1
            elif c == '.' and not ponto:
                ponto = True
                p += 1
            elif c == '.' and ponto:
                raise ValueError(f"Número malformado: {linha[inicio:p + 1]}")    #Aqui o tratamento em si, caso haja mais de um ponto por exemplo
            else:
                break          #Se não for um '.' nem um número, simplesmente encerramos pois achamos algum caractere inválido
        return linha[inicio:p], p

    def estado_palavra(p, inicio):
        while p < tamanho and linha[p].isalpha():
            p += 1
        token = linha[inicio:p].upper()        #Recortamos a string original da linha
        if token not in ["RES", "MEM"]:        #Aqui acontece a verificação da string lida, se ela faz parte do nosso vocabulário de comandos especiais
            raise ValueError(f"Comando desconhecido: '{token}'") #Se não faz parte do vocabulário, descartamos essa linha e avançamos para a próxima
        return token, p

    #Começamos aqui
    while pos < tamanho:
        try:
            token, pos = estado_inicial(pos)   #Aqui guardamos a string (Ou o token) e a posição que o programa parou de ler ele
            if token is not None:
                tokens.append(token)  #Avançamos para a leitura do próximo token, com sua nova posição
        except ValueError as e:
            print(f"Erro Léxico -> {e}")
            return None   #Aqui invalidamos e descartamos a linha que não encanxou em nenhum estado de nossa máquina, seja por qualquer tipo de erro

    return tokens

#EXECUÇÃO E VALIDAÇÃO
OPERADORES = {'+', '-', '*', '/', '//', '%', '^'}

def eh_numero(token):
    try:
        float(token)
        return True
    except ValueError:
        return False

def eh_variavel(token):
    return token.isalpha() and token == token.upper() and token != 'RES'

def aplicar_operacao(a, b, operador):
    if operador == '+': return a + b
    elif operador == '-': return a - b
    elif operador == '*': return a * b
    elif operador == '/': return a / b
    elif operador == '//': return float(int(a) // int(b))
    elif operador == '%': return float(int(a) % int(b))
    elif operador == '^': return a ** int(b)
    else: raise ValueError(f"Operador desconhecido: {operador}")

def executarExpressao(tokens, memoria, historico):
    pilha = []
    for token in tokens:
        if token == '(' or token == ')':
            continue
        elif eh_numero(token):
            pilha.append(float(token))
        elif token in OPERADORES:
            if len(pilha) < 2:
                raise ValueError(f"Operandos insuficientes para '{token}'")
            b = pilha.pop()
            a = pilha.pop()
            resultado = aplicar_operacao(a, b, token)
            pilha.append(resultado)
        elif token == 'RES':
            if len(pilha) == 0:
                raise ValueError("RES precisa de N na pilha")
            n = int(pilha.pop())
            if n < 0 or n >= len(historico):
                raise ValueError(f"RES: índice {n} fora do histórico")
            valor = historico[len(historico) - 1 - n]
            pilha.append(valor)
        elif eh_variavel(token):
            if len(pilha) > 0:
                valor = pilha.pop()
                memoria[token] = valor
                pilha.append(valor)
            else:
                pilha.append(memoria.get(token, 0.0))
        else:
            raise ValueError(f"Token desconhecido: '{token}'")

    if len(pilha) != 1:
        raise ValueError(f"Expressão mal formada. Pilha final: {pilha}")
    return pilha[0]

def exibirResultados(resultados):
    print("\n===== RESULTADOS =====")
    for i, r in enumerate(resultados):
        print(f"  Linha {i}: {r:.1f}")
    print("======================\n")

if __name__ == "__main__":
    #Se o tamanho da lista digita no terminal pelo usuário for diferente de 2, tratamos o erro e indicamos como utilizar de forma correta
    if len(sys.argv) != 2:
        print("Para utilizar, rode no terminal: py main.py <arquivo_de_teste.txt>")
        sys.exit(1)

    nome_arquivo = sys.argv[1]
    linhas_lidas = lerArquivo(nome_arquivo)

    todos_tokens = []

    for linha in linhas_lidas:
        tokens = parseExpressao(linha)
        if tokens:
            print(f"Tokens: {tokens}")
            todos_tokens.append(" ".join(tokens))

        # Exporta tokens validos
    with open("tokens.txt", "w", encoding="utf-8") as f:
        for t in todos_tokens:
            f.write(t + "\n")
    print("\nArquivo tokens.txt gerado com sucesso.")

    # VALIDAÇÃO E EXIBIÇÃO
    memoria = {}
    historico = []

    with open("tokens.txt", "r", encoding="utf-8") as f:
        linhas_tokens = [linha.strip() for linha in f if linha.strip()]

    for i, linha in enumerate(linhas_tokens):
        tokens = linha.split()
        try:
            resultado = executarExpressao(tokens, memoria, historico)
            historico.append(resultado)
            print(f"  Linha {i}: {tokens}  →  {resultado:.4f}")
        except ValueError as e:
            print(f"  Linha {i}: ERRO → {e}")
            historico.append(0.0)

    exibirResultados(historico)

    if memoria:
        print("MEMÓRIA FINAL:")
        for nome, valor in memoria.items():
            print(f"  {nome} = {valor:.4f}")