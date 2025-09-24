# Arbol_Sintactico_en_pythom

Objetivo
Diseñar e implementar un analizador sintáctico en Python para procesar expresiones aritméticas simples, como 2+3 o x+3*3.

El programa recibe dos entradas:

gra.txt: Contiene la gramática que define las reglas de las expresiones aritméticas.
Una cadena de entrada (por ejemplo, x+3*3) proporcionada como argumento en la línea de comandos.

El sistema genera un árbol sintáctico y una visualización en formato PNG, indicando si la cadena es válida según la gramática.

Explicación General del Analizador Sintáctico
Un analizador sintáctico es una herramienta que valida si una cadena cumple con las reglas de una gramática formal y construye un árbol sintáctico que representa su estructura.

Carga de la gramática: Lee las reglas de producción desde "nombre_gramatica".txt.
Análisis léxico: Divide la cadena en tokens (por ejemplo, números, operadores, identificadores).
Análisis sintáctico: Construye el árbol sintáctico siguiendo las reglas de la gramática.
Visualización: Genera un grafo dirigido del árbol sintáctico usando NetworkX y Graphviz.

El analizador comienza con la regla inicial de la gramática (E) y procesa la cadena token por token. Si la cadena sigue las reglas, se genera un árbol sintáctico; de lo contrario, se reporta un error. La salida incluye una imagen PNG del árbol y mensajes en consola sobre el proceso.


Manejo de entrada
Lee la cadena directamente desde la línea de comandos
Usa los tokens generados por el análisis léxico

Control de errores
Detecta caracteres inválidos (ej. @)
Identifica errores sintácticos (ej. paréntesis desbalanceados)

Salida
Lista de tokens en consola
Árbol sintáctico visualizado en PNG y consola


Ejemplo de Salida
python "ejecutable".py "nombre_gramatica".txt "x+3*3"

Salida en consola:
Gramática cargada:
E -> E opsuma T | T
T -> T opmul F | F
F -> id | num | pari E pard

Tokens generados:
[('id', 'x'), ('opsuma', '+'), ('num', '3'), ('opmul', '*'), ('num', '3')]

Análisis sintáctico completado con éxito.
Árbol sintáctico guardado en: arbol_sintactico.png

Casos de prueba:
x+3*3 -> VÁLIDA
2+3 -> VÁLIDA
2++3 -> INVÁLIDA (Error: token no esperado: '+')
(x+3 -> INVÁLIDA (Error: paréntesis desbalanceado)
ε -> INVÁLIDA (Error: cadena vacía no permitida)

Detalles Técnicos
Gramática Utilizada
E -> E opsuma T | T
T -> T opmul F | F
F -> id 
F -> num 
F -> pari E pard

Símbolos

opsuma: + o -
opmul: * o /
id: Identificador alfanumérico (empieza con letra, ej. x, var1)
num: Número entero positivo (ej. 42)pari / pard: Paréntesis de apertura (() y cierre ())

Dependencias

Python 3.8 o superior
Bibliotecas: networkx, matplotlib, pydot
Graphviz instalado y añadido al PATH

Instalación
Para garantizar un entorno limpio y evitar conflictos con otras bibliotecas, es obligatorio usar un entorno virtual (venv) para este proyecto. Sigue estos pasos:

Crear y activar un entorno virtual:
'''bash
python -m venv venv
source venv/bin/activate


Instalar dependencias:Con el entorno virtual activado, ejecuta:
pip install networkx matplotlib pydot

Instalar Graphviz:

Descarga e instala Graphviz desde su sitio oficial.
Asegúrate de añadir Graphviz al PATH del sistema.
Verifica la instalación:dot -V



Advertencia: Si no usas un entorno virtual, podrías tener conflictos con otras versiones de las bibliotecas instaladas globalmente. Además, si Graphviz no está en el PATH, el programa puede ejecutarse, pero no generará la imagen del árbol. En Windows, a veces hay que reiniciar tras instalar Graphviz.

Botas de mejora:

Comprender el  funcionamiento de las gramáticas y los parsers.
Identificar coon mensajes de error.

Problemas Encontrados

Gramáticas mal formadas: Si gra.txt falta un ->, el parser ignora la línea, lo que puede generar árboles incorrectos.
Errores vagos: Mensajes como “token no reconocido” no siempre indican qué causó el problema.
Expresiones incompletas: Cadenas como 2+ generan errores, pero la posición del error no siempre es clara.
