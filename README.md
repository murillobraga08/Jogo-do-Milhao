# Jogo do Milhão

Jogo de perguntas e respostas para computador, inspirado no programa de televisão *Show do Milhão*. O jogador responde a uma sequência de perguntas de múltipla escolha, sobe uma escada de prêmios e pode usar auxílios para aumentar as chances de chegar ao prêmio máximo.

## Sobre o projeto

Este projeto foi desenvolvido como trabalho da disciplina de **Algoritmos**. O objetivo acadêmico foi praticar conceitos de lógica de programação e estruturação de programas: uso de listas e dicionários para armazenar o banco de perguntas, sorteio aleatório de itens, funções para modularizar cada parte do jogo (interface, ranking, banco de dados de perguntas) e tratamento de entrada do usuário.

## Tecnologias

- **Python 3.x** — linguagem principal do projeto
- **CustomTkinter** — biblioteca para construção da interface gráfica (janelas, botões e labels)
- **JSON** — formato de persistência do ranking de jogadores em arquivo
- **Módulo `random`** — sorteio das perguntas exibidas ao jogador

## Requisitos

- Python 3.8 ou superior instalado e disponível no sistema
- Acesso à internet para a instalação da dependência

## Instalação

Clone ou baixe o repositório e, dentro da pasta do projeto, instale a dependência:

```bash
pip install customtkinter
```

## Como executar

```bash
python main.py
```

Uma janela com o título **Show do Milhão** será aberta. Informe seu nome no campo indicado e clique em **COMEÇAR**.

## Como jogar

1. **Informe seu nome** na tela inicial para começar a partida. O nome é usado para registrar seu resultado no ranking.
2. **Leia a pergunta** exibida no painel central e escolha uma das cinco alternativas (A a E).
3. **Selecione a alternativa** clicando nela. A escolha fica destacada em laranja e o botão **CONFIRMAR RESPOSTA** é liberado.
4. **Confirme** para revelar o resultado:
   - **Acertou:** você ganha um ponto e pode seguir para a próxima pergunta.
   - **Errou:** o jogo mostra a alternativa correta, zera a pontuação da partida e encerra o jogo.
5. **Use os auxílios** antes de confirmar, se precisar. Cada um pode ser usado **uma única vez por partida**:
   - **50 / 50** — oculta duas das quatro alternativas erradas, deixando apenas a correta e uma distratora visíveis.
   - **Pular** — descarta a pergunta atual e sorteia uma nova, sem gastar pontos nem errar.
6. **Acompanhe a escada de prêmios** no painel à esquerda. Ela mostra os 15 níveis, de R$ 100 a R$ 1.000.000. Os níveis **8 e 12** aparecem em azul, indicando que são *valores seguros*.
7. **Veja seu ranking** a qualquer momento pelo botão **Ranking** na tela de jogo ou na tela inicial.

O jogo termina quando o jogador erra uma pergunta ou quando o banco de 74 perguntas se esgota — nesse caso, a vitória é declarada.

## Estrutura do projeto

```
Jogo_do_milhao/
├── main.py                 # Ponto de entrada do jogo: telas, estado da partida e lógica das rodadas
├── banco_de_perguntas.py   # Banco com as 74 perguntas (texto, cinco alternativas e gabarito)
├── ranking.py              # Funções de leitura e gravação do ranking em ranking.json
├── .gitignore              # Ignora __pycache__, arquivos .pyc e o ranking.json gerado em execução
└── README.md               # Documentação do projeto
```

O arquivo `ranking.json` é criado automaticamente na primeira partida, com o nome e a pontuação de cada jogador, e é formatado assim:

```json
[
  {
    "nickname": "Murillo",
    "record": 12
  }
]
```

Como é um arquivo gerado em tempo de execução, ele não é versionado no repositório.

## Autor

Desenvolvido por **Murillo Braga** como trabalho da disciplina de Algoritmos.

- GitHub: [murillobraga08](https://github.com/murillobraga08)