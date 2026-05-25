import re
import sys
import os

# =======TOKENS=======

TOKENS = [
    ('SUMMON', r'summon'),
    ('LOOT', r'loot'),
    ('BATTLE', r'battle'),
    ('ENDQUEST', r'endquest'),
    ('FARM', r'farm'),
    ('NUMBER', r'\d+'),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('MULT', r'\*'),
    ('DIV', r'/'),
    ('GREATER', r'>'),
    ('LESS', r'<'),
    ('EQUAL', r'='),
    ('SEMICOLON', r';'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('STRING', r'"[^"]*"'),
    ('COMMENT', r'\#.*'),
    ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('SKIP', r'[ \t\n]+'),
    ('MISMATCH', r'.'),
    
]

# ------ANALISADOR LÉXICO------

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []

    def tokenize(self):
        regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKENS)

        for match in re.finditer(regex, self.code):
            kind = match.lastgroup
            value = match.group()

            if kind == 'SKIP' or kind == 'COMMENT':
                continue

            elif kind == 'MISMATCH':
                raise SyntaxError(f'Erro léxico: caractere inválido -> {value}')

            else:
                self.tokens.append((kind, value))

        return self.tokens

# ------ANALISADOR SINTÁTICO------

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.variables = {}

    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return ('EOF', '')

    def eat(self, token_type):
        token = self.current()

        if token[0] == token_type:
            self.pos += 1
            return token

        raise SyntaxError(f'Esperado {token_type}, encontrado {token[0]}')

    def parse(self):
        while self.current()[0] != 'EOF':
            self.statement()
    
    def farm_statement(self):
        self.eat('FARM')

        times = self.expression()

        self.eat('LBRACE')

        # salva posição inicial do bloco
        block_start = self.pos

        # encontra fim do bloco
        brace_count = 1

        while brace_count > 0:
            if self.tokens[self.pos][0] == 'LBRACE':
                brace_count += 1

            elif self.tokens[self.pos][0] == 'RBRACE':
                brace_count -= 1

            self.pos += 1

        block_end = self.pos - 1

        # executa o bloco várias vezes
        for _ in range(times):

            temp_parser = Parser(self.tokens[block_start:block_end])
            temp_parser.variables = self.variables
            temp_parser.parse()

            self.variables.update(temp_parser.variables)

    
    # ------COMANDOS------

    def statement(self):
        token = self.current()

        if token[0] == 'SUMMON':
            self.let_statement()

        elif token[0] == 'LOOT':
            self.print_statement()

        elif token[0] == 'BATTLE':
            self.if_statement()

        elif token[0] == 'FARM':
            self.farm_statement()
        
        elif token[0] == 'ENDQUEST':
            self.endquest_statement()

        else:
            raise SyntaxError(f'Comando inválido: {token}')

    def let_statement(self):
        self.eat('SUMMON')
        name = self.eat('IDENTIFIER')[1]
        self.eat('EQUAL')

        value = self.expression()

        self.variables[name] = value

        self.eat('SEMICOLON')

    def print_statement(self):
        self.eat('LOOT')

        value = self.expression()

        print(value)

        self.eat('SEMICOLON')

    def if_statement(self):
        self.eat('BATTLE')

        condition = self.expression()

        self.eat('LBRACE')

        if condition:
            while self.current()[0] != 'RBRACE':
                self.statement()
        else:
            while self.current()[0] != 'RBRACE':
                self.pos += 1

        self.eat('RBRACE')

    def endquest_statement(self):

        self.eat('ENDQUEST')

        self.eat('SEMICOLON')

        self.pos = len(self.tokens)

     # ------EXPRESSÕES------

    def expression(self):
        left = self.term()

        while self.current()[0] in ('PLUS', 'MINUS', 'GREATER', 'LESS'):
            op = self.current()[0]
            self.pos += 1
            right = self.term()

            if op == 'PLUS':
                left += right

            elif op == 'MINUS':
                left -= right

            elif op == 'GREATER':
                left = left > right

            elif op == 'LESS':
                left = left < right

        return left

    def term(self):
        left = self.factor()

        while self.current()[0] in ('MULT', 'DIV'):
            op = self.current()[0]
            self.pos += 1
            right = self.factor()

            if op == 'MULT':
                left *= right

            elif op == 'DIV':
                left /= right

        return left

    def factor(self):
        token = self.current()

        if token[0] == 'NUMBER':
            self.pos += 1
            return int(token[1])
        
        elif token[0] == 'STRING':
            self.pos += 1
            return token[1].strip('"')

        elif token[0] == 'IDENTIFIER':
            self.pos += 1

            if token[1] not in self.variables:
                raise NameError(f'Variável não definida: {token[1]}')

            return self.variables[token[1]]

        elif token[0] == 'LPAREN':
            self.eat('LPAREN')
            value = self.expression()
            self.eat('RPAREN')
            return value

        else:
            raise SyntaxError(f'Expressão inválida: {token}')

# ------INICIANDO COMPILADOR------

if __name__ == "__main__":
    if len(sys.argv) > 1:
        nome_arquivo = sys.argv[1]
    else:
        print("--------COMPILADOR/INTERPRETADOR RPG-C--------")
        
        # Lista dos arquivos .rpgc
        arquivos_rpgc = [f for f in os.listdir('.') if f.endswith('.rpgc')]
        
        if not arquivos_rpgc:
            print("\nNenhum arquivo '.rpgc' encontrado")
            print("Coloque os arquivos de código na mesma pasta do 'RPGC.py'.")
            sys.exit()
            
        print("\nArquivos encontrados:")
        for idx, arquivo in enumerate(arquivos_rpgc, start=1):
            print(f" [{idx}] {arquivo}")
        
        while True:
            try:
                escolha = int(input("\nDigite o número do arquivo que deseja compilar: "))
                if 1 <= escolha <= len(arquivos_rpgc):
                    nome_arquivo = arquivos_rpgc[escolha - 1]
                    break
                else:
                    print(f"Opção inválida! Escolha um número entre 1 e {len(arquivos_rpgc)}.")
            except ValueError:
                print("Por favor, digite um número válido.")

    print(f"\n[SISTEMA]: Lendo código-fonte de: '{nome_arquivo}'...\n")

    try:
        with open(nome_arquivo, "r", encoding="utf-8", errors="surrogateescape") as file:
            code = file.read()

        lexer = Lexer(code)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        parser.parse()

    except FileNotFoundError:
        print(f"Erro: O arquivo '{nome_arquivo}' não foi encontrado neste diretório")
    except SyntaxError as e:
        print(f"\n[ERRO DE COMPILAÇÃO]: {e}")
    except NameError as e:
        print(f"\n[ERRO SEMÂNTICO]: {e}")
    except Exception as e:
        print(f"\n[ERRO INESPERADO]: {e}")
