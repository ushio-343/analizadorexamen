from flask import Flask, render_template, request
import ply.lex as lex

app = Flask(__name__)

# Definición de sinónimos en español
sinonimos = {
    'feliz': 'contento', 'contento': 'feliz', 'alegre': 'dichoso', 'dichoso': 'alegre',
    'eufórico': 'exultante', 'satisfecho': 'pleno', 'jovial': 'festivo', 'radiante': 'resplandeciente',
    'optimista': 'positivo', 'entusiasmado': 'emocionado', 'tranquilo': 'sereno', 'sereno': 'tranquilo',
    'plácido': 'calmo', 'sosegado': 'apacible', 'calmado': 'relajado', 'relajado': 'calmado',
    'despreocupado': 'desentendido', 'exultante': 'eufórico', 'jubilos': 'alegre', 'festivo': 'jovial'
}

# Definición de símbolos en español
simbolos = {',', ';', '.', ':', '!', '?', '(', ')', '[', ']', '{', '}'}

# Lista de nombres de tokens
tokens = [
    'SINONIMO', 'SIMBOLO', 'NUMERO', 'ERROR',
    'OPEN_PAREN', 'CLOSE_PAREN', 'OPEN_BRACE', 'CLOSE_BRACE', 'COMMA', 'SEMICOLON',
    'DOT', 'COLON', 'EXCLAMATION', 'QUESTION'
]

# Reglas de expresión regular para tokens simples
t_COMMA = r','
t_SEMICOLON = r';'
t_DOT = r'\.'
t_COLON = r':'
t_EXCLAMATION = r'!'
t_QUESTION = r'\?'
t_OPEN_PAREN = r'\('
t_CLOSE_PAREN = r'\)'
t_OPEN_BRACE = r'\{'
t_CLOSE_BRACE = r'\}'
t_ignore = ' \t\n\r'

# Reglas de expresión regular para identificadores y números
def t_NUMERO(t):
    r'\d+'
    return t

def t_SINONIMO(t):
    r'[a-zA-Záéíóúñ]+'
    if t.value in sinonimos:
        t.type = 'SINONIMO'
    else:
        t.type = 'ERROR'
        t.value = f"Palabra '{t.value}' no reconocida"
    return t

# Manejo de errores
def t_error(t):
    t.type = 'ERROR'
    t.value = f"Carácter ilegal '{t.value[0]}'"
    t.lexer.skip(1)
    return t

# Construcción del lexer
lexer = lex.lex()

@app.route('/', methods=['GET', 'POST'])
def index():
    token_data = []
    totals = {
        'errors': 0, 'open_paren': 0, 'close_paren': 0, 'open_brace': 0, 'close_brace': 0,
        'comma': 0, 'semicolon': 0, 'dot': 0, 'colon': 0, 'exclamation': 0, 'question': 0,
        'numbers': 0, 'synonyms': 0, 'symbols': 0
    }

    if request.method == 'POST':
        code = request.form.get('code', '')
        lexer.input(code)
        row_number = 1
        while (tok := lexer.token()) is not None:
            if tok.type == 'ERROR':
                totals['errors'] += 1
            elif tok.type == 'OPEN_PAREN':
                totals['open_paren'] += 1
            elif tok.type == 'CLOSE_PAREN':
                totals['close_paren'] += 1
            elif tok.type == 'OPEN_BRACE':
                totals['open_brace'] += 1
            elif tok.type == 'CLOSE_BRACE':
                totals['close_brace'] += 1
            elif tok.type == 'COMMA':
                totals['comma'] += 1
            elif tok.type == 'SEMICOLON':
                totals['semicolon'] += 1
            elif tok.type == 'DOT':
                totals['dot'] += 1
            elif tok.type == 'COLON':
                totals['colon'] += 1
            elif tok.type == 'EXCLAMATION':
                totals['exclamation'] += 1
            elif tok.type == 'QUESTION':
                totals['question'] += 1
            elif tok.type == 'NUMERO':
                totals['numbers'] += 1
            elif tok.type == 'SINONIMO':
                totals['synonyms'] += 1
            token_data.append({
                'row': row_number,
                'token': tok.value,
                'synonym': sinonimos.get(tok.value, '') if tok.type == 'SINONIMO' else '',
                'symbol': 'X' if tok.type in {'COMMA', 'SEMICOLON', 'DOT', 'COLON', 'EXCLAMATION', 'QUESTION', 'OPEN_PAREN', 'CLOSE_PAREN', 'OPEN_BRACE', 'CLOSE_BRACE'} else '',
                'number': 'X' if tok.type == 'NUMERO' else '',
                'error': 'X' if tok.type == 'ERROR' else ''
            })
            row_number += 1

    return render_template('web.html', token_data=token_data, totals=totals)

if __name__ == "__main__":
    app.run(debug=True)
