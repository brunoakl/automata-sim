from graphviz import Digraph
import graphviz
import time
import os

class ESimboloNaoDeclarado(Exception):
    pass

class EEstadoNaoDeclarado(Exception):
    pass

class EAutomatoNaoDeterministico(Exception):
    pass

class AutomatoD:
    def __init__(self, estados, simbolo, funcao_transicao, estado_inicial, estado_final):
        self.estados = estados
        self.simbolo = simbolo
        self.funcao_transicao = funcao_transicao
        self.estado_inicial = estado_inicial
        self.estado_final = estado_final
    
    def gerar_arquivo_txt(self, nome_arquivo):
        numero = 1
        novo_nome_arquivo = nome_arquivo

        while os.path.exists(novo_nome_arquivo):
            nome, extensao = os.path.splitext(nome_arquivo)
            novo_nome_arquivo = f"{nome}{numero}{extensao}"
            numero += 1

        with open(novo_nome_arquivo, 'w') as arquivo:
            arquivo.write(','.join(self.estados) + "\n")
            arquivo.write(','.join(self.simbolo) + "\n")
            arquivo.write(self.estado_inicial + "\n")
            arquivo.write(','.join(self.estado_final) + "\n")
            for estado,transicoes in self.funcao_transicao.items():
                for simbolo, proximo_estado in transicoes.items():
                    arquivo.write(f"{estado},{simbolo},{proximo_estado}\n")

    def accepts(self, cadeia_recebida):
        current_state = self.estado_inicial
        for symbol in cadeia_recebida:
            if symbol not in self.simbolo:
                return False
            current_state = self.funcao_transicao[current_state][symbol]
        return current_state in self.estado_final

    def verificar_cadeia_recebida(self, cadeia_recebida):
        if self.accepts(cadeia_recebida):
            print(f"A cadeia_recebida {cadeia_recebida} é aceita.")
        else:
            print(f"A cadeia_recebida {cadeia_recebida} não é aceita.")

        # Execução passo a passo
        current_state = self.estado_inicial
        passos = []  # Armazena cada passo (símbolo, estado)
        for symbol in cadeia_recebida[0:]:  # Iterar por toda a cadeia de entrada
            if symbol not in self.simbolo:
                print(f"Símbolo '{symbol}' não reconhecido.")
                return
            passos.append((symbol, current_state))
            current_state = self.funcao_transicao[current_state][symbol]
        # Imprime os passos da simulação
        print("Passos da simulação:")
        i = 0
        while i < len(passos):
            
            symbol, state = passos[i]
            print(f"\nPasso {i}: Símbolo='{symbol}', Estado='{state}'")
            print(f"      {symbol}")
            print(f"({state}) --->  \n")
            i += 1
            time.sleep(1)
            show_automato(self, state)  # Mostrar automato com o estado atual destacado em vermelho
        print(f"Estado final: {current_state}\n")
        

        show_automato(self) # Mostrar o automato final após a simulação

def Declarar_automato():
    # Solicita os detalhes do autômato
    estados = input("\nDigite os estados do autômato, separados por vírgulas: ").strip().split(",")
    simbolo = input("Digite o alfabeto do autômato, separado por vírgulas: ").strip().split(",")
    estado_inicial = input("Digite o estado inicial do autômato: ").strip()
    estado_final = input("Digite os estados de aceitação do autômato, separados por vírgulas: ").strip().split(",")

    # Constrói a função de transição
    funcao_transicao = {}
    for state in estados:
        funcao_transicao[state] = {}
        for symbol in simbolo:
            while True:
                if state in estado_final:
                    print(f"\n      {symbol}")
                    transition = input(f"({state}) ---> ").strip()
                else:
                    print(f"\n      {symbol}")
                    transition = input(f" {state}  ---> ").strip()
            
                if transition in estados:
                    break
                print("Transição inválida. Insira novamente.")
        
            funcao_transicao[state][symbol] = transition

    # Cria o automato com os detalhes fornecidos pelo usuário
    automato = AutomatoD(set(estados), set(simbolo), funcao_transicao, estado_inicial, set(estado_final))
    automato.gerar_arquivo_txt('automato.txt')
    return automato


def criar_automato_leitor(arquivo, deterministico):
    with open(arquivo, 'r') as f:
        # Ler as informações do arquivo
        estados = f.readline().strip().split(',')  # Linha 1: Estados
        simbolos = f.readline().strip().split(',')  # Linha 2: Simbolos
        estado_inicial = f.readline().strip()  # Linha 3: Estado inicial
        estado_final = f.readline().strip().split(',')  # Linha 4: Estados Finais

        # Conjunto para armazenar todos os estados e símbolos declarados
        declarados = set(estados + simbolos + [estado_inicial] + estado_final)

        # Voltar para o início do arquivo
        f.seek(0)

        # Pular as primeiras 4 linhas
        for _ in range(4):
            next(f)

        # Definir as transições
        limitador = []
        funcao_transicao = {}
        for linha in f:
            origem, simbolo, destino = linha.strip().split(',')
            if deterministico:
                if limitador.count(origem + simbolo) > 1:
                    raise EAutomatoNaoDeterministico(f"Estado '{origem}' possui mais transições do que permitido!")

            if origem not in declarados:
                raise EEstadoNaoDeclarado(f"Estado '{origem}' não declarado")
            if destino not in declarados:
                raise EEstadoNaoDeclarado(f"Estado '{destino}' não declarado")
            if simbolo not in declarados:
                raise ESimboloNaoDeclarado(f"Símbolo '{simbolo}' não declarado")

            """ automato.edge(origem, destino, label=simbolo) """
            
            if origem not in funcao_transicao:
                funcao_transicao[origem] = {}
            funcao_transicao[origem][simbolo] = destino

    automato_obj = AutomatoD(set(estados), set(simbolos), funcao_transicao, estado_inicial, set(estado_final))
    return automato_obj


def show_automato(automato, current_state=None):
    #automato_graph.attr(rankdir='LR', size='8,5')
    automato_graph = graphviz.Digraph(format='png')

    for estado in automato.estados:
        if estado == automato.estado_inicial:
            shape = 'doubleoctagon' if estado in automato.estado_final else 'Mcircle'
        elif estado in automato.estado_final:
            shape = 'doublecircle'
        else:
            shape = 'circle'
        automato_graph.node(estado, shape=shape)

        if estado == current_state:
            automato_graph.node(estado, shape=shape, color='red')
        else:
            automato_graph.node(estado, shape=shape)

    for estado in automato.estados:
        for simbolo in automato.simbolo:
            destino = automato.funcao_transicao[estado][simbolo]
            automato_graph.edge(estado, destino, label=simbolo)

    automato_graph.view()


# Recebe a escolha do usuário de criar um autômato ou usar o padrão
def cria_automato():
    while True:
        choice = input("\nEscolha seu método de criação:\n1: Manual\n2: Usar padrão do sistema \n3: Leitor de automato por txt \n4: Sair\n--> ").strip()
        
        if choice == '1': # Constrói o automato com base nas entradas do usuário
            automato = Declarar_automato()
            # Mostra o autômato criado
            show_automato(automato)
            
            while True:
                cadeia_recebida = input("\nDigite uma cadeia_recebida de entrada (ou 'sair' para voltar ao menu principal): ")
                if cadeia_recebida.lower() == 'sair':
                    break
                automato.verificar_cadeia_recebida(cadeia_recebida)
            
        elif choice == '2': # Usar autômato pré-definido
            while True:
                choice = input("\nSelecione o tipo do autômato programado:\n1: Automato finito deterministico\n2: Automato finito não deterministico \n3: Voltar ao menu\n--> ").strip()
                
                if choice == '1': #Automato finito deterministico
                    estados = ['q0', 'q1', 'q2']
                    simbolo = ['0', '1']
                    funcao_transicao = {
                        'q0': {'0': 'q0', '1': 'q1'},
                        'q1': {'0': 'q2', '1': 'q1'},
                        'q2': {'0': 'q2', '1': 'q0'}}
                    estado_inicial = 'q0'
                    estado_final = ['q1']
                    # Cria o automato com os detalhes pré-definidos
                    automato = AutomatoD(set(estados), set(simbolo), funcao_transicao, estado_inicial, set(estado_final))
                    # Mostra o autômato
                    time.sleep(1)
                    show_automato(automato)
                    automato.gerar_arquivo_txt('automato.txt')

                    while True:
                        cadeia_recebida = input("\nDigite uma cadeia de entrada (ou 'sair' para voltar ao menu principal): ")
                        if cadeia_recebida.lower() == 'sair':
                            break
                        automato.verificar_cadeia_recebida(cadeia_recebida)

                elif choice == '2': #Automato finito não deterministico 
                    estados = ['q0', 'q1', 'q2', 'q3', 'q4']
                    simbolo = ['a', 'b']
                    funcao_transicao = {
                        'q0': {'a': 'q1', 'b': 'q2'},
                        'q1': {'a': 'q2', 'b': 'q1'},
                        'q2': {'a': 'q3', 'b': 'q4'},
                        'q3': {'a': 'q3', 'b': 'q3'},
                        'q4': {'a': 'q4', 'b': 'q4'}
                    }
                    estado_inicial = 'q0'
                    estado_final = ['q3', 'q4']                   
                    # Cria o automato com os detalhes pré-definidos
                    automato = AutomatoD(set(estados), set(simbolo), funcao_transicao, estado_inicial, set(estado_final))
                    # Mostra o autômato
                    show_automato(automato)
                    automato.gerar_arquivo_txt('automato.txt')

                    while True:
                        cadeia_recebida = input("\nDigite uma cadeia de entrada (ou 'sair' para voltar ao menu principal): ")
                        if cadeia_recebida.lower() == 'sair':
                            break
                        automato.verificar_cadeia_recebida(cadeia_recebida)

                elif choice == '3':
                    break

                else:
                    print("\nInválido. Tente novamente\n") #Reinicia o processo se a opcao e invalida
                
        elif choice == '3': #automato por txt
            while True:
                choice = input("\nSelecione o tipo de autômato:\n1: Automato finito deterministico\n2: Automato finito não deterministico \n3: Voltar ao menu\n--> ").strip()
                
                if choice == '1':
                    try:
                        automato = criar_automato_leitor('automato.txt', deterministico=True)
                    except Exception as E:
                        print(repr(E))
                    else:
                        show_automato(automato)

                    while True:
                        cadeia = input("\nDigite uma cadeia de entrada (ou 'sair' para voltar ao menu principal): ")
                        if cadeia.lower() == 'sair':
                            break
                        automato.verificar_cadeia_recebida(cadeia)

                elif choice == '2':
                    try:
                        automato = criar_automato_leitor('automato.txt', deterministico=False)
                    except Exception as E:
                        print(repr(E))
                    else:
                        show_automato(automato)

                    while True:
                        cadeia = input("\nDigite uma cadeia de entrada (ou 'sair' para voltar ao menu principal): ")
                        if cadeia.lower() == "sair":
                            break
                        automato.verificar_cadeia_recebida(cadeia)

                elif choice == '3':
                    break

                else:
                    print("Inválido. Tente novamente") #Reinicia o processo se a opcao e invalida

        elif choice == '4':
            print('Encerrando\n')
            break
        
        else:
            print("Inválido. Tente novamente") #Reinicia o processo se a opcao e invalida
            
cria_automato()