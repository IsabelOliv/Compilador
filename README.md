# Interpretador RPG-C

**Aluna:** Isabel Cristina de Souza Oliveira  
**Disciplina:** Compiladores

> **Importante:** Este arquivo README apresenta um resumo executivo do projeto. A documentação teórica completa, contendo as especificações detalhadas do Scanner, do Parser, a modelagem conceitual está disponível no arquivo **[Compilador_RGP-C.pdf](./Compilador_RGP-C.pdf)** presente neste repositório.

---

## Sobre o Projeto
**RPG-C** é um mini-compilador que funciona como um interpretador. Desenvolvido de forma incremental, o sistema realiza a análise e a execução de uma linguagem própria com regras claras, tokens definidos e tratamento de erros integrado.

O projeto está dividido em 3 etapas:
1. **Pré-processamento:** Leitura de arquivos de código externos (`.rpgc`) e tratamento inicial do texto.
2. **Analisador Léxico (Scanner):** Identificação e classificação de lexemas em tokens através de Expressões Regulares.
3. **Analisador Sintático (Parser):** Validação da estrutura dos comandos com base em uma Gramática Livre de Contexto (GLC) e execução em tempo de execução.

---

## Tokens e Estruturas Suportadas
A linguagem reconhece e processa as seguintes estruturas temáticas:

* **`summon` (SUMMON):** Criação e atribuição de variáveis (ex: `summon hp = 100;`).
* **`loot` (LOOT):** Exibição de dados e mensagens no console (ex: `loot hp;`).
* **`battle` (BATTLE):** Estrutura condicional baseada em operadores lógicos (ex: `battle hp > 50 { ... }`).
* **`farm` (FARM):** Estrutura de repetição para loops controlados (ex: `farm 3 { ... }`).
* **`endquest` (ENDQUEST):** Comando obrigatório para encerramento.
* **Operadores:** Suporte nativo para operações aritméticas (`+`, `-`, `*`, `/`) e relacionais (`>`, `<`).

---

## Tratamento de Erros
* **Erro Léxico:** Interrompe a execução ao encontrar caracteres inválidos que não pertencem ao alfabeto da linguagem (ex: `summon hp = 10@`).
* **Erro Sintático:** Interrompe o processo caso a ordem dos tokens viole as regras da gramática (ex: `summon hp 10;` $\rightarrow$ acusa a falta do sinal de igual).

---

## Como Executar
1. Certifique-se de ter o **Python 3** instalado.
2. Mantenha o script `RPGC.py` e os arquivos de teste `.rpgc` (`programa_valido.rpgc`, `erro_lexico.rpgc`, `erro_sintatico.rpgc`) no mesmo diretório.
3. Execute o interpretador no terminal:
   ```bash
   python RPGC.py
