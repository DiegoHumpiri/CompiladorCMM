############################################
#    Analizador lexico del lenguaje C--
############################################
import ply.lex as lex
import pandas as pd
from nltk.tokenize import WhitespaceTokenizer

# Palabras reservadas del lenguaje
reservadas = {
    'principal' : 'PRINCIPAL',
    'si'        : 'SI' ,
    'sino'      : 'SINO',
    'mientras'  : 'MIENTRAS',
    'para'      : 'PARA',
    'funcion'   : 'FUNCION',
    'retornar'  : 'RETORNAR',
    'vacio'     : 'VACIO',
    'boleano'   : 'BOLEANO',
    'entero'    : 'ENTERO',
    'decimal'   : 'DECIMAL',
    'caracter'  : 'CARACTER',
    'cadena'    : 'CADENA',
    'verdadero' : 'VERDADERO',
    'falso'     : 'FALSO'
}

# Lista de tokens
tokens = (
    'NUMERO_ENTERO',
    'NUMERO_DECIMAL',
    'SUMA',
    'RESTA',
    'MULTIPLICACION',
    'DIVISION',
    'NEGACION',
    'CONJUNCION',
    'DISYUNCION',
    'ASIGNACION',
    'IGUAL',
    'DIFERENTE',
    'MENOR_QUE',
    'MENOR_IGUAL_QUE',
    'MAYOR_QUE',
    'MAYOR_IGUAL_QUE',
    'FIN_SENTENCIA',
    'PARENTESIS_DER',
    'PARENTESIS_IZQ',
    'LLAVES_DER',
    'LLAVES_IZQ',
    'COMA',
    'IDENTIFICADOR',
    'COMENTARIOS',
    'LITERAL_CADENA',
    'LITERAL_CARACTER',
) + tuple(reservadas.values())

# Expresiones regulares para los tokens simples
t_SUMA = r'\+'
t_RESTA = r'-'
t_MULTIPLICACION = r'\*'
t_DIVISION = r'/'
t_NEGACION = r'!'
t_CONJUNCION = r'&'
t_DISYUNCION = r'\|'
t_ASIGNACION = r'='
t_IGUAL = r'=='
t_DIFERENTE = r'!='
t_MENOR_QUE = r'<'
t_MENOR_IGUAL_QUE = r'<='
t_MAYOR_QUE = r'>'
t_MAYOR_IGUAL_QUE = r'>='
t_FIN_SENTENCIA = r';'
t_PARENTESIS_DER = r'\)'
t_PARENTESIS_IZQ = r'\('
t_LLAVES_DER = r'}'
t_LLAVES_IZQ = r'{'
t_COMA = r','


# Expresiones regulares complejas
# Numeros decimales
def t_NUMERO_DECIMAL(t):
    r'([0-9][0-9]*)([\.{1}][0-9]*)'
    t.value = float(t.value)
    return t

# Numeros naturales
def t_NUMERO_ENTERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

#Identificadores
def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reservadas.get(t.value, 'IDENTIFICADOR')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print("Caracter ilegal '%s'" % t.value[0])
    t.lexer.skip(1)

def t_COMENTARIOS(t):
    r'(\/\/)([^\n]*\n)'
    pass

# Literal de cadenas
def t_LITERAL_CADENA(t):
   r'\"([^\\\n]|(\\.))*?\"'
   t.value = str(t.value)
   return t

# Literal caracter
def t_LITERAL_CARACTER(t):
   r'\'([^\\\n])\''
   t.value = str(t.value)
   return t

# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

lexer = lex.lex()

class TokenLexico:
  def __init__(self, type, lexeme, line, column):
    self.type = type
    self.lexeme = lexeme
    self.line = line
    self.column = column

def tokenizar( data ):
    listaTokens = []
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokenColumna = find_column(data, tok)
        tokList = TokenLexico(tok.type, tok.value, tok.lineno, tokenColumna)
        listaTokens.append(tokList)
    return listaTokens

def imprimirTokens( listaTokens ):
    print(f'{"# Linea":<10}{"# Columna":<10}{"Tipo":<20}{"Lexema"}')
    for i in range( len(listaTokens) ):
        print(f'{listaTokens[i].line:<10}{listaTokens[i].column:<10}{listaTokens[i].type:<20}{listaTokens[i].lexeme}')

inputTokens = []

with open('test.cmm', mode='r') as fileSource:
#with open('test.cmm', mode='r') as fileSource:
    fileStr = fileSource.read()
    inputTokens = tokenizar(fileStr)

tokenDolar = TokenLexico("$", "$", 0, 0)
inputTokens.append(tokenDolar)

#imprimirTokens(inputTokens)

def imprimirTokensLL1( listaTokens ):
    print(f'{"# Linea":<10}{"# Columna":<10}{"Tipo":<20}{"Lexema"}')
    for i in range( len(listaTokens) ):
        print(listaTokens[i].type, end=" ")

#imprimirTokensLL1(inputTokens)

############################################
#    Analizador sintactico del lenguaje C--
############################################
class node_stack:
  def __init__(self, token):
    global count
    self.token = token
    self.id = count + 1
    count += 1

class node_tree:
  def __init__(self, node):
    self.node = node
    self.children = []
    self.father = None

def buscarNodeTree(id, tree):
  if id == tree.node.id:
    return tree
  for child in tree.children:
    temp = buscarNodeTree(id, child)
    if temp != None:
      return temp
  return None
  
def printTree(tree, level):
  print("<" + str(tree.node.id) + ">" + str(tree.node.type) + " | " + str(level))
  for child in tree.children:
    printTree(child, level + 1)

def printStack(stack):
  print("Stack: ", end="")
  for i in stack:
    print("<" + str(i.id) + ">" + str(i.node.type) + " ", end="")
  print()

#tabla = pd.read_csv("tabla.csv", index_col = 0)
tabla = pd.read_csv("grammar_final.csv", index_col = 0)
#print(tabla)
count = 0
stack = []

# init stack
tokenPrograma = TokenLexico('programa', None, None, None)
symbol_E = node_stack(tokenPrograma)
tokenDollar = TokenLexico('$', None, None, None)
symbol_dollar = node_stack(tokenDollar)
stack.append(symbol_dollar)
stack.append(symbol_E)

# init tree
root = node_tree(symbol_E)

tk = WhitespaceTokenizer()
i = 0
while len(stack) != 0:
  if stack[-1].token.type in tabla.columns or stack[-1].token.type == "e":
    terminal = stack.pop()
    if(inputTokens[i].type == terminal.token.type):
      #buscar en el tree y remplazar con información del token
      tempTokenInfo = buscarNodeTree(terminal.id, root)
      if( tempTokenInfo is not None ):
        if ( tempTokenInfo.node.token.type != '$' ):
          tempTokenInfo.node.token = inputTokens[i]
          #print(f'{inputTokens[i].line:<10}{inputTokens[i].column:<10}{inputTokens[i].type:<20}{inputTokens[i].lexeme}')          
      i = i + 1
    else:
      if terminal.token.type == "e":
        print("", end="")
      else:  
        print("Error. No pertenece al lenguaje.")
        break
  else:
    production = tabla.loc[stack[-1].token.type, inputTokens[i].type]
    production = str(production)
    if production == "nan":
      print("Error produccion. No pertenece al lenguaje.")
      break
    tokens = tk.tokenize(production)
    node_p = stack.pop()
    nodes = []
    nodesTree = []
    tokens = reversed(tokens)
    for r in tokens:
      tokenTemp = TokenLexico( r, None, None, None )
      tempNode = node_stack( tokenTemp )
      tempNodeTree = node_tree( tempNode )
      if tempNode.token.type != "e":
        stack.append(tempNode)  
      nodesTree.append(tempNodeTree)
    node_father = buscarNodeTree(node_p.id, root)
    for child in nodesTree:
      node_father.children.append(child)
      child.father = node_father
if( len(stack) == 0 ):
  print("Pertenece al lenguaje")

def treeToGraphviz(tree, father):
  if(father is not None):  
    #print("Tiene father")
    global graphvizText
    graphvizText = graphvizText + "\"" + str(father.node.id) + "\\n" + str(father.node.token.type) 
    if(father.node.token.lexeme is not None):
      graphvizText = graphvizText + "\\n" + str(father.node.token.lexeme) 
    graphvizText = graphvizText + "\"" 
    graphvizText = graphvizText + " -> " 
    graphvizText = graphvizText + "\"" + str(tree.node.id) + "\\n" + str(tree.node.token.type) 
    if(tree.node.token.lexeme is not None):
      graphvizText = graphvizText + "\\n" + str(tree.node.token.lexeme) 
    graphvizText = graphvizText + "\";"
    
    #graphvizText = graphvizText + " " + tree.symbol + ";"
    graphvizText = graphvizText + "\n"
  #else:
    #print("No tiene father")

  for child in reversed(tree.children):
    treeToGraphviz(child, tree)

if( len(stack) == 0 ):
    graphvizText = "digraph {\n"
    treeToGraphviz(root, None)
    graphvizText = graphvizText +  "} "

    print(graphvizText)

############################################
#    Analizador Semántico del lenguaje C--
############################################

class NodoTablaSimbolo():
  def __init__(self, tipo_dato, identificador, ambito, tipo_identificador):
    self.tipo_dato = tipo_dato
    self.identificador = identificador
    self.ambito = ambito
    self.tipo_identificador = tipo_identificador

tablaSimbolos = []

def imprimirTablaSimbolos(tabla):
  print(f'{"Tipo dato":<15}{"Identificador":<20}{"ambito":<20}{"tipo_identificador"}')
  for node in tabla: 
    print(f'{node.tipo_dato:<15}{node.identificador:<20}{node.ambito:<20}{node.tipo_identificador}')

# Parte I registrar funciones

def registrarFunciones(tree, tabla): 
  if(tree.node.token.type == "funcion"):
    #print("Nombre funcion: " + str(tree.node.id))
    #print("Nombre funcion: " + str(tree.children[10].children[0].node.token.type))
    #print("Nombre funcion: " + str(tree.children[9].node.token.lexeme))
    nodo = NodoTablaSimbolo(tree.children[10].children[0].node.token.type, tree.children[9].node.token.lexeme, "global", "f") # f->funcion o v->variable
    tabla.append(nodo)
  for child in tree.children:
    temp = registrarFunciones(child, tabla)
    if temp != None:
      return temp
  return None

registrarFunciones(root, tablaSimbolos)

def registrarVariables(tree, tabla, ambito):
  if(tree.node.token.type == "funcion"):
     ambito = tree.children[9].node.token.lexeme
  if(tree.node.token.type == "creacion_variable"):
    #print("Ambito: " + ambito)
    #print("Nombre variable: " + str(tree.node.id))
    #print("Nombre variable: " + str(tree.children[2].children[0].node.token.type))
    #print("Nombre variable: " + str(tree.children[1].node.token.lexeme))
    nodo = NodoTablaSimbolo(tree.children[2].children[0].node.token.type, tree.children[1].node.token.lexeme, ambito, "v") # f->funcion o v->variable
    tabla.append(nodo)
  for child in tree.children:
    temp = registrarVariables(child, tabla, ambito)
    if temp != None:
      return temp
  return None

def registrarParametros(tree, tabla, ambito):
  if(tree.node.token.type == "funcion"):
     ambito = tree.children[9].node.token.lexeme
  if(tree.node.token.type == "parametros"):
     print( str( tree.node.id ) + " " + tree.node.token.type )
     #print("Ambito: " + ambito)
     if(tree.children[0].node.token.type == 'e'):
        print( "Nodo e: No tiene parametros" )
     else:
        print( "Tiene parametros" )
        parametro = tree.children[1]
        parametros_ = tree.children[0]
        print( "Parametro: " + str(parametro.node.id) + " " + parametro.node.token.type )
        print( "Parametro tipo: " + str(parametro.children[1].node.id) + " " + str(parametro.children[1].children[0].node.token.type) )
        print( "Parametro identificador: " + str(parametro.children[0].node.id) + " " + str(parametro.children[0].node.token.lexeme) )
        print( "Parametro_: " + str(parametros_.node.id) + " " + parametros_.node.token.type )
        print()

        nodo = NodoTablaSimbolo(parametro.children[1].children[0].node.token.type, parametro.children[0].node.token.lexeme, ambito, "v")
        tabla.append(nodo)

        while parametros_.children[0].node.token.type != 'e':
          parametro = parametros_.children[1]
          parametros_ = parametros_.children[0]
          print( "Parametro: " + str(parametro.node.id) + " " + parametro.node.token.type )
          print( "Parametro_: " + str(parametros_.node.id) + " " + parametros_.node.token.type )
          print( "Parametro: " + str(parametro.node.id) + " " + parametro.node.token.type )
          print( "Parametro tipo: " + str(parametro.children[1].node.id) + " " + str(parametro.children[1].children[0].node.token.type) )
          print( "Parametro identificador: " + str(parametro.children[0].node.id) + " " + str(parametro.children[0].node.token.lexeme) )
          print()

          nodo = NodoTablaSimbolo(parametro.children[1].children[0].node.token.type, parametro.children[0].node.token.lexeme, ambito, "v")
          tabla.append(nodo)
      
  for child in tree.children:
    temp = registrarParametros(child, tabla, ambito)
    if temp != None:
      return temp
  return None

#def analizadorScope(tree, tabla):
#def buscarEnTablaSimbolo(tree):
#def eliminarSimbolo(tree):

 
registrarVariables(root, tablaSimbolos, "global")     
registrarParametros(root, tablaSimbolos, "global")     

imprimirTablaSimbolos(tablaSimbolos)






'''
helpful
https://cs.stackexchange.com/questions/4862/left-factoring-a-grammar-into-ll1
'''