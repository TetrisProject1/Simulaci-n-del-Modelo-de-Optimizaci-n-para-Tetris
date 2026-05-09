Tetris Optimización con Modelos - Exploración Matemática

Descripcion:
Este programa simula distintas versiones de un modelo matemático para determinar la mejor posición posible para colocar piezas en Tetris. El objetivo es comparar qué tan efectivos y rápidos son diferentes métodos de decisión.

El programa utiliza tres versiones del modelo:

1. Simple

  Evalúa únicamente la pieza actual.
3. Futuro
  
  Evalúa la pieza actual y las siguientes dos piezas visibles.
4. Optimizado
  
  Evalúa la pieza actual y las siguientes tres piezas visibles, utilizando filtros para reducir la cantidad de cálculos necesarios.

Los modelos buscan maximizar:

-Líneas completadas (L)

Y minimizar:

-Altura máxima (H)

-Huecos (O)

-Irregularidad del tablero (I)

-----------------------------------

Cómo usar el programa:

1. Ejecutar el archivo de Python.

2. El programa realizará automáticamente simulaciones para cada modelo.

3. Cada simulación utiliza:

      -Un tablero de 10x20,
   
      -Una secuencia aleatoria de 1000 piezas,
   
      -Semillas específicas para mantener las mismas condiciones entre modelos.
   

Los resultados incluyen:

-Altura máxima alcanzada (H)

-Cantidad de líneas completadas (L)

-Tiempo de ejecución (s)

--Es importante tomar en cuenta que el tiempo de ejecución varía dependiendo de las capacidades de tu computadora--

-----------------------------------

Cómo cambiar experimentos:

Cantidad de piezas:

Modificar el número dentro del paréntesis al final en:
pieces_sequence = [random.choice(list(PIECES.keys())) for _ in range(1000)]

Semillas utilizadas:

Modificar los números en (cada número representa una semilla única):
for seed in [1,2,3,4,5...]

Cantidad de piezas futuras que considera el modelo optimizado:

Modificar el número en:
top_n=3

Cantidad de piezas futuras que considera el modelo a futuro:

Modificar el número en:
depth=2

-----------------------------------

Requisitos:
-Python 3

-Librerías utilizadas:
   
    -random
    
    -time
    
    -copy

No se requieren librerías externas.

---------------------------------------------------------

Autor:
Diego Leal

Exploración Matemática IB
