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
my_length([],0).
my_length([_|L],N) :- my_length(L,N1), N is N1 + 1.

sliceList([X|_],1,1,[X]) :- !.
sliceList(_, Menor, Mayor,  _) :- Menor>Mayor, print('ERROR 3.2 Indices.'), !, fail.
sliceList(L, N, Mayor, _) :- N<Mayor, my_length(L,N), print('ERROR 3.3 Longitud de lista.'), !, fail.

sliceList([X|L], 1, Mayor, [X|Sublista]) :- Mayor>1, Mayor1 is Mayor-1,
   sliceList(L, 1, Mayor1, Sublista).
sliceList([_|L], Menor, Mayor, Sublista) :- Menor>1, 
	Menor1 is Menor-1, Mayor1 is Mayor-1, sliceList(L, Menor1, Mayor1, Sublista).

contiene([],_) :- print('ERROR 3.1 Elemento.'), !, fail.
contiene([X|_],Y) :-  Y=X, !.
contiene([_|L],Y) :- contiene(L, Y).

sublista(Lista,Menor,Mayor,E,Sublista) :- sliceList(Lista, Menor, Mayor, Sublista), contiene(Sublista,E), !.

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
   Incremento is (Mayor-Menor)/(Numero_elementos-1), !.
rejilla(Menor, 1, _, [Menor]) :- !.
rejilla(Menor, Numero_elementos, Incremento, [Menor|Rejilla]) :-
   Numero_elementos1 is Numero_elementos-1, Menor1 is Menor+Incremento, rejilla(Menor1, Numero_elementos1, Incremento, Rejilla).
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
distribucion(L) :- sum(L,1.0).
calculo_kl([],[_|_],_) :- print('ERROR 6.3. Listas de distinto tamaño'), !, fail.
calculo_kl([_|_],[],_) :- print('ERROR 6.3. Listas de distinto tamaño'), !, fail.
calculo_kl([], [], 0.0).
calculo_kl([0.0|_], [_|_], _) :- print('ERROR 6.1. Divergencia KL no definida.'), !, fail.
calculo_kl([_|_], [0.0|_], _) :- print('ERROR 6.1. Divergencia KL no definida.'), !, fail.
calculo_kl([X|LX], [Y|LY], KL) :- calculo_kl(LX, LY, K), KL is K+(X*log(X/Y)).
divergencia_kl(LX, _, _) :- normalizar(LX,DNX), LX \== DNX, print('ERROR 6.2. Divergencia KL definida solo para distribuciones'), !, fail.
divergencia_kl(_, LY, _) :- normalizar(LY,DNY), LY \== DNY, print('ERROR 6.2. Divergencia KL definida solo para distribuciones'), !, fail.
divergencia_kl(LX, LY, KL) :- calculo_kl(LX, LY, KL).

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
% Calcula el producto de un número fila de la matriz
producto_fila([X],Y, [S]) :- S is X*Y, S<0, print('ERROR 8.1. Elemento menor que cero.'), !, fail.
producto_fila([X],Y, [S]) :- S is X*Y, !.
producto_fila([A|L],Y, [B|R]) :- producto_fila(L,Y,R), B is A*Y.

% Calcula el producto de un número por una matriz
producto_matriz([X],Y, [S]) :- producto_fila(X,Y,S), !.
producto_matriz([A|L],Y, [B|R]) :- producto_matriz(L,Y,R), producto_fila(A,Y,B).

%producto_kronecker([[3,4]], [[0,5], [6,7]], R).
producto_kronecker([[X]],Y, [[S]]) :- producto_matriz(Y,X,S), !.
producto_kronecker([[A|L]],Y, [[B|R]]) :- producto_kronecker([L],Y,[R]), producto_matriz(Y,A,B), !.
producto_kronecker([A|L],Y, [B|R]) :- 
    producto_kronecker(L,Y,R), producto_kronecker([A],Y,[B]), !.

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
distancia_euclidea(X1, X2, D) :- suma_cuadratica(X1, X2, Res), D is sqrt(Res), !.
suma_cuadratica([], [], 0).
suma_cuadratica([X1|L1], [X2|L2], D) :- suma_cuadratica(L1, L2, Res), D is Res + (X1-X2)**2.

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
distanciasFila([],_,[]).
distanciasFila([Punto|M_entrenamiento], X_test, [Res|Fila_Resultados]) :- 
   distanciasFila(M_entrenamiento, X_test, Fila_Resultados), distancia_euclidea(Punto,X_test,Res).
calcular_distancias(_,[],[]).
calcular_distancias(M_entrenamiento, [X_test|M_test], [Fila_Resultados|Matriz_resultados]) :- 
   calcular_distancias(M_entrenamiento, M_test, Matriz_resultados), 
   distanciasFila(M_entrenamiento, X_test, Fila_Resultados), !.

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
predecir_etiquetas(_, _, [], []).
predecir_etiquetas(Y_entrenamiento, K, [X|Matriz_resultados], [Etiqueta|Etiquetas]) :- 
   predecir_etiquetas(Y_entrenamiento, K, Matriz_resultados, Etiquetas), 
   predecir_etiqueta(Y_entrenamiento, K, X, Etiqueta).

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
predecir_etiqueta(Y_entrenamiento, K, Vec_distancias, Etiqueta) :- 
   calcular_K_etiquetas_mas_relevantes(Y_entrenamiento, K, Vec_distancias, K_etiquetas),
   calcular_etiqueta_mas_relevante(K_etiquetas, Etiqueta).


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
calcular_tuplas([],[],[]).
calcular_tuplas([Y|Y_entrenamiento], [D|Vec_distancias], [[D|Y]|Tuplas]) :- 
   calcular_tuplas(Y_entrenamiento, Vec_distancias, Tuplas).

cortarKEtiquetas(_, 0, []).
cortarKEtiquetas([[_|Etiqueta]|TuplasOrdenadas], K, [Etiqueta|K1_etiquetas]) :- 
   K1 is K-1, cortarKEtiquetas(TuplasOrdenadas, K1, K1_etiquetas).

calcular_K_etiquetas_mas_relevantes(Y_entrenamiento, K, Vec_distancias, K_etiquetas) :- 
   calcular_tuplas(Y_entrenamiento, Vec_distancias, Tuplas), msort(Tuplas, TuplasOrdenadas),
   cortarKEtiquetas(TuplasOrdenadas, K, K_etiquetas), !.


/***************
* EJERCICIO 9f. calcular_etiqueta_mas_relevante/2
*
*       ENTRADA:
*               K_etiquetas: Vector de valores alfanumericos de una distribucion categorica.
*       SALIDA:
*               Etiqueta: Elemento de valor alfanumerico.
*
****************/
% pack(L1,L2) :- the list L2 is obtained from the list L1 by packing
%    repeated occurrences of elements into separate sublists.
%    (list,list) (+,?)
pack([],[]).
pack([X|Xs],[Z|Zs]) :- transfer(X,Xs,Ys,Z), pack(Ys,Zs).

% transfer(X,Xs,Ys,Z) Ys is the list that remains from the list Xs
%    when all leading copies of X are removed and transfered to Z
transfer(X,[],[],[X]).
transfer(X,[Y|Ys],[Y|Ys],[X]) :- X \= Y.
transfer(X,[X|Xs],Ys,[X|Zs]) :- transfer(X,Xs,Ys,Zs).

% encode(L1,L2) :- the list L2 is obtained from the list L1 by run-length
%    encoding. Consecutive duplicates of elements are encoded as terms [N,E],
%    where N is the number of duplicates of the element E.
%    (list,list) (+,?)
encode(L1,L2) :- pack(L1,L), transform(L,L2).

transform([],[]).
transform([[X|Xs]|Ys],[[N,X]|Zs]) :- length([X|Xs],N), transform(Ys,Zs).

calcular_contadores(L, Res) :- msort(L, Sorted), encode(Sorted, Res).

masFrec([X|_],[Y|_]) :- X>Y.
menIgFrec([X|_],[Y|_]) :- X=<Y.
maximo_etiquetas([],[0,_]).
maximo_etiquetas([E|Etiquetas], Etiqueta) :- 
    maximo_etiquetas(Etiquetas, Etiqueta), menIgFrec(E,Etiqueta).
maximo_etiquetas([E|Etiquetas], E) :- 
    maximo_etiquetas(Etiquetas, Etiqueta), masFrec(E,Etiqueta).

calcular_etiqueta_mas_relevante(K_etiquetas, Etiqueta) :- 
   calcular_contadores(K_etiquetas, Etiquetas), 
   maximo_etiquetas(Etiquetas, [_,Etiqueta]), !.

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
k_vecinos_proximos(X_entrenamiento, Y_entrenamiento, K, X_test, Y_test) :- 
   calcular_distancias(X_entrenamiento, X_test, Matriz_Distancias),
   predecir_etiquetas(Y_entrenamiento, K, Matriz_Distancias, Y_test), !.


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
clasifica_patrones(Patrones,Etiquetas,K,Tasa_aciertos) :- 
   csv_read_file(Patrones, Rows1), csv_read_file(Etiquetas, Rows2),
   leave_one_out(Rows1, Rows2, K, Tasa_aciertos), !.

leave_one_out(Rows1, Rows2, K, Tasa_aciertos) :- 
   iterar(length(Rows1), Rows1, Rows2, K, Tasa_aciertos).

iterar(0, _, _, _, 0.0).
iterar(N, Rows1, Rows2, K, Tasa_aciertos+Tasa_acierto/length(Rows1)) :- 
   N1 is N-1, iterar(N1, Rows1, Rows2, K, Tasa_aciertos), 
   tasa_acierto(N1, Rows1, Rows2, K, Tasa_acierto).

tasa_acierto(N, Rows1, Rows2, K, 0.0) :- 
   remove_at(X, Rows1, N, K_vecinos), remove_at(Real, Rows2, N, K_etiquetas),
   k_vecinos_proximos(K_vecinos, K_etiquetas, K, X, Prediccion), Prediccion\=Real.
tasa_acierto(N, Rows1, Rows2, K, 1.0) :- 
   remove_at(X, Rows1, N, K_vecinos), remove_at(Real, Rows2, N, K_etiquetas),
   k_vecinos_proximos(K_vecinos, K_etiquetas, K, X, Prediccion), Prediccion=Real.


% The first element in the list is number 1.
% remove_at(X,L,K,R) :- X is the K'th element of the list L; R is the
%    list that remains when the K'th element is removed from L.
%    (element,list,integer,list) (?,?,+,?)
remove_at(X,[X|Xs],1,Xs).
remove_at(X,[Y|Xs],K,[Y|Ys]) :- K > 1, 
   K1 is K - 1, remove_at(X,Xs,K1,Ys).
