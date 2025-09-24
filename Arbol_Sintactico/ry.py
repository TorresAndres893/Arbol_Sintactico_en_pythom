import sys
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout

if len(sys.argv) < 3: #Minimo 2 arguntos a pasar
    print("Error: Se requieren dos argumentos: <archivo_gramatica> <cadena>")
    sys.exit(1)

archivo_entrada = sys.argv[1] #el primer argumento a pasar es la gramatica
cadena = sys.argv[2] #el segundo argumento a pasar es la cadena de prueba

def Leer_grama(archivo_entrada): #funcion para leer la gramatiica para que pueda utilizarse en el programa
    try:
        with open(archivo_entrada, encoding="utf-8") as archivo: 
            lineas = archivo.readlines()
    except FileNotFoundError:
        print(f"Error: El archivo '{archivo_entrada}' no existe")
        sys.exit(1)
    return [linea.strip() for linea in lineas if linea.strip()] # lee las lineas y separa las lineas vacias 

def Guard_Grama(lineas): # funcion para guardar la gramatica 
    gramatica = {}
    terminales_esperados = {'opsuma', 'opmul', 'num', 'id', 'pari', 'pard'}
    no_terminales = set()

    for linea in lineas:#recorrer cada linea de la gramatica para identificar cuales tienen las caracteristcas de las reglas de produccion
        if '->' not in linea:
            print(f"Advertencia: Línea ignorada por no contener '->': '{linea}'")
            continue
        try:
            izquierda, derecha = linea.strip().split('->') #separamos a la izquierda y a la derecha del (->) 
            izquierda = izquierda.strip() # en el lado is¿zquierdo eliminamos cualquier espacio vacio
            if not izquierda: # si no hay nada en la parte izquierda tirar error.
                raise ValueError("La parte izquierda de la producción está vacía")
            no_terminales.add(izquierda) # a la lista de los no terminales añadimos la parte izquierda de la gramatica que efectivamente son los nodos no terminales principales
            derecha = [d.strip().split() for d in derecha.split('|')] 
            if not derecha:
                raise ValueError(f"No se encontraron producciones válidas en la línea: '{linea}'")
            for prod in derecha:
                if not prod:
                    raise ValueError(f"Producción vacía en la línea: '{linea}'")
                for simbolo in prod:
                    if simbolo not in terminales_esperados and simbolo not in no_terminales:
                        no_terminales.add(simbolo)
            if izquierda not in gramatica:
                gramatica[izquierda] = []
            gramatica[izquierda].extend(derecha)
        except ValueError as e:
            print(f"Error procesando línea '{linea}': {e}")
            sys.exit(1)
    if not gramatica:
        print("Error: La gramática está vacía")
        sys.exit(1)
    for izq, producciones in gramatica.items():
        for prod in producciones:
            for simbolo in prod:
                if simbolo not in terminales_esperados and simbolo not in gramatica:
                    print(f"Error: Símbolo '{simbolo}' en la producción '{izq} -> {' '.join(prod)}' no está definido")
                    sys.exit(1)
    return gramatica

def Tokens(cadena):
    token_spec = {
        '+': 'opsuma',
        '-': 'opsuma',
        '*': 'opmul',
        '/': 'opmul',
        '(': 'pari',
        ')': 'pard',
        ' ': 'espacio'
    }
    resultado = []
    i = 0
    while i < len(cadena):
        char = cadena[i]
        if char.strip() == "":
            i += 1
            continue
        if char.isdigit():
            num = char
            while i + 1 < len(cadena) and cadena[i + 1].isdigit():
                i += 1
                num += cadena[i]
            resultado.append(('num', num))
        elif char.isalpha():
            iden = char
            while i + 1 < len(cadena) and (cadena[i + 1].isalnum()):
                i += 1
                iden += cadena[i]
            resultado.append(('id', iden))
        elif char in token_spec:
            if token_spec[char] != 'espacio':
                resultado.append((token_spec[char], char))
        else:
            raise ValueError(f"Carácter no reconocido: '{char}' en posición {i}")
        i += 1
    return resultado

class Nodo:
    def __init__(self, tipo, valor=None):
        self.tipo = tipo
        self.valor = valor
        self.hijos = []

    def agregar_hijo(self, hijo):
        self.hijos.append(hijo)

def parse_E(tokens, pos):
    nodo_izq, pos = parse_T(tokens, pos)
    # Envolver T en E para E -> T
    nodo_e = Nodo("E")
    nodo_e.agregar_hijo(nodo_izq)
    while pos < len(tokens) and tokens[pos][0] == 'opsuma':
        op = tokens[pos]
        pos += 1
        nodo_der, pos = parse_T(tokens, pos)
        nuevo = Nodo("E")
        nuevo.agregar_hijo(nodo_e)
        # Crear nodo opsuma con hijo para el operador
        nodo_opsuma = Nodo("opsuma")
        nodo_opsuma.agregar_hijo(Nodo(op[1]))
        nuevo.agregar_hijo(nodo_opsuma)
        nuevo.agregar_hijo(nodo_der)
        nodo_e = nuevo
    return nodo_e, pos

def parse_T(tokens, pos):
    nodo_izq, pos = parse_F(tokens, pos)
    # Envolver F en T para T -> F
    nodo_t = Nodo("T")
    nodo_t.agregar_hijo(nodo_izq)
    while pos < len(tokens) and tokens[pos][0] == 'opmul':
        op = tokens[pos]
        pos += 1
        nodo_der, pos = parse_F(tokens, pos)
        nuevo = Nodo("T")
        nuevo.agregar_hijo(nodo_t)
        # Crear nodo opmul con hijo para el operador
        nodo_opmul = Nodo("opmul")
        nodo_opmul.agregar_hijo(Nodo(op[1]))
        nuevo.agregar_hijo(nodo_opmul)
        nuevo.agregar_hijo(nodo_der)
        nodo_t = nuevo
    return nodo_t, pos

def parse_F(tokens, pos):
    tok = tokens[pos]
    if tok[0] == 'num' or tok[0] == 'id':
        # Envolver num/id en F y num/id en su propio nodo
        nodo_f = Nodo("F")
        nodo_terminal = Nodo(tok[0])
        nodo_terminal.agregar_hijo(Nodo(tok[1]))
        nodo_f.agregar_hijo(nodo_terminal)
        return nodo_f, pos + 1
    elif tok[0] == 'pari':
        pos += 1
        nodo_e, pos = parse_E(tokens, pos)
        if pos >= len(tokens) or tokens[pos][0] != 'pard':
            raise ValueError("Se esperaba ')'")
        # Envolver pari E pard en F
        nodo_f = Nodo("F")
        nodo_f.agregar_hijo(Nodo("pari", "("))
        nodo_f.agregar_hijo(nodo_e)
        nodo_f.agregar_hijo(Nodo("pard", ")"))
        pos += 1
        return nodo_f, pos
    else:
        raise ValueError(f"Token inesperado en F: {tok}")

def nodo_a_grafo(nodo, G=None, padre=None, contador=None):
    if G is None:
        G = nx.DiGraph()
    if contador is None:
        contador = {"v": 0}
    idx = contador["v"]
    contador["v"] += 1
    # Usar solo el valor para terminales, tipo para no terminales
    etiqueta = nodo.valor if nodo.valor is not None else nodo.tipo
    nombre = f"{nodo.tipo}_{idx}"
    G.add_node(nombre, label=etiqueta)
    if padre is not None:
        G.add_edge(padre, nombre)
    for hijo in nodo.hijos:
        nodo_a_grafo(hijo, G, nombre, contador)
    return G

def dibujar_arbol(G):
    try:
        pos = graphviz_layout(G, prog='dot')
        labels = nx.get_node_attributes(G, 'label')
        plt.figure(figsize=(12, 6))  # Igual que Código 2
        nx.draw(G, pos, with_labels=True, labels=labels,
                node_size=1000, node_color="red",
                font_size=9, font_weight="bold", arrows=False)
        plt.axis('off')
        plt.savefig("arbol_sintactico.png", dpi=300)
        print("Árbol guardado como 'arbol_sintactico.png'")
    except Exception as e:
        print(f"Error al visualizar el árbol: {e}")

if __name__ == "__main__":
    try:
        lineas = Leer_grama(archivo_entrada)
        gramatica = Guard_Grama(lineas)

        print("Gramática cargada:")
        for izq, der in gramatica.items():
            print(f"{izq} -> {' | '.join(' '.join(p) for p in der)}")

        resultado = Tokens(cadena)
        print("Tokens:", resultado)

        raiz, pos_final = parse_E(resultado, 0)

        if pos_final != len(resultado):
            raise ValueError("No se consumieron todos los tokens")

        G = nodo_a_grafo(raiz)
        dibujar_arbol(G)
        print("Árbol sintáctico generado correctamente.")

    except Exception as e:
        print("Error:", e)
        sys.exit(1)
