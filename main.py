#Integrantes
#Felipe Boaretto - GitHub: BoarettoFelipe
#Igor Mamus - GitHub: igormamus1703
#Grupo Canvas: RA1 17

import sys
import struct

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
    else: raise ValueError(f"operador desconhecido: {operador}")

def executarExpressao(tokens, memoria, historico):
    pilha = []
    for token in tokens:
        if token == '(' or token == ')':
            continue
        elif eh_numero(token):
            pilha.append(float(token))
        elif token in OPERADORES:
            if len(pilha) < 2:
                raise ValueError(f"operandos insuficientes para '{token}'")
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
            raise ValueError(f"token desconhecido: '{token}'")

    if len(pilha) != 1:
        raise ValueError(f"expressão mal formada. Pilha final: {pilha}")
    return pilha[0]

def exibirResultados(resultados):
    print("\n===== RESULTADOS =====")
    for i, r in enumerate(resultados):
        print(f"  Linha {i}: {r:.1f}")
    print("======================\n")
def double_para_words(valor):
    
    #converte um float Python para dois .word de 32 bits (little-endian).
    #necessário porque o ARMv7 armazena doubles como dois words de 32 bits.
    #ex: 5.0 → .word 0x00000000, 0x40140000
    
    empacotado = struct.pack('<d', valor)
    low = struct.unpack('<I', empacotado[0:4])[0]
    high = struct.unpack('<I', empacotado[4:8])[0]
    return low, high


def gerarAssembly(todas_linhas_tokens, codigo_assembly_path="saida.s"):
    
    #recebe todas as linhas de tokens e gera um arquivo Assembly ARMv7
    #completo e funcional para o CPUlator DE1-SoC.
    

    # ---------------------------------------------------------
    # Fase 1: coletar constantes e variáveis
    # ---------------------------------------------------------
    constantes = {}
    variaveis = set()
    num_linhas = len(todas_linhas_tokens)
    contador_const = 0

    # constantes sempre necessárias
    constantes['0.0'] = 'const_zero'
    constantes['1.0'] = 'const_um'

    for tokens in todas_linhas_tokens:
        for token in tokens:
            if token == '(' or token == ')':
                continue
            elif eh_numero(token):
                val = str(float(token))
                if val not in constantes:
                    constantes[val] = f'const_{contador_const}'
                    contador_const += 1
            elif eh_variavel(token):
                variaveis.add(token)

    # ---------------------------------------------------------
    # Fase 2: gerar seção .data
    # ---------------------------------------------------------
    data_lines = []
    data_lines.append(".data")
    data_lines.append("    .align 3")
    data_lines.append("")
    data_lines.append("    @ === CONSTANTES NUMÉRICAS (IEEE 754, 64 bits) ===")

    for val_str, label in sorted(constantes.items(), key=lambda x: x[1]):
        valor = float(val_str)
        low, high = double_para_words(valor)
        data_lines.append(f"    {label}:  .word 0x{low:08X}, 0x{high:08X}    @ {val_str}")

    data_lines.append("")

    if variaveis:
        data_lines.append("    @ === VARIÁVEIS DE MEMÓRIA ===")
        for var in sorted(variaveis):
            low, high = double_para_words(0.0)
            data_lines.append(f"    var_{var}:  .word 0x{low:08X}, 0x{high:08X}    @ variável {var}")
        data_lines.append("")

    data_lines.append("    @ === HISTÓRICO DE RESULTADOS (para comando RES) ===")
    for i in range(num_linhas):
        low, high = double_para_words(0.0)
        data_lines.append(f"    hist_{i}:  .word 0x{low:08X}, 0x{high:08X}    @ resultado linha {i}")
    data_lines.append("")

    data_lines.append("    @ === RESULTADOS FINAIS ===")
    for i in range(num_linhas):
        low, high = double_para_words(0.0)
        data_lines.append(f"    res_{i}:  .word 0x{low:08X}, 0x{high:08X}    @ resultado linha {i}")
    data_lines.append("")

    # flag de erro e número total de linhas (para validação do RES)
    data_lines.append("    @ === CONTROLE DE ERROS ===")
    data_lines.append(f"    total_linhas:  .word {num_linhas}    @ total de linhas no programa")
    data_lines.append(f"    error_flag:    .word 0               @ 0=ok, 1=erro RES fora do limite")
    data_lines.append("")

    # ---------------------------------------------------------
    # Fase 3: sub-rotinas auxiliares
    # ---------------------------------------------------------
    text_lines = []
    text_lines.append(".text")
    text_lines.append(".global _start")
    text_lines.append("")

    #potenciação ---
    text_lines.append("@ === SUB-ROTINA: Potenciação (d0 ^ d1) ===")
    text_lines.append("@ d0 = base, d1 = expoente inteiro positivo")
    text_lines.append("@ Resultado em d0")
    text_lines.append("sub_pot:")
    text_lines.append("    PUSH {r0, r1, lr}")
    text_lines.append("    VCVT.S32.F64 s4, d1")
    text_lines.append("    VMOV r1, s4")
    text_lines.append("    LDR r0, =const_um")
    text_lines.append("    VLDR d2, [r0]")
    text_lines.append("    CMP r1, #0")
    text_lines.append("    BLE sub_pot_fim")
    text_lines.append("sub_pot_loop:")
    text_lines.append("    VMUL.F64 d2, d2, d0")
    text_lines.append("    SUBS r1, r1, #1")
    text_lines.append("    BNE sub_pot_loop")
    text_lines.append("sub_pot_fim:")
    text_lines.append("    VMOV.F64 d0, d2")
    text_lines.append("    POP {r0, r1, lr}")
    text_lines.append("    BX lr")
    text_lines.append("")

    #divisão inteira (sem SDIV — Cortex-A9 não suporta) ---
    #estratégia: divide como float, trunca para inteiro, converte de volta
    text_lines.append("@ === SUB-ROTINA: Divisão Inteira (d0 // d1) ===")
    text_lines.append("@ Usa VFP: divide como double, trunca para int, volta para double")
    text_lines.append("@ Resultado em d0")
    text_lines.append("sub_div_int:")
    text_lines.append("    PUSH {lr}")
    text_lines.append("    VDIV.F64 d0, d0, d1        @ d0 = a / b (double)")
    text_lines.append("    VCVT.S32.F64 s4, d0        @ s4 = truncar para inteiro")
    text_lines.append("    VCVT.F64.S32 d0, s4        @ d0 = inteiro como double")
    text_lines.append("    POP {lr}")
    text_lines.append("    BX lr")
    text_lines.append("")

    #resto da divisão (sem SDIV) ---
    # estratégia: resto = a - (a // b) * b, tudo em VFP
    text_lines.append("@ === SUB-ROTINA: Resto da Divisão (d0 % d1) ===")
    text_lines.append("@ Usa VFP: resto = a - trunc(a/b) * b")
    text_lines.append("@ Resultado em d0")
    text_lines.append("sub_mod:")
    text_lines.append("    PUSH {lr}")
    text_lines.append("    VMOV.F64 d2, d0             @ d2 = a (backup)")
    text_lines.append("    VDIV.F64 d3, d0, d1         @ d3 = a / b")
    text_lines.append("    VCVT.S32.F64 s4, d3         @ s4 = trunc(a / b)")
    text_lines.append("    VCVT.F64.S32 d3, s4         @ d3 = trunc como double")
    text_lines.append("    VMUL.F64 d3, d3, d1         @ d3 = trunc(a/b) * b")
    text_lines.append("    VSUB.F64 d0, d2, d3         @ d0 = a - trunc(a/b)*b = resto")
    text_lines.append("    POP {lr}")
    text_lines.append("    BX lr")
    text_lines.append("")

    # ---------------------------------------------------------
    # Fase 4: programa principal — código para cada linha
    # ---------------------------------------------------------
    text_lines.append("@ === PROGRAMA PRINCIPAL ===")
    text_lines.append("_start:")
    text_lines.append("")

    for idx_linha, tokens in enumerate(todas_linhas_tokens):
        text_lines.append(f"    @ --- Linha {idx_linha}: {' '.join(tokens)} ---")

        for token in tokens:
            if token == '(' or token == ')':
                continue

            elif eh_numero(token):
                val_str = str(float(token))
                label = constantes[val_str]
                text_lines.append(f"    LDR r0, ={label}")
                text_lines.append(f"    VLDR d0, [r0]             @ d0 = {token}")
                text_lines.append(f"    VPUSH {{d0}}               @ empilha {token}")

            elif token == '+':
                text_lines.append(f"    VPOP {{d1}}                @ b = topo")
                text_lines.append(f"    VPOP {{d0}}                @ a = abaixo")
                text_lines.append(f"    VADD.F64 d0, d0, d1       @ d0 = a + b")
                text_lines.append(f"    VPUSH {{d0}}               @ empilha resultado")

            elif token == '-':
                text_lines.append(f"    VPOP {{d1}}                @ b = topo")
                text_lines.append(f"    VPOP {{d0}}                @ a = abaixo")
                text_lines.append(f"    VSUB.F64 d0, d0, d1       @ d0 = a - b")
                text_lines.append(f"    VPUSH {{d0}}               @ empilha resultado")

            elif token == '*':
                text_lines.append(f"    VPOP {{d1}}                @ b = topo")
                text_lines.append(f"    VPOP {{d0}}                @ a = abaixo")
                text_lines.append(f"    VMUL.F64 d0, d0, d1       @ d0 = a * b")
                text_lines.append(f"    VPUSH {{d0}}               @ empilha resultado")

            elif token == '/':
                text_lines.append(f"    VPOP {{d1}}                @ b = topo")
                text_lines.append(f"    VPOP {{d0}}                @ a = abaixo")
                text_lines.append(f"    VDIV.F64 d0, d0, d1       @ d0 = a / b")
                text_lines.append(f"    VPUSH {{d0}}               @ empilha resultado")

            elif token == '//':
                text_lines.append(f"    VPOP {{d1}}                @ b = topo")
                text_lines.append(f"    VPOP {{d0}}                @ a = abaixo")
                text_lines.append(f"    BL sub_div_int             @ d0 = a // b")
                text_lines.append(f"    VPUSH {{d0}}               @ empilha resultado")

            elif token == '%':
                text_lines.append(f"    VPOP {{d1}}                @ b = topo")
                text_lines.append(f"    VPOP {{d0}}                @ a = abaixo")
                text_lines.append(f"    BL sub_mod                 @ d0 = a %% b")
                text_lines.append(f"    VPUSH {{d0}}               @ empilha resultado")

            elif token == '^':
                text_lines.append(f"    VPOP {{d1}}                @ expoente")
                text_lines.append(f"    VPOP {{d0}}                @ base")
                text_lines.append(f"    BL sub_pot                 @ d0 = base ^ exp")
                text_lines.append(f"    VPUSH {{d0}}               @ empilha resultado")

            elif token == 'RES':
                #contador único para labels de branch do RES
                res_label = f"res_ok_{idx_linha}_{tokens.index(token)}"
                text_lines.append(f"    VPOP {{d0}}                @ N = linhas atrás")
                text_lines.append(f"    VCVT.S32.F64 s4, d0")
                text_lines.append(f"    VMOV r1, s4                @ r1 = N")
                text_lines.append(f"    MOV r2, #{idx_linha}")
                text_lines.append(f"    SUB r2, r2, #1")
                text_lines.append(f"    SUB r2, r2, r1             @ r2 = índice no histórico")
                #validação: r2 >= 0? ---
                text_lines.append(f"    CMP r2, #0")
                text_lines.append(f"    BLT _error                 @ índice negativo → erro")
                #validação: r2 < idx_linha? ---
                text_lines.append(f"    CMP r2, #{idx_linha}")
                text_lines.append(f"    BGE _error                 @ índice >= linha atual → erro")
                text_lines.append(f"    LDR r0, =hist_0")
                text_lines.append(f"    ADD r0, r0, r2, LSL #3    @ r0 = &hist_0 + idx*8")
                text_lines.append(f"    VLDR d0, [r0]             @ d0 = resultado referenciado")
                text_lines.append(f"    VPUSH {{d0}}               @ empilha valor do RES")

            elif eh_variavel(token):
                # lógica para distinguir (V NOME) de (NOME)
                # encontramos o par de parênteses mais interno que
                # contém a variável. Depois contamos quantos "itens"
                # existem nesse grupo. Um item pode ser:
                # um token simples (número, operador, etc.)
                # uma sub-expressão inteira (...) conta como 1 item
                #
                # se ha 2+ itens E a variável é o último -> ESCRITA
                # se a variável é o único item ->LEITURA
                eh_escrita = False

                # encontrar a posição deste token na lista
                idx_na_lista = None
                for j in range(len(tokens)):
                    if tokens[j] == token and tokens[j] != '(' and tokens[j] != ')':
                        idx_na_lista = j
                        break

                if idx_na_lista is not None:
                    # buscar o ( mais próximo à esquerda (mesmo nível)
                    nivel = 0
                    inicio_grupo = 0
                    for j in range(idx_na_lista - 1, -1, -1):
                        if tokens[j] == ')':
                            nivel += 1
                        elif tokens[j] == '(':
                            if nivel == 0:
                                inicio_grupo = j
                                break
                            nivel -= 1

                    # buscar o ) correspondente à direita
                    nivel = 0
                    fim_grupo = len(tokens) - 1
                    for j in range(idx_na_lista + 1, len(tokens)):
                        if tokens[j] == '(':
                            nivel += 1
                        elif tokens[j] == ')':
                            if nivel == 0:
                                fim_grupo = j
                                break
                            nivel -= 1

                    # contar ITENS no grupo:
                    # tokens simples no nível 0 contam como 1 item
                    # sub-expressões (...) inteiras contam como 1 item
                    itens_no_grupo = []
                    j = inicio_grupo + 1
                    while j < fim_grupo:
                        if tokens[j] == '(':
                            # sub-expressão inteira → conta como 1 item
                            itens_no_grupo.append('(SUBEXPR)')
                            # pular até o ) correspondente
                            nivel_sub = 1
                            j += 1
                            while j < fim_grupo and nivel_sub > 0:
                                if tokens[j] == '(':
                                    nivel_sub += 1
                                elif tokens[j] == ')':
                                    nivel_sub -= 1
                                j += 1
                        else:
                            itens_no_grupo.append(tokens[j])
                            j += 1

                    # se há 2+ itens E a variável é o último → escrita
                    if len(itens_no_grupo) >= 2 and itens_no_grupo[-1] == token:
                        eh_escrita = True

                if eh_escrita:
                    text_lines.append(f"    VPOP {{d0}}                @ valor a armazenar")
                    text_lines.append(f"    LDR r0, =var_{token}")
                    text_lines.append(f"    VSTR d0, [r0]             @ {token} = d0")
                    text_lines.append(f"    VPUSH {{d0}}               @ re-empilha")
                else:
                    text_lines.append(f"    LDR r0, =var_{token}")
                    text_lines.append(f"    VLDR d0, [r0]             @ d0 = {token}")
                    text_lines.append(f"    VPUSH {{d0}}               @ empilha variável")

        # resultado da linha → salvar no histórico e resultados
        text_lines.append(f"    VPOP {{d0}}                @ resultado linha {idx_linha}")
        text_lines.append(f"    LDR r0, =hist_{idx_linha}")
        text_lines.append(f"    VSTR d0, [r0]             @ salva no histórico")
        text_lines.append(f"    LDR r0, =res_{idx_linha}")
        text_lines.append(f"    VSTR d0, [r0]             @ salva em resultados")
        text_lines.append("")

    #tratamento de erro e fim 
    text_lines.append("    @ === TRATAMENTO DE ERRO ===")
    text_lines.append("    @ Se RES apontar para índice inválido, cai aqui")
    text_lines.append("_error:")
    text_lines.append("    LDR r0, =error_flag")
    text_lines.append("    MOV r1, #1")
    text_lines.append("    STR r1, [r0]               @ error_flag = 1")
    text_lines.append("")
    text_lines.append("    @ === FIM ===")
    text_lines.append("    @ Resultados em res_0 a res_N na memória")
    text_lines.append("    @ Se error_flag = 1, houve erro de RES")
    text_lines.append("_end:")
    text_lines.append("    B _end")

    # ---------------------------------------------------------
    # Fase 5: montar e salvar
    # ---------------------------------------------------------
    assembly_completo = "\n".join(data_lines) + "\n\n" + "\n".join(text_lines) + "\n"

    with open(codigo_assembly_path, 'w', encoding='utf-8') as f:
        f.write(assembly_completo)

    return assembly_completo

if __name__ == "__main__":
    #se o tamanho da lista digita no terminal pelo usuário for diferente de 2, tratamos o erro e indicamos como utilizar de forma correta
    if len(sys.argv) != 2:
        print("Para utilizar, rode no terminal: py main.py <arquivo_de_teste.txt>")
        sys.exit(1)

    nome_arquivo = sys.argv[1]
    linhas_lidas = lerArquivo(nome_arquivo)

    todos_tokens = []
    todos_tokens_lista = []  # lista de listas de tokens, para geração do assembly

    for linha in linhas_lidas:
        tokens = parseExpressao(linha)
        if tokens:
            print(f"Tokens: {tokens}")
            todos_tokens.append(" ".join(tokens))
            todos_tokens_lista.append(tokens)

        # exporta tokens validos
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

    print("\n" + "=" * 50)
    print("ETAPA 3 — GERAÇÃO DO ASSEMBLY ARMv7")
    print("=" * 50)

    codigo = gerarAssembly(todos_tokens_lista, "saida.s")
    print("\nArquivo saida.s gerado com sucesso!")
    print("Cole o conteúdo no CPUlator (ARMv7 DE1-SoC) para executar.")
    print(f"Total de linhas Assembly: {len(codigo.splitlines())}")



