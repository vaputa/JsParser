import ply.lex as lex
import ply.yacc as yacc
import pprint
import sys

reserved = {
    'if' : 'IF', 
    'for' : 'FOR', 
    'define' : 'DEFINE',
    'return' : 'RETURN',
    'function' : 'FUNCTION',
    'true': 'TRUE',
    'false': 'FALSE',
    'var' : 'VAR',
    'if' : 'IF', 
    'else' : 'ELSE'
}

tokens = [
   'NUMBER',
   'PLUS',
   'MINUS',
   'TIMES',
   'DIVIDE',
   'LPAREN',
   'RPAREN',
   'LBRACE',
   'RBRACE',
   'LBRACKET',
   'RBRACKET',
   'COMMA', 
   'SEMICOLON',
   'SQUOTEMARK',
   'DQUOTEMARK',
   'COLON',
   'POINT', 
   'STRING',
   'ID',
   'EQUAL', 
   'QMARK', 
   'SGN'
] + list(reserved.values())

t_POINT     = r'\.'
t_COLON     = r':'
t_COMMA     = r','
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LBRACE    = r'{'
t_RBRACE    = r'}'
t_LBRACKET  = r'\['
t_RBRACKET  = r'\]'
t_SEMICOLON = r';'
t_SQUOTEMARK= r'\''
t_DQUOTEMARK= r'"'
t_QMARK     = r'\?'
t_EQUAL = r'='
t_ignore  = ' \t'

def wrapper(t):
    return t if isinstance(t, list) else [t]

def t_COMMENT(t):
    r'''(/\*.*\*/)|(//.*)'''
    print t.value
    pass

def t_STRING(t):
    r'''("([^"\n]*(\\")*[^"\n]*)?")|('([^'\n]*(\\')*[^'\n]*)?')|(/[^/]+/[^/,;]+)'''
    try:
        t.value = eval(t.value)
    except:
        pass
    return t

def t_ID(t):
    r'''[a-zA-Z_][a-zA-Z_0-9]*'''
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_NUMBER(t):
    r'(\+|-)*\d+(\.?)\d*'
    try:
        t.value = int(t.value)
    except:
        t.value = float(t.value)
    return t

def t_SGN(t):
    r'''(\+|\-|\*|/|\=|\.|\>|\<)+'''
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def p_program(p):
    ''' program         : DEFINE LPAREN function RPAREN
                        | DEFINE LPAREN function RPAREN SEMICOLON
                        | DEFINE LPAREN array COMMA function RPAREN
                        | DEFINE LPAREN array COMMA function RPAREN SEMICOLON
    '''
    if len(p) == 5:
        p[0] = {
            '__type__'  : 'program',
            'parameter' : None,
            'function'  : p[3]
        }
    elif len(p) == 6:
        p[0] = {
            '__type__'  : 'program',
            'parameter' : None,
            'function'  : p[3]
        }
    else:
        p[0] = {
            '__type__'  : 'program',
            'parameter' : p[3],
            'function'  : p[5]
        }

def p_array(p):
    ''' array           : LBRACKET RBRACKET
                        | LBRACKET parameters RBRACKET
    '''
    if len(p) == 3:
        p[0] = []
    elif len(p) == 4:
        p[0] = p[2]

def p_paremeter(p):
    ''' parameters      : expression COMMA parameters
                        | expression
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[3].insert(0, p[1])
        p[0] = p[3]

def p_expression(p):
    ''' expression      : expression SGN expression
                        | expression QMARK expression COLON expression
                        | expression array
                        | VAR parameters
                        | NUMBER
                        | ID
                        | STRING
                        | TRUE 
                        | FALSE
                        | dictionary
                        | array
                        | function

    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 3:
        p[0] = wrapper(p[1]) + wrapper(p[2])
    elif len(p) == 4:
        p[0] = wrapper(p[1]) + wrapper(p[2]) + wrapper(p[3])
    elif len(p) == 5:
        p[0] = wrapper(p[1]) + wrapper(p[2]) + wrapper(p[3]) + wrapper(p[4])        

def p_dictionary(p):
    ''' dictionary      : LBRACE RBRACE
                        | LBRACE kv_pairs 
        kv_pairs        : RBRACE
                        | expression COLON expression RBRACE
                        | expression COLON expression COMMA kv_pairs
    '''
    if len(p) == 2:
        p[0] = {}
    elif len(p) == 3:
        p[0] = p[2] if isinstance(p[2], dict) else {}
    elif len(p) == 5:
        p[0] = {p[1]: p[3]}        
    elif len(p) == 6:
        p[5][p[1]] = p[3]
        p[0] = p[5]

def p_if(p):
    ''' if_statement    : IF LPAREN expression RPAREN statement else_statement
                        | IF LPAREN expression RPAREN LBRACE statements RBRACE else_statement

    '''

def p_else(p):
    ''' else_statement  : empty
                        | ELSE statement
                        | ELSE LBRACE statements RBRACE
    '''

def p_function(p):
    ''' function        : ID LPAREN RPAREN
                        | ID LPAREN parameters RPAREN
                        | FUNCTION LPAREN RPAREN LBRACE statements RBRACE
                        | FUNCTION LPAREN parameters RPAREN LBRACE statements RBRACE
    '''
    if len(p) == 4:
        p[0] = {
            '__type__'  : 'function_call',
            'parameters': None,
            'function'  : p[1]
        }
    elif len(p) == 5:
        p[0] = {
            '__type__'  : 'function_call', 
            'parameters': p[3],
            'function'  : p[1]
        }
    elif len(p) == 7:
        p[0] = {
            '__type__'  : 'function',
            'parameters': None,
            'statements': p[5]
        }
    else:
        p[0] = {
            '__type__'  : 'function',
            'parameters': p[3],
            'statements': p[6]
        }

def p_statements(p):
    ''' statements      : empty
                        | nestatements
        nestatements    : statement 
                        | statement nestatements
    '''
    if p[1]:
        if len(p) == 2:
            p[0] = p[1] if isinstance(p[1], list) else [p[1], ]
        else:
            p[2].insert(0, p[1])
            p[0] = p[2]
    else:
        p[0] = []

def p_statement(p):
    ''' statement       : if_statement
                        | expression SEMICOLON
                        | RETURN expression SEMICOLON
    '''
    if len(p) == 3:
        p[0] = {
            '__type__'  : 'statement',
            'statement' : p[1]
        }
    elif len(p) == 4:
        p[0] = {
            '__type__'  : 'statement',
            'statement' : p[2]
        }
 
def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print("Syntax error at '%s' '%d' " % (p.value, p.lineno))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "useage: python parser.py JS_FILENAME"
        exit()
    try:
        fd = open(sys.argv[1])
    except:
        print "Can not open file"
        exit()

    data = ""
    for line in fd.readlines():
        data += line
    fd.close()

    lexer = lex.lex()
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok: 
            break
        # print(tok)
    parser = yacc.yacc()
    result = parser.parse(data)
    pprint.pprint(result, width=40, depth=8)
