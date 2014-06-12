# Classic Histogram vs Distribution Steps

`Distrbution Steps` es un estimador de tuplas que satisfacen una condicion, ya sea

- Por igualdad ( a = 2)
- Por menor ( a < 5) o (a <= 5)
- Por mayor ( a > 2) o (a >= 2)

Los estimadores son utilizados en las bases de datos para seleccionar un plan de ejecucion optimo 
para el motor a la hora de realizar una consulta.

Son varios los factores que involucran el calculo de estimadores, como la precision, la cantidad de informacion,
los errores de estimacion, el espacio que consume y la estructura para consultar esa informacion.

Cada uno de estos factores, se ajustan al modificar algunas variables a las que se ajusta este estimador.

Las variables en cuestion son:

- Steps (cantidad en que se divide el 100% de los datos)

--Modificando la cantidad de `steps` en que dividimos el conjunto de datos, o--

A medida que aumentamos el valor de `steps`, aumentamos la precision y disminuimos el error de la estimación.


El beneficio que aporta `Distrbution Steps` podra ser observado al compararlo con `Classic Histogram` y evaluar
diferentes factores.

- El error que comete
- Costo temporal/espacial de construccion
- Costo temporal de consulta


Para entender el funcionamiento de ambos estimadores, creamos el siguiente caso simple de prueba.

[[ EXPLICAR EL EJEMPLO CON PALABRAS Y QUE REPRESENTA ]]

![Imagen Distribution Steps](url)

![Imagen Classic Histogram](url)

## Hipotesis

Basandonos en nuestro simple ejemplo, suponemos que el comportamiento de los distintos estimadores depende de la distribicion de los datos.

Cuando los datos estan agrupados, `Distribucion Steps` nos brinda un menor error en la estimación pero,
cuando los datos estan dispersos el error es mucho mayor que el `Classic Histogram`

A continuacion experimentaremos con datos que siguen una distribucion Uniforme o Normal.

### Generacion casos de prueba

Los casos de prueba los vamos a generar de manera aleatoria, utilizando una funcion que genera numeros aleatorios que siguen una distribucion normal y otra para la uniforme.

(tendran 1000 datos, o mas)



Los dos estimadores los comparamos usando la misma cantidad de bins, porque esa es la informacion que guarda cada uno.
Uno va a tener bins mas altos y otro mas anchos, eso se debe a la particularidad de como se construyen los histogramas.


### Factores

Por la estructura que utilizamos para construir los estimadores y el algoritmo de construccion podemos decir que:

#### Costos

`Classic Histogram`
> Usamos un diccionario

* Creacion: `O( b * n + n)` # + n es el minimo maximo y cantidad total.
* Espacial: `O( 2 * b + 3 )` # + 3 es el minimo maximo y cantidad total. *2 cantidad y acumulado.
* Consulta: `O(1)`

`Distribution Steps`
> Usamos un Array

* Creacion: `O( n*log(n) + n + n)` # lo ordenamos una vez y lo recorremos una vez. el otro +n es max min y total.
* Espacial: `O( b + 1 )` # +1 es la altura..
* Consulta: `O(n)`


> n = cantidad de tuplas
> b = cantidad de bins

### Distribucion Uniforme

Partimos con una base de datos que la información sigue una distribucion Uniforme.

![Grafico Distribution Steps](url)

![Grafico Classic Histogram](url)

#### Conclusion

En el factor de error en la estimacion, los dos estimadores no difieren significativamente dado que 
al tener los datos distribuidos de forma uniforme, la probabilidad de cada elemento es 1/n

( Para rango |a-b|/(max - min))


Como los comparamos con igual cantidad de _bins_ la altura y el ancho de cada uno son similares.


Sin embargo en el factor de `costos de creacion` el `Distribution Steps` es mas caro por que tenemos que ordenar los datos antes de construir el histograma.


Para `consultar` los dos estimadores los representamos como un diccionario, por lo tanto tienen el mismo costo de acceso que un Hash.



Por lo tanto, para datos que cumplen una Distribucion Uniforme, sugerimos implementar `Classic Histogram` por el menor costo de construccion.


### Distribution Normal

Partimos con una base de datos que la información sigue una distribucion Normal.

![Grafico Distribution Steps](url)

![Grafico Classic Histogram](url)

