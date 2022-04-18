write_log(S) :- open('error_logs.txt', append, Out), write(Out, S), write(Out, '\n'), close(Out).

/***************
*EJERCICIO 1. slice/4
*
***************/
% Extract a slice from a list

% slice(L1,I,K,L2) :- L2 is the list of the elements of L1 between
%    index I and index K (both included).
%    (list,integer,integer,list) (?,+,+,?)

slice([X|_],1,1,[X]).
slice([X|Xs],1,K,[X|Ys]) :- K > 1, 
   K1 is K - 1, slice(Xs,1,K1,Ys).
slice([_|Xs],I,K,Ys) :- I > 1, 
   I1 is I - 1, K1 is K - 1, slice(Xs,I1,K1,Ys).

/***************
* EJERCICIO 2. sum_pot_prod/4
*
*	ENTRADA:
*		X: Vector de entrada de numeros de valor real.
*		Y: Vector de entrada de numeros de valor real.
*		Potencia: Numero de valor entero, potencia.
*	SALIDA:
*		Resultado: Numero de valor real resultado de la operacion sum_pot_prod. 
*
****************/
sum_pot_prod(_, _, Potencia, _) :- Potencia<0, print('ERROR 1.1 Potencia.'), !, fail.
sum_pot_prod([], _, _, _) :- print('ERROR 1.2 Longitud.'), !, fail.
sum_pot_prod(_, [], _, _) :- print('ERROR 1.2 Longitud.'), !, fail.
sum_pot_prod([A|[]], [B|[]], Potencia, Resultado) :- Resultado is (A*B)^Potencia, !.
sum_pot_prod([A|LA],[B|LB], Potencia, Resultado2) :- sum_pot_prod(LA, LB, Potencia, Resultado), Resultado2 is Resultado+(A*B)^Potencia.


/***************
* EJERCICIO 3. segundo_penultimo/3
*
*       ENTRADA:
*               L: Lista de entrada de numeros de valor real.
*       SALIDA:
*               X : Numero de valor real. Segundo elemento.
*		Y : Numero de valor real. Penultimo elemento.
*
****************/
penultimo([B,_|[]],B) :- !.
penultimo([_|L],X) :- penultimo(L,X).
segundo_penultimo([], _, _) :- print('ERROR 2.1 Longitud.'), !, fail.
segundo_penultimo([_], _, _) :- print('ERROR 2.1 Longitud.'), !, fail.
segundo_penultimo([A,B], X, Y) :- X is B, Y is A, !.
segundo_penultimo([_,A,_], X, Y) :- X is A, Y is A, !.
segundo_penultimo([_,A|L],X,Y) :- penultimo(L,Y), X is A, !.


/***************
* EJERCICIO 4. sublista/5
*
*       ENTRADA:
*		L: Lista de entrada de cadenas de texto.
*		Menor: Numero de valor entero, indice inferior.
*		Mayor: Numero de valor entero, indice superior.
*		E: Elemento, cadena de texto.
*       SALIDA:
*		Sublista: Sublista de salida de cadenas de texto.
*
****************/




/*contiene(L,A) :- !.*/
my_length([],0).
my_length([_|L],N) :- my_length(L,N1), N is N1 + 1.


contiene(L,Y) :- contiene([X|L], Y), Y=X, !.
contiene(L,Y) :- contiene([X|L], Y).
contiene([X|L],Y) :- contiene(L,Y) or X=Y

sublista([X|_],1,1,_,[X]).
sublista(_, Menor, Mayor, _, _) :- Menor>Mayor, print('ERROR 3.2 Indices.'), !, fail.
sublista(L, _, Mayor, N, _) :- N<Mayor,my_length(L,N), print('ERROR 3.3 Indices.'), !, fail.
sublista([X|L], 1, Mayor, E, [X|Sublista]) :- Mayor>1, Mayor1 is Mayor-1,
   sublista(L, 1, Mayor1, E, Sublista).
sublista([_|L], Menor, Mayor, E, Sublista) :- Menor>1, 
	Menor1 is Menor-1, Mayor1 is Mayor-1, sublista(L, Menor1, Mayor1, E, Sublista).

/***************
* EJERCICIO 5. espacio_lineal/4
*
*       ENTRADA:
*               Menor: Numero de valor entero, valor inferior del intervalo.
*               Mayor: Numero de valor entero, valor superior del intervalo.
*               Numero_elementos: Numero de valor entero, numero de valores de la rejilla.
*       SALIDA:
*               Rejilla: Vector de numeros de valor real resultante con la rejilla.
*
****************/
numElm(Menor, Mayor, Numero_elementos, Incremento) :-
   Incremento is (Mayor-Menor)/Numero_elementos, print(Incremento),!.
rejilla(Menor, 1, _, [Menor]) :- !.
rejilla(Menor, Numero_elementos, Incremento, [Menor|Rejilla]) :-
   rejilla(Menor1, Numero_elementos1, Incremento, Rejilla),
   Menor1 is Menor+Incremento, Numero_elementos1 is Numero_elementos-1.
espacio_lineal(Menor, Mayor, _, _) :- Menor>Mayor, print('ERROR 5.1 Indices.'), !, fail.
espacio_lineal(Menor, Mayor, Numero_elementos, Rejilla) :- 
   numElm(Menor, Mayor, Numero_elementos, Incremento),
   rejilla(Menor, Numero_elementos, Incremento, Rejilla).

/***************
* EJERCICIO 6. normalizar/2
*
*       ENTRADA:
*		Distribucion_sin_normalizar: Vector de numeros reales de entrada. Distribucion sin normalizar.
*       SALIDA:
*		Distribucion: Vector de numeros reales de salida. Distribucion normalizada.
*
****************/
sum([N|_],_) :- N<0, print('ERROR 5.1. Negativos'), !, fail.
sum([],0) :- !.
sum([A|L],Norma) :- sum(L,Sum), Norma is Sum+A.
dividir([A|[]],N,[B|[]]) :- B is A/N, !.
dividir([A|L],N,[B|Resultado]) :- dividir(L,N,Resultado), B is A/N.
normalizar(Distribucion_sin_normalizar, Distribucion) :- sum(Distribucion_sin_normalizar, Norma),
dividir(Distribucion_sin_normalizar, Norma, Distribucion). /* ¿Hace falta acabar con una exclamacion? */

/***************
* EJERCICIO 7. divergencia_kl/3
*
*       ENTRADA:
*		D1: Vector de numeros de valor real. Distribucion.
*		D2: Vector de numeros de valor real. Distribucion.
*       SALIDA:
*		KL: Numero de valor real. Divergencia KL.
*
****************/
distribucion(L) :- sum(L,1.0), print(L).
calculo_kl([],[_|_],_) :- print('ERROR 6.3. Listas de distinto tamaño'), !, fail.
calculo_kl([_|_],[],_) :- print('ERROR 6.3. Listas de distinto tamaño'), !, fail.
calculo_kl([], [], 0.0).
calculo_kl([0.0|_], [_|_], _) :- print('ERROR 6.1. Divergencia KL no definida.'), !, fail.
calculo_kl([_|_], [0.0|_], _) :- print('ERROR 6.1. Divergencia KL no definida.'), !, fail.
calculo_kl([X|LX], [Y|LY], KL) :- calculo_kl(LX, LY, K), KL is K+(X*log(X/Y)).
divergencia_kl(LX, LY, KL) :- calculo_kl(LX, LY, KL), distribucion(LX), distribucion(LY). /* ¿Hace falta acabar con una exclamacion? */
/***************************************************************************
Falta añadir el control de errores de si no es una distribucion
***************************************************************************/

/***************
* EJERCICIO 8. producto_kronecker/3
*
*       ENTRADA:
*		Matriz_A: Matriz de numeros de valor real.
*		Matriz_B: Matriz de numeros de valor real.
*       SALIDA:
*		Matriz_bloques: Matriz de bloques (matriz de matrices) de numeros reales.
*
****************/
producto_kronecker(Matriz_A, Matriz_B, Matriz_bloques) :- print('Error. Este ejercicio no esta implementado todavia.'), !, fail.

/***************
* EJERCICIO 9a. distancia_euclidea/3
*
*       ENTRADA:
*               X1: Vector de numeros de valor real. 
*               X2: Vector de numeros de valor real.
*       SALIDA:
*               D: Numero de valor real. Distancia euclidea.
*
****************/
distancia_euclidea(X1, X2, D) :- print('Error. Este ejercicio no esta implementado todavia.'), !, fail.

/***************
* EJERCICIO 9b. calcular_distancias/3
*
*       ENTRADA:
*               X_entrenamiento: Matriz de numeros de valor real donde cada fila es una instancia representada por un vector.
*               X_test: Matriz de numeros de valor real donde cada fila es una instancia representada por un vector. Instancias sin etiquetar.
*       SALIDA:
*               Matriz_resultados: Matriz de numeros de valor real donde cada fila es un vector con la distancia de un punto de test al conjunto de entrenamiento X_entrenamiento.
*
****************/
calcular_distancias(X_entrenamiento, X_test, Matriz_resultados) :- print('Error. Este ejercicio no esta implementado todavia.'), !, fail.

/***************
* EJERCICIO 9c. predecir_etiquetas/4
*
*       ENTRADA:
*               Y_entrenamiento: Vector de valores alfanumericos de una distribucion categorica. Cada etiqueta corresponde a una instancia de X_entrenamiento.
*               K: Numero de valor entero.
*               Matriz_resultados: Matriz de numeros de valor real donde cada fila es un vector con la distancia de un punto de test al conjunto de entrenamiento X_entrenamiento.
*       SALIDA:
*               Y_test: Vector de valores alfanumericos de una distribucion categorica. Cada etiqueta corresponde a una instancia de X_test.
*
****************/
predecir_etiquetas(Y_entrenamiento, K, Matriz_resultados, Y_test) :- print('Error. Este ejercicio no esta implementado todavia.'), !, fail.

/***************
* EJERCICIO 9d. predecir_etiqueta/4
*
*       ENTRADA:
*               Y_entrenamiento: Vector de valores alfanumericos de una distribucion categorica. Cada etiqueta corresponde a una instancia de X_entrenamiento.
*               K: Numero de valor entero.
*               Vec_distancias: Vector de valores reales correspondiente a una fila de Matriz_resultados.
*       SALIDA:
*               Etiqueta: Elemento de valor alfanumerico.
*
****************/
predecir_etiqueta(Y_entrenamiento, K, Vec_distancias, Etiqueta) :- print('Error. Este ejercicio no esta implementado todavia.'), !, fail.

/***************
* EJERCICIO 9e. calcular_K_etiquetas_mas_relevantes/4
*
*       ENTRADA:
*               Y_entrenamiento: Vector de valores alfanumericos de una distribucion categorica. Cada etiqueta corresponde a una instancia de X_entrenamiento.
*               K: Numero de valor entero.
*               Vec_distancias: Vector de valores reales correspondiente a una fila de Matriz_resultados.
*       SALIDA:
*		K_etiquetas: Vector de valores alfanumericos de una distribucion categorica.
*
****************/
calcular_K_etiquetas_mas_relevantes(Y_entrenamiento, K, Vec_distancias, K_etiquetas) :- print('Error. Este ejercicio no esta implementado todavia.'), !, fail.

/***************
* EJERCICIO 9f. calcular_etiqueta_mas_relevante/2
*
*       ENTRADA:
*               K_etiquetas: Vector de valores alfanumericos de una distribucion categorica.
*       SALIDA:
*               Etiqueta: Elemento de valor alfanumerico.
*
****************/
calcular_etiqueta_mas_relevante(K_etiquetas, Etiqueta) :- print('Error. Este ejercicio no esta implementado todavia.'), !, fail.

/***************
* EJERCICIO 9g. k_vecinos_proximos/5
*
*       ENTRADA:
*		X_entrenamiento: Matriz de numeros de valor real donde cada fila es una instancia representada por un vector.
*		Y_entrenamiento: Vector de valores alfanumericos de una distribucion categorica. Cada etiqueta corresponde a una instancia de X_entrenamiento.
*		K: Numero de valor entero.
*		X_test: Matriz de numeros de valor real donde cada fila es una instancia representada por un vector. Instancias sin etiquetar.
*       SALIDA:
*		Y_test: Vector de valores alfanumericos de una distribucion categorica. Cada etiqueta corresponde a una instancia de X_test.
*
****************/
k_vecinos_proximos(X_entrenamiento, Y_entrenamiento, K, X_test, Y_test) :- print('Error. Este ejercicio no esta implementado todavia.'), !, fail.

/***************
* EJERCICIO 9h. clasifica_patrones/4
*
*       ENTRADA:
*		iris_patrones.csv: Fichero con los patrones a clasificar, disponible en Moodle.
*		iris_etiquetas.csv: Fichero con las etiquetas de los patrones a clasificar, disponible en Moodle.
*		K: Numero de valor entero.
*       SALIDA:
*		tasa_aciertos: Tasa de acierto promediada sobre las iteraciones leave-one-out
*
****************/
clasifica_patrones('iris_patrones.csv','iris_etiquetas.csv',K,tasa_aciertos) :- print('Error. Este ejercicio no esta implementado todavia.'), !, fail.
