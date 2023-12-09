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

########################################################################################
##########  Lectura del archivo
########################################################################################
#with open('test.cmm', mode='r') as fileSource:
with open('operaciones_aritmeticas.cmm', mode='r') as fileSource:
#with open('estructuras_si', mode='r') as fileSource:
#with open('funciones.cmm', mode='r') as fileSource:
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
#    Analizador sintáctico del lenguaje C--
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
        #print( "Tiene parametros" )
        parametro = tree.children[1]
        parametros_ = tree.children[0]
        #print( "Parametro: " + str(parametro.node.id) + " " + parametro.node.token.type )
        #print( "Parametro tipo: " + str(parametro.children[1].node.id) + " " + str(parametro.children[1].children[0].node.token.type) )
        #print( "Parametro identificador: " + str(parametro.children[0].node.id) + " " + str(parametro.children[0].node.token.lexeme) )
        #print( "Parametro_: " + str(parametros_.node.id) + " " + parametros_.node.token.type )
        #print()

        nodo = NodoTablaSimbolo(parametro.children[1].children[0].node.token.type, parametro.children[0].node.token.lexeme, ambito, "v")
        tabla.append(nodo)

        while parametros_.children[0].node.token.type != 'e':
          parametro = parametros_.children[1]
          parametros_ = parametros_.children[0]
          #print( "Parametro: " + str(parametro.node.id) + " " + parametro.node.token.type )
          #print( "Parametro_: " + str(parametros_.node.id) + " " + parametros_.node.token.type )
          #print( "Parametro: " + str(parametro.node.id) + " " + parametro.node.token.type )
          #print( "Parametro tipo: " + str(parametro.children[1].node.id) + " " + str(parametro.children[1].children[0].node.token.type) )
          #print( "Parametro identificador: " + str(parametro.children[0].node.id) + " " + str(parametro.children[0].node.token.lexeme) )
          #print()

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

 
#registrarVariables(root, tablaSimbolos, "global")     
#registrarParametros(root, tablaSimbolos, "global")     

#imprimirTablaSimbolos(tablaSimbolos)


''''
    'vacio'     : 'VACIO',
    'boleano'   : 'BOLEANO',
    'entero'    : 'ENTERO',
    'decimal'   : 'DECIMAL',
    'caracter'  : 'CARACTER',
    'cadena'    : 'CADENA',
    'verdadero' : 'VERDADERO',
    'falso'     : 'FALSO'
'''

# recibe un NodeTree type: expresion 
def typeCheckerExpresion(expresion):
   return

def esOperacionBinaria(expresion):
   if len(expresion.children[0].children) == 1 and len(expresion.children[1].children[0].children) == 1:
      return False
   return True

# recibe factor: expresion minima 
def factorTypeChecker(factor):
   if esBoleano(factor):
      return 'BOLEANO'
   if esEntero(factor):
      return 'ENTERO'
   if esDecimal(factor):
      return 'DECIMAL'
   if esCaracter(factor):
      return 'CARACTER'
   if esCadena(factor):
      return 'CADENA'
   return 'DESCONOCIDO'

def esBoleano(factor):   
   if factor.children[0].node.token.type == "VERDADERO":
      return True
   if factor.children[0].node.token.type == "FALSO":
      return True
   return False

def esEntero(factor):
   if factor.children[0].node.token.type == "NUMERO_ENTERO":
      return True
   return False

def esDecimal(factor):
   if factor.children[0].node.token.type == "NUMERO_DECIMAL":
      return True
   return False

def esCaracter(factor):
   if factor.children[0].node.token.type == "LITERAL_CARACTER":
      return True
   return False

def esCadena(factor):
   if factor.children[0].node.token.type == "LITERAL_CADENA":
      return True
   return False

def checkExpresionBinaria(nodoExpresion):
   if len(nodoExpresion.children[0].children) == 1 and len(nodoExpresion.children[1].children[0].children) == 1:
      return

def check_termino(nodoTermino):
   if len(nodoTermino.children[0].childre) == 1:
      return factorTypeChecker(nodoTermino.children[1])
   else :
      return  

def check_expresion_(expresion_):
   if len(expresion_.children[0].children) == 1:
      return [ expresion_.children[2].node.token.type,  ]
   
def getTiposPorOperador(operador):
   if operador == 'SUMA':
      return ['ENTERO', 'DECIMAL', 'CADENA']
   elif operador == 'RESTA':
      return ['ENTERO', 'DECIMAL']
   elif operador == "MULTIPLICACION":
      return ['ENTERO', 'DECIMAL']
   elif operador == "DIVISION":
      return ['ENTERO', 'DECIMAL']
   elif operador == 'CONJUNCION':
      return ['BOLEANO']
   elif operador == 'DISYUNCION':
      return ['BOLEANO']
   elif operador == 'IGUAL':
      return ['ENTERO', 'DECIMAL', 'CARACTER', 'CADENA', 'BOLEANO']
   elif operador == 'DIFERENTE':
      return ['ENTERO', 'DECIMAL', 'CARACTER', 'CADENA', 'BOLEANO']
   elif operador == 'MENOR_IGUAL_QUE':
      return ['ENTERO', 'DECIMAL']
   elif operador == 'MENOR_QUE':
      return ['ENTERO', 'DECIMAL']
   elif operador == 'MAYOR_IGUAL_QUE':
      return ['ENTERO', 'DECIMAL']
   elif operador == 'MAYOR_QUE':
      return ['ENTERO', 'DECIMAL']


#nodeTest = buscarNodeTree(20, root)
#print(nodeTest.node.token.type)
#print(esOperacionBinaria(nodeTest))
#print(esBoleano(nodeTest))
#print(esEntero(nodeTest))
#print(esDecimal(nodeTest))
#print(esCaracter(nodeTest))
#print(esCadena(nodeTest))

print()
##############################################################
###### Generador de Código Assembly MIPS 
##############################################################

'''
def buscarNodeTree(id, tree):
  if id == tree.node.id:
    return tree
  for child in tree.children:
    temp = buscarNodeTree(id, child)
    if temp != None:
      return temp
  return None
'''
codigoGenerado = "# Codigo ensamblador:\n.data \n"

def contarParametros(node):
   parametros_n = 0;
   temp = node
   while temp.children[0].node.token.type != 'e':
      parametros_n = parametros_n + 1
      temp = temp.children[0]

   return parametros_n

ambito = ""
def reservarMemoriaVariables( tree ):
   global ambito
   global codigoGenerado
   #print( str( tree.node.id ) + " " + tree.node.token.type )
   if(tree.node.token.type == "funcion"):
       ambito = tree.children[9].node.token.lexeme
       # Reservar memoria para los parametros de la funcion
       temp = tree.children[7]
       while temp.children[0].node.token.type != 'e':
         if temp.children[1].children[1].children[0].node.token.type == "ENTERO":
            codigoGenerado = codigoGenerado + "# Creacion de variable parametro "
            codigoGenerado = codigoGenerado + temp.children[1].children[1].children[0].node.token.lexeme
            codigoGenerado = codigoGenerado + " " + temp.children[1].children[0].node.token.lexeme         
            codigoGenerado = codigoGenerado + " de la funcion " + ambito

            codigoGenerado = codigoGenerado + "\nvar_" + ambito + "_" + temp.children[1].children[0].node.token.lexeme
            codigoGenerado = codigoGenerado + ":\t\t.word\t0:1\n"   
      
         temp = temp.children[0]

       
   if tree.node.token.type == "creacion_variable":
      if tree.children[2].children[0].node.token.type == "ENTERO":
         codigoGenerado = codigoGenerado + "# Creacion de variable "
         codigoGenerado = codigoGenerado + tree.children[2].children[0].node.token.lexeme
         codigoGenerado = codigoGenerado + " " + tree.children[1].node.token.lexeme
         if ambito == "":
            codigoGenerado = codigoGenerado + "\nvar_" + tree.children[1].node.token.lexeme
         else:
            codigoGenerado = codigoGenerado + " en funcion " + ambito
            codigoGenerado = codigoGenerado + "\nvar_" + ambito + "_" + tree.children[1].node.token.lexeme
         codigoGenerado = codigoGenerado + ":\t\t.word\t0:1\n"
   
   for child in reversed(tree.children):
      reservarMemoriaVariables(child)

def reservarMemoriaVariables1( tree ):
    global ambito
    global codigoGenerado
 
    if(tree.node.token.type == "funcion"):
       ambito = tree.children[9].node.token.lexeme
    if(tree.node.token.type == "programa"):
       ambito = ""
    
    for child in tree.children:
       temp = reservarMemoriaVariables( child )
       if temp != None:
          return temp

    if tree.node.token.type == "creacion_variable":
       if tree.children[2].children[0].node.token.type == "ENTERO":
         
         codigoGenerado = codigoGenerado + "# Creacion de variable "
         codigoGenerado = codigoGenerado + tree.children[2].children[0].node.token.lexeme
         codigoGenerado = codigoGenerado + " " + tree.children[1].node.token.lexeme
         if ambito == "programa":
            codigoGenerado = codigoGenerado + "\nvar_" + tree.children[1].node.token.lexeme
         else:
            codigoGenerado = codigoGenerado + "\nvar_" + ambito + "_" + tree.children[1].node.token.lexeme
         codigoGenerado = codigoGenerado + ":\t\t.word\t0:1\n"
    
    return None

reservarMemoriaVariables( root )

terminales = { 
               'ENTERO', 'DECIMAL', 'CARACTER', 'CADENA', 
               'VERDADERO', 'FALSO', 'NUMERO_ENTERO', 'NUMERO_DECIMAL', 
               'PARENTESIS_DER', 'PARENTESIS_IZQ', 'LLAVES_DER', 'IDENTIFICADOR',
               'LITERAL_CADENA', 'LITERAL_CARACTER', 
               'SUMA', 'RESTA', 'MULTIPLICACION', 'DIVISION', 
               'MENOR_QUE', 'MENOR_IGUAL_QUE', 'MAYOR_QUE', 'MAYOR_IGUAL_QUE',
               'IGUAL', 'DIFERENTE',
             }

expresionFormula = []

def recorrerExpresion( nodoExpresion ):

   for child in reversed(nodoExpresion.children):
      recorrerExpresion(child)
#    if temp != None:
#      return temp
   if nodoExpresion.node.token.type in terminales:
      #print( str(nodoExpresion.node.id) + " " + nodoExpresion.node.token.type + " : " +  str( nodoExpresion.node.token.lexeme )) 
      global expresionFormula
      expresionFormula.append(nodoExpresion.node)


def printExpresionFormula( expresion ):
   for i in expresion:
      print( str(i.id) + " " + i.token.type + " : " +  str( i.token.lexeme ))

#recorrerExpresion( buscarNodeTree(26, root) )

#printExpresionFormula(expresionFormula)

operando = { 
             'ENTERO', 'DECIMAL', 'CARACTER', 'CADENA', 'VERDADERO', 'FALSO', 'NUMERO_ENTERO',
             'NUMERO_DECIMAL', 'IDENTIFICADOR', 'LITERAL_CADENA', 'LITERAL_CARACTER' 
           }
operadores = { 
               'MULTIPLICACION', 'DIVISION', 'SUMA', 'RESTA', 
               'MENOR_QUE', 'MENOR_IGUAL_QUE', 'MAYOR_QUE', 'MAYOR_IGUAL_QUE',
               'IGUAL', 'DIFERENTE',
               'PARENTESIS_DER', 'PARENTESIS_IZQ' 
             }
operadoresPrecedencia = [ 
                          ('MULTIPLICACION', 5), ('DIVISION', 5), 
                          ('SUMA', 4), ('RESTA', 4), 
                          ('MENOR_QUE', 3), ('MENOR_IGUAL_QUE', 3), 
                          ('MAYOR_QUE', 3), ('MAYOR_IGUAL_QUE', 3),
                          ('IGUAL', 2), ('DIFERENTE', 2),
                          ('PARENTESIS_IZQ',1), ('PARENTESIS_DER',1) 
                        ]

pilaOperadores = []
expresionPolaca = []

def convertirNotacionPolaca( expresionFormula ):
   global expresionPolaca
   for token in expresionFormula:
      if token.token.type in operando:
         expresionPolaca.append( token )
      
      elif token.token.type == 'PARENTESIS_IZQ':
         pilaOperadores.append(token)
         
      elif token.token.type == 'PARENTESIS_DER':
         while True:
            tokenTemp = pilaOperadores.pop()            
            if tokenTemp.token.type == 'PARENTESIS_IZQ':
               break
            else:
               expresionPolaca.append(tokenTemp)
               
      elif token.token.type in operadores:
         while not len(pilaOperadores) == 0:
            precedencia = [i for i in operadoresPrecedencia if token.token.type in i]
            precedenciaPila = [i for i in operadoresPrecedencia if pilaOperadores[-1].token.type in i]
            if precedenciaPila[0][1] >= precedencia[0][1]:
               expresionPolaca.append( pilaOperadores.pop() )
            else:
               break

         pilaOperadores.append(token)
   while not len(pilaOperadores) == 0:
      expresionPolaca.append(pilaOperadores.pop())

#convertirNotacionPolaca(expresionFormula)
print()
#printExpresionFormula(expresionPolaca)

constantes = { 'NUMERO_ENTERO' }
variables = { 'IDENTIFICADOR' }

def expresionPolacaAssembly(expresionPolaca, scope):
   global constantes
   global variables
   global operadores
   global codigoGenerado
   acumuladorEnUso = False
   primerOperando = True
   pilaOperandosCode = []
   for token in expresionPolaca:
      if token.token.type in constantes:         
         if primerOperando == True:
            codigoGenerado = codigoGenerado + "\n# Codigo generado para una constante entera: " 
            codigoGenerado = codigoGenerado + str(token.token.lexeme) + "\n"
            codigoGenerado = codigoGenerado + "li $a0, " + str(token.token.lexeme) + "\n"
            primerOperando = False
         else:
            codigoGenerado = codigoGenerado + "\n# Codigo generado para una constante entera: " 
            codigoGenerado = codigoGenerado + str(token.token.lexeme) + "\n"
            codigoGenerado = codigoGenerado + "sw $a0 0($sp)\n"
            codigoGenerado = codigoGenerado + "add $sp $sp -4\t# Hacemos push\n"
            codigoGenerado = codigoGenerado + "li $a0, " + str(token.token.lexeme) + "\n"
      elif token.token.type in variables:
         if primerOperando == True:
            codigoGenerado = codigoGenerado + "\n# Codigo generado para leer la variable: " 
            codigoGenerado = codigoGenerado + str(token.token.lexeme) + "\n"
            if scope == "":
               codigoGenerado = codigoGenerado + "la $t0, var_" + str(token.token.lexeme) + "\n"
            else:
               codigoGenerado = codigoGenerado + "la $t0, var_" + scope + "_" + str(token.token.lexeme) + "\n"
            codigoGenerado = codigoGenerado + "lw $a0 0($t0)\n"
            primerOperando = False
         else:
            codigoGenerado = codigoGenerado + "\n# Codigo generado para leer la variable: " 
            codigoGenerado = codigoGenerado + str(token.token.lexeme) + "\n"
            codigoGenerado = codigoGenerado + "sw $a0 0($sp)\n"
            codigoGenerado = codigoGenerado + "add $sp $sp -4\t# Hacemos push\n"
            if scope == "":
               codigoGenerado = codigoGenerado + "la $t0, var_" + str(token.token.lexeme) + "\n"
            else:
               codigoGenerado = codigoGenerado + "la $t0, var_" + scope + "_" + str(token.token.lexeme) + "\n"
            codigoGenerado = codigoGenerado + "lw $a0 0($t0)\n"

      elif token.token.type in operadores:
         if token.token.type == 'SUMA':
            codigoGenerado = codigoGenerado + "\n# Codigo generado para sumar: \n" 
            codigoGenerado = codigoGenerado + "\n# Cargar de la pila en $t1: \n" 
            codigoGenerado = codigoGenerado + "lw $t1, 4($sp)\n"
            codigoGenerado = codigoGenerado + "add $a0, $a0, $t1\n"
            codigoGenerado = codigoGenerado + "add $sp $sp 4\t# Hacemos pop\n"
         
         if token.token.type == 'RESTA':
            codigoGenerado = codigoGenerado + "\n# Codigo generado para restar: \n" 
            codigoGenerado = codigoGenerado + "\n# Cargar de la pila en $t1: \n" 
            codigoGenerado = codigoGenerado + "lw $t1, 4($sp)\n"
            codigoGenerado = codigoGenerado + "sub $a0, $t1, $a0 \n"
            codigoGenerado = codigoGenerado + "add $sp $sp 4\t# Hacemos pop\n"

         if token.token.type == 'MULTIPLICACION':
            codigoGenerado = codigoGenerado + "\n# Codigo generado para multiplicar: \n" 
            codigoGenerado = codigoGenerado + "\n# Cargar de la pila en $t1: \n" 
            codigoGenerado = codigoGenerado + "lw $t1, 4($sp)\n"
            codigoGenerado = codigoGenerado + "mul $a0, $t1, $a0 \n"
            codigoGenerado = codigoGenerado + "add $sp $sp 4\t# Hacemos pop\n"

         if token.token.type == 'DIVISION':
            codigoGenerado = codigoGenerado + "\n# Codigo generado para dividir: \n" 
            codigoGenerado = codigoGenerado + "\n# Cargar de la pila en $t1: \n" 
            codigoGenerado = codigoGenerado + "lw $t1, 4($sp)\n"
            codigoGenerado = codigoGenerado + "div $a0, $t1, $a0 \n"
            codigoGenerado = codigoGenerado + "add $sp $sp 4\t# Hacemos pop\n"

         if token.token.type == 'MENOR_QUE':
            codigoGenerado = codigoGenerado + "\n# Codigo generado para comparar menor_que: \n" 
            codigoGenerado = codigoGenerado + "\n# Cargar de la pila en $t1: \n" 
            codigoGenerado = codigoGenerado + "lw $t1, 4($sp)\n"
            codigoGenerado = codigoGenerado + "slt $a0, $t1, $a0 \n"
            codigoGenerado = codigoGenerado + "add $sp $sp 4\t# Hacemos pop\n"

         if token.token.type == 'MENOR_IGUAL_QUE': # a < b
            codigoGenerado = codigoGenerado + "\n# Codigo generado para comparar menor_igual_que: \n" 
            codigoGenerado = codigoGenerado + "\n# Cargar de la pila en $t1: \n" 
            codigoGenerado = codigoGenerado + "lw $t1, 4($sp)\n"
            codigoGenerado = codigoGenerado + "move $t2, $a0 \n"
            # a < b  ---> or
            codigoGenerado = codigoGenerado + "slt $t3, $t1, $t2 \n"
            # b < a  ---> not --> or
            codigoGenerado = codigoGenerado + "slt $t4, $t2, $t1 \n"
            # not
            codigoGenerado = codigoGenerado + "not $t4, $t4 \n"
            # or
            codigoGenerado = codigoGenerado + "or $a0, $t3, $t4 \n"
            codigoGenerado = codigoGenerado + "add $a0, $a0, 2 \n"
            codigoGenerado = codigoGenerado + "add $sp $sp 4\t# Hacemos pop\n"

         if token.token.type == 'MAYOR_QUE':
            codigoGenerado = codigoGenerado + "\n# Codigo generado para comparar mayor_que: \n" 
            codigoGenerado = codigoGenerado + "\n# Cargar de la pila en $t1: \n" 
            codigoGenerado = codigoGenerado + "lw $t1, 4($sp)\n"
            codigoGenerado = codigoGenerado + "slt $a0, $a0, $t1 \n"
            codigoGenerado = codigoGenerado + "add $sp $sp 4\t# Hacemos pop\n"
         
         if token.token.type == 'MAYOR_IGUAL_QUE':
            codigoGenerado = codigoGenerado + "\n# Codigo generado para comparar mayor_igual_que: \n" 
            codigoGenerado = codigoGenerado + "\n# Cargar de la pila en $t1: \n" 
            codigoGenerado = codigoGenerado + "lw $t1, 4($sp)\n"
            codigoGenerado = codigoGenerado + "move $t2, $a0 \n"
            # a < b  ---> or
            codigoGenerado = codigoGenerado + "slt $t3, $t2, $t1 \n"
            # b < a  ---> not --> or
            codigoGenerado = codigoGenerado + "slt $t4, $t1, $t2 \n"
            # not
            codigoGenerado = codigoGenerado + "not $t4, $t4 \n"
            # or
            codigoGenerado = codigoGenerado + "or $a0, $t3, $t4 \n"
            codigoGenerado = codigoGenerado + "add $a0, $a0, 2 \n"
            codigoGenerado = codigoGenerado + "add $sp $sp 4\t# Hacemos pop\n"

         if token.token.type == 'IGUAL':
            codigoGenerado = codigoGenerado + "\n# Codigo generado para comparar igual: \n" 
            codigoGenerado = codigoGenerado + "\n# Cargar de la pila en $t1: \n" 
            codigoGenerado = codigoGenerado + "lw $t1, 4($sp)\n"
            codigoGenerado = codigoGenerado + "move $t2, $a0 \n"
            # a < b  ---> or
            codigoGenerado = codigoGenerado + "slt $t3, $t2, $t1 \n"
            # b < a  ---> or
            codigoGenerado = codigoGenerado + "slt $t4, $t1, $t2 \n"
            # or
            codigoGenerado = codigoGenerado + "or $a0, $t3, $t4 \n"
            # not
            codigoGenerado = codigoGenerado + "not $a0, $a0 \n"
            codigoGenerado = codigoGenerado + "add $a0, $a0, 2 \n"
            codigoGenerado = codigoGenerado + "add $sp $sp 4\t# Hacemos pop\n"

         if token.token.type == 'DIFERENTE':
            codigoGenerado = codigoGenerado + "\n# Codigo generado para comparar diferente: \n" 
            codigoGenerado = codigoGenerado + "\n# Cargar de la pila en $t1: \n" 
            codigoGenerado = codigoGenerado + "lw $t1, 4($sp)\n"
            codigoGenerado = codigoGenerado + "move $t2, $a0 \n"
            # a < b  ---> or
            codigoGenerado = codigoGenerado + "slt $t3, $t2, $t1 \n"
            # b < a  ---> or
            codigoGenerado = codigoGenerado + "slt $t4, $t1, $t2 \n"
            # or
            codigoGenerado = codigoGenerado + "or $a0, $t3, $t4 \n"
            codigoGenerado = codigoGenerado + "add $sp $sp 4\t# Hacemos pop\n"

         
print()
print()

def genExpresionAssembly(node, scope):
   global codigoGenerado 
   codigoGenerado = codigoGenerado + "\n# **************************************************\n"
   codigoGenerado = codigoGenerado + "# Generando codigo para la expresion: " + str(node.node.id)
   codigoGenerado = codigoGenerado + "\n# **************************************************\n"
   global expresionFormula
   expresionFormula = []
   recorrerExpresion( node )
   printExpresionFormula(expresionFormula)
   print()
   global expresionPolaca
   global pilaOperadores
   pilaOperadores = []
   expresionPolaca = []
   convertirNotacionPolaca( expresionFormula )
   printExpresionFormula(expresionPolaca)
   print("____________________________________________________")
   expresionPolacaAssembly( expresionPolaca, scope )   


print()
print()

codigoGenerado = codigoGenerado + ".text \nmain:\n"

#expresionPolacaAssembly(expresionPolaca)

#genExpresionAssembly( buscarNodeTree(43, root) )
# tree.children[2].children[0].node.token.lexeme
# tree.children[2].children[0].node.token.type
# node type es declaracion
def genDeclaracionAssembly(node, scope):
   global codigoGenerado 

   # Creacion de variable sin asignacion
   '''
   if node.children[0].node.token.type == "creacion_variable":
      # Generar codigo para la expresion de la asignacion
      genExpresionAssembly(node.children[0].children[0].children[1])
      # Asignar el resultado a la variable
      codigoGenerado = codigoGenerado + "\n# Codigo generado para la asignacion en una creacion de variable:\n" 
      codigoGenerado = codigoGenerado + "la $t1, var_" + node.children[0].children[1].node.token.lexeme + "\n"   
      codigoGenerado = codigoGenerado + "sw $a0, 0($t1) \n"
      return
   '''

   # Creacion de variable con asignacion
   if node.children[0].node.token.type == "creacion_variable":
      # Generar codigo para la expresion de la asignacion

      if len( node.children[0].children[0].children ) == 1:
         # No se realiza ninguna operacion
         return
      else:
         genExpresionAssembly(node.children[0].children[0].children[1], scope)
         # Asignar el resultado a la variable
               
         codigoGenerado = codigoGenerado + "\n# Codigo generado para la asignacion en una creacion de variable:\n" 
         if scope == "":
            codigoGenerado = codigoGenerado + "la $t1, var_" + node.children[0].children[1].node.token.lexeme + "\n"   
         else:
            codigoGenerado = codigoGenerado + "la $t1, var_" + scope + "_" + node.children[0].children[1].node.token.lexeme + "\n"   
         codigoGenerado = codigoGenerado + "sw $a0, 0($t1) \n"
         return
   
   if node.children[0].children[0].node.token.type == "asignacion":
      # Generar codigo para la expresion de la asignacion
      genExpresionAssembly(node.children[0].children[0].children[1], scope)
      # Asignar el resultado a la variable
      codigoGenerado = codigoGenerado + "\n# Codigo generado para la asignacion en una declaracion:\n"   
      if scope == "":
         codigoGenerado = codigoGenerado + "la $t1, var_" + node.children[1].node.token.lexeme + "\n"   
      else:
         codigoGenerado = codigoGenerado + "la $t1, var_" + scope + "_" + node.children[1].node.token.lexeme + "\n"   
      codigoGenerado = codigoGenerado + "sw $a0, 0($t1) \n"
      return

   ##############################################################################################
   # Se evaluara la expresion en si( expresion ): verdadero: 1 ||| falso: 0
   # Ejemplo: 3 > 5 resultado 0, 3 + 1 == 4 resultado 1
   ##############################################################################################
   if node.children[0].children[0].node.token.type == "si":
      codigoGenerado = codigoGenerado + "\n############################################################"
      codigoGenerado = codigoGenerado + "\n# Generar codigo para la estructura de control si, sino     "
      codigoGenerado = codigoGenerado + "\n############################################################\n"
      print(node.children[0].children[0].children[5].node.token.type)
      genExpresionAssembly(node.children[0].children[0].children[5], scope)
      
      codigoGenerado = codigoGenerado + "# Comparacion: si la expresion es 0 (falso) o verdadero (1)\n"
      codigoGenerado = codigoGenerado + "beqz $a0, LABEL_SI_FALSO_"
      codigoGenerado = codigoGenerado + str(node.children[0].children[0].node.id)
      codigoGenerado = codigoGenerado + " # Si ( $a0 == 0 )\n"

      codigoGenerado = codigoGenerado + "LABEL_SI_VERDADERO:  # Si $a0 == 1\n"

      codigoGenerado = codigoGenerado + "# Codigo generado para las declaraciones del si\n"
      genBloqueDeclaracionesAssembly( node.children[0].children[0].children[2], scope)
      
      codigoGenerado = codigoGenerado + "\nb LABEL_END_SI_" + str(node.children[0].children[0].node.id) + "\n\n"

      codigoGenerado = codigoGenerado + "LABEL_SI_FALSO_" + str(node.children[0].children[0].node.id) + ": "
      codigoGenerado = codigoGenerado + " # Si $a0 == 0\n"

      #codigoGenerado = codigoGenerado + "li $a0 20\n\n" ########## - Replace - ########################
      codigoGenerado = codigoGenerado + "# Codigo generado para las declaraciones del sino si las hay\n"
      if len( node.children[0].children[0].children[0].children ) > 1:
         genBloqueDeclaracionesAssembly( node.children[0].children[0].children[0].children[1], scope )

      codigoGenerado = codigoGenerado + "LABEL_END_SI_" + str(node.children[0].children[0].node.id) + ":\n"

      codigoGenerado = codigoGenerado + "\n################### FIN SI SINO #############################\n\n"
      return
   
   '''
   if node.token.type == "creacion_variable":
      codigoGenerado = codigoGenerado + "\n# Codigo generado para la asignacion de la variable: " 
   codigoGenerado = codigoGenerado + + "\n" 
   codigoGenerado = codigoGenerado + "la $t1, var_" + '' + "\n"
   codigoGenerado = codigoGenerado + "sw $a0, 0($t1) \n"
   '''
   
#genDeclaracionAssembly(buscarNodeTree(21, root))

def recorrerDeclaraciones(node): # node.type declaraciones
   temp = node
   while  temp.children[0].node.token.type != 'e':
      #genDeclaracionAssembly( temp.children[1] )
      print( str(temp.children[0].node.id ) + " - " + temp.children[0].node.token.type )
      print( str(temp.children[1].node.id ) + " - " + temp.children[1].node.token.type )
      temp = temp.children[0]
   return

def genBloqueDeclaracionesAssembly( node, scope ):
   global codigoGenerado
   temp = node
   while  temp.children[0].node.token.type != 'e':
      codigoGenerado = codigoGenerado + "\n# Codigo para la declaracion " 
      codigoGenerado = codigoGenerado + str( temp.children[1].node.id ) + "\n" 
      genDeclaracionAssembly( temp.children[1], scope )
      codigoGenerado = codigoGenerado + "\n# ________________________________________________________\n" 
      #print( str(temp.children[0].node.id ) + " - " + temp.children[0].node.token.type )
      #print( str(temp.children[1].node.id ) + " - " + temp.children[1].node.token.type )
      temp = temp.children[0]

#recorrerDeclaraciones( buscarNodeTree( 5, root ) )
#genBloqueDeclaracionesAssembly( buscarNodeTree( 5, root ), "" )


def genCodigoFuncion(node):
   global codigoGenerado
   scope_funcion = node.children[9].node.token.lexeme
   codigoGenerado = codigoGenerado + "\n############################################################"
   codigoGenerado = codigoGenerado + "\n# Generar codigo para la funcion   "
   codigoGenerado = codigoGenerado + "\n############################################################\n"
   
   codigoGenerado = codigoGenerado + node.children[9].node.token.lexeme + ":\n"
   codigoGenerado = codigoGenerado + "move $fp $sp\n"
   codigoGenerado = codigoGenerado + "sw $ra 0($sp)\n"
   codigoGenerado = codigoGenerado + "addiu $sp $sp -4 # Push\n"

   codigoGenerado = codigoGenerado + "### Declaraciones de la funcion\n"

   genBloqueDeclaracionesAssembly( node.children[4], scope_funcion )

   codigoGenerado = codigoGenerado + "### Fin de declaraciones\n"

   codigoGenerado = codigoGenerado + "### Evaluar el return\n"
   genExpresionAssembly( node.children[2].children[0], scope_funcion )

   codigoGenerado = codigoGenerado + "\nlw $ra 4($sp)\n"
   codigoGenerado = codigoGenerado + "addiu $sp $sp 8\n"
   codigoGenerado = codigoGenerado + "lw $fp 0($sp)\n"
   codigoGenerado = codigoGenerado + "jr $ra\n"
   '''
   parametros_c = contarParametros( node.children[7] )
   print(parametros_c)
   
   if parametros_c == 0 :
      codigoGenerado = codigoGenerado + "\nLa funcion no tiene parametros\n"
   if parametros_c == 1:
      codigoGenerado = codigoGenerado + "lw $a0, 8($sp)\n"
      codigoGenerado = codigoGenerado + "sw $a0, 0($sp)\n"
      codigoGenerado = codigoGenerado + "addiu $sp $sp -4 # Push\n"
   '''
   return

def genCodigoLlamadaFuncion(  ):
   # Asignar los valores de los argumentos a las variables parametros
   codigoGenerado = codigoGenerado + "\n#############################################"
   codigoGenerado = codigoGenerado + "\n# Codigo generado de llamada a funcion "
   codigoGenerado = codigoGenerado + "\n#############################################\n"
   codigoGenerado = codigoGenerado + "sw $fp 0($sp)\n"
   codigoGenerado = codigoGenerado + "addiu $sp $sp -4\n"
   codigoGenerado = codigoGenerado + "# Generar codigo para los argumentos \n"
   ### Buscar funcion
   #nodo_funcion = 
   codigoGenerado = codigoGenerado + ""
   codigoGenerado = codigoGenerado + ""
   codigoGenerado = codigoGenerado + ""

   return

def buscarFuncion( tree, nombre ):
   temp = tree
   while temp.children[0].children[0].node.token.type != 'e':
      #genDeclaracionAssembly( temp.children[1] )
      print( str(temp.children[0].node.id ) + " -- " + temp.children[0].node.token.type )
      print( str(temp.children[0].children[1].node.id ) + " -- " + temp.children[0].children[1].node.token.type )
      print( str(temp.children[0].children[1].children[9].node.id ) + " -- " + temp.children[0].children[1].children[9].node.token.lexeme )
      if nombre == temp.children[0].children[1].children[9].node.token.lexeme:
         return temp.children[0].children[1]

      temp = temp.children[0]
   return 

def generarCodigo( tree ):
   genBloqueDeclaracionesAssembly( buscarNodeTree( 5, tree ), "" )
   return

generarCodigo( root )

codigoGenerado = codigoGenerado + "\n\nli $v0, 1\n"
codigoGenerado = codigoGenerado + "syscall\n"
codigoGenerado = codigoGenerado + "\njr $ra\n"


#genCodigoFuncion( buscarNodeTree( 31, root) )

#func = buscarFuncion( root, "fun" )
#print( str( func.node.id )  + " " + func.node.token.type )

#print ( contarParametros(buscarNodeTree( 88, root) ) )

if( len(stack) == 0 ):
   text_file = open("salida.s", "w")
   text_file.write( codigoGenerado )
   text_file.close()
