# PyConvolve
PyConvolve es una herramienta que permite convolucionar dos señales.
El script está pensado para verificar rápidamente la convolución de dos funciones, 
obteniendo su gráfica. Esto permite conocer la respuesta de un sistema si se conoce la 
función que describe su respuesta impulsiva.

La definición de las funciones se realiza describiendo cada operación de manera literal
Solo se pueden agrupar términos con paréntesis y es posible editar las expresiones, así
como el rango en que se muestran las gráficas en cualquier momento durante una ejecución.


## Operadores
*   \+ Suma
*   \- Resta
*   \* Multiplicación
*   / División
*   |a| Valor absoluto
*   a^b Potenciación

## Funciones
*   Las funciones trigonometricas: Se definen en minúscula. La función seno se llama con sin(t)
*   Impulso: se invoca con d(t-T0), crea un impulso en T0.
    *   Nota: El impulso tiene la magnitud del muestreo debido a que scipy.signal.convolve() trata los datos de forma discreta y no continua.
*   Escalon unitario: se utiliza con u(t-T0). Vale 1 para todo valor mayor o igual a T0
*   Pulso: se utiliza con p(inicio, final). Esta función es equivalente a tener la expresión  
    ```"u(t-inicio)-u(t-final)"```. Su propósito es simplificar la función insertada

## Ejemplo de funciones
Es posible tener un sistema que actúe como filtro pasabaja si su entrada impulsiva es  
```sin(t)*p(0,pi)```  
Por lo que si la entrada del sistema posee una señal periodica de baja frecuencia mezclada con otra señal de frecuencia alta, por ejemplo  
```0.5*cos(10*t)+sin(t)```  
La respuesta carecerá de las frecuencias altas del coseno. fuente: The Scientist and Engineer's Guide to Digital Signal Processing. Steven W. Smith  

## Dependencias
* Python 3.10.6+
* MatPlotLib
* SciPy
* Numpy

Para instalarlas, se debe ingresar al directorio del proyecto

```bash
cd PyConvolve
```

E instalar las dependencias con el siguiente comando:

```bash
pip install -r requirements.txt
```
