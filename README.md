## Projeto para Simulador de Autômatos Finitos

## Autores: Bruno Machado Ferreira, Ernani Neto, Fábio Gomes e Ryan Henrique Nantes

### Testado em:
- Ubuntu 23.04 e 24.04 LTS
- Conda 23.5.0
- Python 3.10.9
 
## Divisão de tarefas:
- Bruno: Memorial, revisão, troubleshooting;
- Ernani: Pesquisa teórica, bibliotecas e snippets;
- Fábio: Desenvolvimento back-end;
- Ryan: Revisão e scripts
  
## Para instalar as dependências para Conda e Python, abra um terminal na pasta do projeto e execute:
- $ source requirements.sh

## Para desativar e reinstalar o ambiente virtual, execute:
- $ source reinstall.sh

## Iniciando o programa
Abra o terminal na pasta do projeto e execute usando Python 3
- $ python3 Simulador.py

## Escolha uma das opções do menu e siga as orientações do terminal.
### Descrição:
O projeto é composto por um menu no terminal para escolher o método de criação do autômato com subpáginas para decidir entre AFD ou AFND.
Selecionando um dos padrões do sistema, o programa vai apresentar o resultado e esperar um ENTER de confirmação. 
Ao confirmar, o programa pedirá uma cadeia para teste, apontará se ela e válida vai demonstrar seu passo a passo pelo autômato.
Selecionando um dos métodos manuais, o programa usa os dados de um autômato(estados, alfabeto, transições, etc.) fornecidos pelo usuário 	 e procede com testes e apresentação, assim como no método automático.
Ao testar uma cadeia válida ou inválida, o programa mostra sua passagem pelos estados do autômato no terminal e destaca na imagem o estado que está sendo passado naquela etapa. Os passos avançam automaticamente em intervalos de 1 segundo até que a cadeia chegue ao fim. 
Cada autômato criado gera 2 arquivos na pasta de execução: 1 de imagem e 1 de texto. O usuário pode usar os arquivos de texto gerados para recriar o respectivo autômato por meio do método do leitor.

### Observações importantes:
1. O método por meio do leitor exige que o arquivo .txt lido siga uma formatação específica, conforme os moldes gerados quando se gera um autômato automático ou manual e também deve estar nomeado como "automato.txt"

2. Recomendamos fechar as instâncias do seu visualizador de imagens antes de gerar outro autômato para evitar inconsistência de performance.

3. Em ISOs Linux novas, pode ocorrer um problema onde o editor de texto do sistema tentará carregar os arquivos de imagem juntamente do visualizador de imagem nativo. Ele apenas mostrará os dados criptografados da imagem e não será problema para o funcionamento do programa. Siga as orientações do terminal normalmente.


