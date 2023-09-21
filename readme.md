# Fenómenos Emergentes en el Juego de la Vida de Conway

## Introducción

Este proyecto tiene como objetivo explorar propiedades emergentes y reduccionistas en el Juego de la Vida de Conway. El Juego de la Vida es un autómata celular creado por John Conway. Es un juego sin jugadores, lo que significa que su evolución está determinada por su estado inicial, sin requerir más intervenciones. El proyecto está diseñado para ejecutar el juego mientras visualiza simultáneamente sus propiedades emergentes y reduccionistas mediante gráficos en tiempo real.

## Cómo Funciona

El proyecto utiliza Python junto con bibliotecas como Cupy para aceleración por GPU, Pygame para la visualización del juego y Matplotlib para graficar en tiempo real. Utiliza multihilo para ejecutar tanto el juego como los gráficos en paralelo, aunque se recomienda precaución al ejecutar bibliotecas basadas en GUI en hilos separados.

### Componentes

- `GameOfLife`: Esta clase maneja la lógica del Juego de la Vida, actualizando el estado de la cuadrícula en cada iteración.
- `App`: Esta clase utiliza Pygame para visualizar el Juego de la Vida. También permite el acercamiento y desplazamiento interactivo.
- `RealTimeGraph`: Esta clase utiliza Matplotlib para trazar gráficos en tiempo real que visualizan propiedades emergentes y reduccionistas del juego.

## Propiedades Emergentes vs. Reduccionistas

### Propiedades Emergentes

En el contexto de este proyecto, la propiedad emergente considerada es la entropía, una medida del desorden o la aleatoriedad. A medida que el juego evoluciona, la entropía cambia de una manera que es difícil de prever con solo mirar las células individuales. Esto sirve como un ejemplo de cómo los sistemas complejos pueden exhibir propiedades que no son fácilmente aparentes a partir de sus partes más pequeñas.

### Propiedades Reduccionistas

Aquí, la propiedad reduccionista es simplemente el recuento de células vivas en cada iteración. Nos da una medida clara y cuantificable, pero carece de la profundidad de comprensión que se obtiene al observar las propiedades emergentes.

## Objetivo Experimental

El objetivo es mostrar que, aunque las propiedades reduccionistas como el recuento de células vivas pueden ser útiles, a menudo pierden la "imagen completa". Las propiedades emergentes como la entropía proporcionan una mejor comprensión del comportamiento del sistema. Al trazar estas propiedades en tiempo real a medida que evoluciona el juego, buscamos demostrar que los fenómenos emergentes son irreducibles a simplemente la suma de las partes individuales.

## Cómo Ejecutar

Ejecute el archivo `main_script.py`. Esto iniciará tanto el juego como los gráficos en tiempo real. Asegúrese de tener todas las bibliotecas requeridas instaladas.

`python main_script.py`

## Nota

Debido a las limitaciones de ejecutar bibliotecas basadas en GUI en hilos separados, es posible que encuentre problemas. Se recomienda ejecutar en un solo hilo si enfrenta tales problemas.

## Conclusión

Este proyecto tiene como objetivo proporcionar un argumento visual convincente para la importancia de considerar fenómenos emergentes al estudiar sistemas complejos, demostrando así que estos fenómenos son irreducibles y no se pueden entender simplemente analizando componentes individuales.
