# Cuadrícula interactiva de círculos

Desarrollo en clase de un Aplicativo de escritorio en Python, que permite visualizar una cuadrícula de 8×8 con círculos transparentes. El usuario interactua con esta mediante el ingreso de unas coordenada (X, Y), tipo matrices de algebra lineal. En donde el círculo correspondiente cambia su estado a rellenado. Es posible seleccionar varias coordenadas, reiniciar la cuadrícula y visualizar las coordenadas elegidas.

## Requisitos

- Python 3 instalado.
- La librería `tkinter`, que viene incluida con Python.
  - En Windows y macOS no se instala nada aparte.
  - En Linux (Ubuntu/Debian), si aparece `ModuleNotFoundError: No module named 'tkinter'`, instálala con:
    ```
    sudo apt install python3-tk
    ```

> Importante: es una aplicación de escritorio, por lo que debe ejecutarse en un computador con entorno gráfico. No funciona en entornos sin pantalla (GitHub Codespaces, servidores remotos por SSH sin `$DISPLAY`).

## Instalación y ejecución

1. Clonar o descargar el repositorio:
   ```
   git clone <URL-del-repositorio>
   ```
2. Entrar a la carpeta del proyecto y ejecutar:
   ```
   python Taller_II_VF.py
   ```
   (Si `python` no funciona, usar `py Taller_II_VF.py` en Windows o `python Taller_II_VF.py`.)

## Uso

1. Escribir un valor en el campo **X** y otro en el campo **Y** (entre 1 y 8).

2. Pulsar **Seleccionar**: el círculo correspondiente se rellena de negro y la coordenada se agrega a la lista inferior.

3. Repetir para seleccionar varias coordenadas.

4. Pulsar **Reiniciar** para volver todos los círculos a transparente y vaciar la lista.

Si la coordenada no es un número o está fuera del rango 1–8, se muestra un mensaje informativo.

## Explicación del código por bloques

**Bloque 1 — Importaciones (líneas 1–2)**
Trae la librería gráfica (`tk`) y el módulo de mensajes emergentes.

**Bloque 2 — Constantes de configuración (líneas 4–6)**
Define los valores base: tamaño de la cuadrícula (`N`), radio de los círculos (`R`) y separación (`PAD`).

**Bloque 3 — Ventana principal (líneas 8–9)**
Crea la ventana y le asigna un título.

**Bloque 4 — Lienzo de dibujo (líneas 11–13)**
Calcula el tamaño del área, crea el Canvas blanco y lo ubica en la ventana.

**Bloque 5 — Estructuras de datos (líneas 15–16)**
`circulos`: diccionario que asocia cada coordenada `(x, y)` con el círculo dibujado.
`seleccionados`: lista de las coordenadas elegidas por el usuario.

**Bloque 6 — Dibujar la cuadrícula (líneas 18–24)**
Dos bucles anidados recorren filas y columnas, calculan el centro de cada círculo y lo dibujan transparente. Avala los requerimientos: RF01, RF02 y RF03.

**Bloque 7 — Función `seleccionar` (líneas 26–41)**
Lee las coordenadas, valida que sean números y que estén en rango, rellena el círculo y actualiza la lista. Avala los requerimientos: RF05, RF06, RF07, RF08 y RF10.

**Bloque 8 — Función `reiniciar` (líneas 43–48)**
Vuelve todos los círculos transparentes y vacía la lista. Avala el requerimiento RF09.

**Bloque 9 — Campos de entrada (líneas 50–56)**
Crea las etiquetas y campos de texto para X e Y. Avala el requerimiento RF04.

**Bloque 10 — Botones (líneas 58–59)**
Botones que llaman a `seleccionar` y `reiniciar` al pulsarlos.

**Bloque 11 — Etiqueta de resultados (líneas 61–62)**
Muestra las coordenadas seleccionadas en la parte inferior.

**Bloque 12 — Bucle principal (línea 64)**
Mantiene la ventana abierta escuchando eventos. Sin esta línea el programa se cerraría al instante.

## Requerimientos funcionales cubiertos

/ ID / Requerimiento / Dónde se cumple/

/ RF01 / Cuadrícula mínima 8×8 / Bloque 6 (`N = 8`)/
/ RF02 / Cada círculo con coordenada (X, Y) / Diccionario `circulos` /
/ RF03 / Círculos transparentes al inicio / `fill=""` en Bloque 6 /
/ RF04 / Ingreso por campos de texto / Bloque 9 /
/ RF05 / Coordenada válida → relleno / Bloque 7 (`itemconfig`) /
/ RF06 / Validar límites / `if 1 <= x <= N and 1 <= y <= N` /
/ RF07 / Mensaje si es inválida / `messagebox` en Bloque 7 /
/ RF08 / Seleccionar varias coordenadas / Lista `seleccionados` /
/ RF09 / Reiniciar la cuadrícula / Bloque 8 /
/ RF10 / Mostrar coordenadas seleccionadas / Etiqueta inferior /
