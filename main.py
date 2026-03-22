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


if __name__ == "__main__":
    #Se o tamanho da lista digita no terminal pelo usuário for diferente de 2, tratamos o erro e indicamos como utilizar de forma correta
    if len(sys.argv) != 2:
        print("Para utilizar, rode no terminal: py main.py <arquivo_de_teste.txt>")
        sys.exit(1)

    nome_arquivo = sys.argv[1]
    linhas_lidas = lerArquivo(nome_arquivo)

    for l in linhas_lidas:
        print(l)


