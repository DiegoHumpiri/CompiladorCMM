# Codigo ensamblador:
.data 
# Creacion de variable entero y
var_y:		.word	0:1
# Creacion de variable entero x
var_x:		.word	0:1
# Creacion de variable entero operacion
var_operacion:		.word	0:1
.text 
main:

# Codigo para la declaracion 13

# **************************************************
# Generando codigo para la expresion: 20
# **************************************************

# Codigo generado para una constante entera: 2
li $a0, 2

# Codigo generado para una constante entera: 4
sw $a0 0($sp)
add $sp $sp -4	# Hacemos push
li $a0, 4

# Codigo generado para multiplicar: 

# Cargar de la pila en $t1: 
lw $t1, 4($sp)
mul $a0, $t1, $a0 
add $sp $sp 4	# Hacemos pop

# Codigo generado para una constante entera: 1
sw $a0 0($sp)
add $sp $sp -4	# Hacemos push
li $a0, 1

# Codigo generado para una constante entera: 6
sw $a0 0($sp)
add $sp $sp -4	# Hacemos push
li $a0, 6

# Codigo generado para una constante entera: 2
sw $a0 0($sp)
add $sp $sp -4	# Hacemos push
li $a0, 2

# Codigo generado para dividir: 

# Cargar de la pila en $t1: 
lw $t1, 4($sp)
div $a0, $t1, $a0 
add $sp $sp 4	# Hacemos pop

# Codigo generado para multiplicar: 

# Cargar de la pila en $t1: 
lw $t1, 4($sp)
mul $a0, $t1, $a0 
add $sp $sp 4	# Hacemos pop

# Codigo generado para restar: 

# Cargar de la pila en $t1: 
lw $t1, 4($sp)
sub $a0, $t1, $a0 
add $sp $sp 4	# Hacemos pop

# Codigo generado para la asignacion en una creacion de variable:
la $t1, var_y
sw $a0, 0($t1) 

# ________________________________________________________

# Codigo para la declaracion 58

# ________________________________________________________

# Codigo para la declaracion 66

# **************************************************
# Generando codigo para la expresion: 71
# **************************************************

# Codigo generado para una constante entera: 4
li $a0, 4

# Codigo generado para la asignacion en una declaracion:
la $t1, var_x
sw $a0, 0($t1) 

# ________________________________________________________

# Codigo para la declaracion 81

# **************************************************
# Generando codigo para la expresion: 88
# **************************************************

# Codigo generado para una constante entera: 2
li $a0, 2

# Codigo generado para leer la variable: y
sw $a0 0($sp)
add $sp $sp -4	# Hacemos push
la $t0, var_y
lw $a0 0($t0)

# Codigo generado para una constante entera: 1
sw $a0 0($sp)
add $sp $sp -4	# Hacemos push
li $a0, 1

# Codigo generado para sumar: 

# Cargar de la pila en $t1: 
lw $t1, 4($sp)
add $a0, $a0, $t1
add $sp $sp 4	# Hacemos pop

# Codigo generado para multiplicar: 

# Cargar de la pila en $t1: 
lw $t1, 4($sp)
mul $a0, $t1, $a0 
add $sp $sp 4	# Hacemos pop

# Codigo generado para una constante entera: 20
sw $a0 0($sp)
add $sp $sp -4	# Hacemos push
li $a0, 20

# Codigo generado para leer la variable: x
sw $a0 0($sp)
add $sp $sp -4	# Hacemos push
la $t0, var_x
lw $a0 0($t0)

# Codigo generado para dividir: 

# Cargar de la pila en $t1: 
lw $t1, 4($sp)
div $a0, $t1, $a0 
add $sp $sp 4	# Hacemos pop

# Codigo generado para restar: 

# Cargar de la pila en $t1: 
lw $t1, 4($sp)
sub $a0, $t1, $a0 
add $sp $sp 4	# Hacemos pop

# Codigo generado para la asignacion en una creacion de variable:
la $t1, var_operacion
sw $a0, 0($t1) 

# ________________________________________________________


li $v0, 1
syscall

jr $ra
