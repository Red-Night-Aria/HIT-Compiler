import ply.lex as lex

# List of token names.
tokens = [
    'INT',
    'REAL',
    'PLUS',
    'SUB',
    'ASSIGN',
    'MULTI',
    'DIV',
    'LPAREN',
    'RPAREN',
    'LBRACKET',
    'RBRACKET',
    'LBRACE',
    'RBRACE',
    'SEMI',
    'COMMA',
    'ID',
    'LITERAL',
    'EOF',
    'BLANK',
    'REL',
    'AND',
    'OR',
    'NOT',
]

reserved = {
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'do': 'DO',
    'function': 'FUNCTION',
    'integer': 'INTEGER',
    'float': 'FLOAT',
    'string': 'STRING',
    'boolean': 'BOOLEAN',
    'return': 'RETURN',
    'define': 'DEFINE',
    'true': 'TRUE',
    'false': 'FALSE',
    'record': 'RECORD'
}

tokens += list(reserved.values())

def createMyLexer():

    def t_newline(t):
        r'((\r\n)|\n)+'
        t.lexer.lineno += len(t.value)

    '''若标识符没法被识别成关键字，则作为变量处理'''
    def t_ID(t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        #print('www')
        t.type = reserved.get(t.value, 'ID')
        return t

    def t_REAL(t):
        r'\d+\.\d+'
        t.value = float(t.value)
        return t

    def t_INT(t):
        r'\d+'
        t.value = int(t.value)
        return t

    # Regular expression rules for simple tokens
    t_REL = r'<=|>=|<|>|!=|=='
    t_AND = r'&&'
    t_OR = r'\|\|'
    t_NOT = r'!'
    t_EOF = r'\$'
    t_PLUS = r'\+'
    t_SUB = r'\-'
    t_MULTI = r'\*'
    t_DIV = r'\/'
    t_ASSIGN = r'='
    t_SEMI = r';'
    t_COMMA = r','
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_LITERAL = r'\"[^\"]*\"'
    t_ignore  = ' \t' # A string containing ignored characters (spaces and tabs)
    t_ignore_COMMENT = r'\#.*'
    t_BLANK = r'\%\$'

    # Error handling rule
    def t_error(t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    return lex.lex()
