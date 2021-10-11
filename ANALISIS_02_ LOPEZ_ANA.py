"""
Created on Sat Oct  9 13:04:41 2021

@author: Ana Yomira López Hernández
"""

#Importamos libreria para leer CSV
import csv

#Hacemos una lista de datos vacía para poder importar todos los datos del CSV
lista_datos = []

#Llamamos al archivo con la funcio With en modo lectur ("r")
with open("synergy_logistics_database.csv", "r") as archivo:
    lector = csv.DictReader(archivo)

#Ciclo for para poder concatenar los datos     
    for registro in lector:
        lista_datos.append(registro)

        
#Se realiza el código para poder obtener las 10 rutas más demandadas        
'''############### OPCION 1: 10 RUTAS MAS DEMANDADAS ###############'''

#Se define una función que será un contador de las rutas según sean exportadas o importadas
#Primera opción para resolver éste enfoque de análisis

def rutas_exportacion_importacion (direccion): #La direccion debe ser "Exports" o "Imports"
    contador = 0 
    rutas_contadas = []
    rutas_conteo = []

#Ciclo for para llamar a cada elemento de la lista creada con todos los datos y poder 
# llamar a una lista nueva los valores de  origen a destino (paises)    
    for ruta in lista_datos:
        if ruta["direction"] == direccion:
            ruta_actual = [ruta["origin"], ruta["destination"]]

#En esta parte del código vamos contando las veces que una ruta se repite considerando 
#ambas variables destino y origen            
            if ruta_actual not in rutas_contadas:
                for ruta_data in lista_datos:
                    if ruta_actual == [ruta_data["origin"], ruta_data["destination"]]:
                        contador += 1
                        
#Se crea una nueva lista que vaya uniendo todos los  datos de las rutas encontradas con sus totales
                rutas_contadas.append(ruta_actual)
                rutas_conteo.append([contador, ruta["origin"], ruta["destination"]])    
                contador = 0
            
#Se acomodan por medio de la función Soart de mayor a menor.
    rutas_conteo.sort(reverse = True, key = lambda x:x[0])
    return rutas_conteo

#En caso de querer visualizar la información por direccion se imprimen se asignan variables en ambas opciones
conteo_exportaciones = rutas_exportacion_importacion ("Exports")
conteo_importaciones = rutas_exportacion_importacion ("Imports")

#print(conteo_exportaciones)
#print(conteo_importaciones)


#Esta es una segunda opción para analizar la información sobre las rutas, basada en la direccion,
# pero enfocada en el valor que cada ruta genera

def valor_movimiento(direccion):  #La direccion debe ser "Exports" o "Imports"
    contados = []
    valores_paises = []

#Se llama a cada elemento de la lista de datos y se utiliza la llave origin, para clasificar     
    for transaccion in lista_datos:
        actual = [direccion, transaccion["origin"]]
        valor = 0
        operaciones = 0

#Se utiliza un ciclo for para ir recolectando los datos y sumando su valor total para las rutas
#que van en la misma dirección        
        if actual in contados:
            continue
        for movimiento in lista_datos:
            if actual == [movimiento["direction"], movimiento["origin"]]:
                valor += int(movimiento["total_value"])
                operaciones += 1

#Se hace una lista nueva que da los valores de los países concatenados por ruta                 
        contados.append(actual)
        valores_paises.append([direccion,transaccion["origin"],valor,operaciones])

#Mediante la funcion soarted, utilizando un límite de parámetros, aquí solo seleccionamos el top 10 
#De las rutas más importantes dependiendo su direccion y enfocado en su valor
    sorted(valores_paises, key = lambda x: max(x[3:]), reverse = True)
    return valores_paises[:10]




'''############### OPCION 2: LOS 3 MEDIOS DE TRANSPORTE MÀS UTILIZADOS Y CUÁL REDUCIR ###############'''
#Se crea una función que basada en la dirección, obtendrá los totales por valor de los medios de transporte utilizados
# que son #Sea #Air #Rail #Road
def transporte_utilizado (direccion) : #"Exports" o "Imports"

    contados = []
    valores_transporte = []

#Creamos un contador que considera la llave de medio de transoporte "transport_mode" para cada
#elemnto de la lista de datos    
    for transaccion in lista_datos:
        actual = [direccion, transaccion["transport_mode"]]
        valor = 0
        operaciones = 0

#Aplicamos un ciclo for que va a comparar la direccion y el tipo de transporte, para concatenar
# y sumar los valores de cada transacción (o movimiento)        
        if actual in contados:
            continue
        for movimiento in lista_datos:
            if actual == [movimiento["direction"], movimiento["transport_mode"]]:
                valor += int(movimiento["total_value"])
                operaciones += 1
                
#Se crera una nueva lista que irá concatenando y arrojando los valores totales del valor por medio de transporte,
# relacionado a la dirección

        contados.append(actual)
        valores_transporte.append([transaccion["transport_mode"],direccion,valor,operaciones])

#Utilizamos la función sorted para acomodar de mayor a menor los valores de las transacciones por medio de trasnporte
    sorted(valores_transporte, key = lambda x: max(x[2:]), reverse = True)
    return valores_transporte[:4]

#valores_transporte =  transporte_utilizado ("Imports")
#print(valores_transporte)





'''############### OPCION 3: ENFOQUE EN LAS TRANSACCIONES QUE LE GENERAN EL 80% ###############'''

#Definimos una función que permita calcular el porcentaje que representa el valor de cada país, considerando aquellos
#que representen el porcentaje que determinemos a conocer del total de la operación

def porcentaje_pais(lista_paises, porcentaje): #lista de países con su valor por transacción, porcentaje meta
    valor_total = 0
    
#Utilizamos un ciclo for para que crear un contador por cada país de origen basado en la dirección

    for pais in lista_paises:
        valor_total += pais[2]
    paises = []
    porcentajes_calculados = []


 #Se crea un ciclo for para poder hacer la operación matemática para cada operación basado en su valor / el valor total de la operación
 #Se hace una lista con esos valores calculados y el porcentaje actual que cada uno representa

    for pais in lista_paises:
        porcentaje_actual = round(pais[2]/valor_total,3)
        porcentajes_calculados.append(porcentaje_actual)
        paises.append(pais)
        porcentajes_calculados.append(porcentaje_actual)
        
#Se concatenan aquellos valores no repetidos en la lista
        if porcentaje_actual == porcentajes_calculados[-1]:
            pais.append(porcentajes_calculados[-1])
#Si se supera la condición, ya no se incluye en la lista
        else:
            paises.pop(-1)
            porcentajes_calculados.pop(-1)
            break
#Se ordena la lista de mayor a menor, para así seguir con el flujo e ir sumando de las transacciones que generan más % de valor
# a las que menos
    valores_paises.sort(reverse = True, key = lambda x:x[2])        
    return paises


#paises_80  = porcentaje_pais(valor_movimiento("Imports"),.80)

#Definimos una útlima función, la cual nos permitirá basado en la lista obtenida de porcentajes de valores individuales actuales,
#concatenar hasta que la suma de los porcentajes calculados sea menor a porcentaje meta asignado considerando el últinmo valor
#de la lista para comparar
def top_paises_porcentaje (lista_paises, porcentaje): #La lista obtenida de porcentajes de valores individuales por país actuales, porcentaje meta


    top_80 = []
    porcentaje_acumulado = 0
    
    
 # Hacemos un ciclo for para ir sumando los totales hasta obtener un valor menor o igual al porcentaje asignado   
    for pais in lista_paises:
        porcentaje_acumulado += pais[4]

        if porcentaje_acumulado <= porcentaje:
            top_80.append(pais)
            #print(porcentaje_acumulado) #EPara imprimir el total acumulado
#Imprimimos los valores que corresponden a cada país de la lista de países que conforman el total del porcentaje asignado de la operación
    for pais in top_80:
      print(pais[4],pais[1])
      
     
      
#top_paises_80 = top_paises_porcentaje(paises_80,.8)

'''#A continueación se hace un menú que permite correr cada uno de los códigos dependiendo el enfoque que se
#quiera utilizar para analizar la información:'''
exp_imp = 0
ans = True
while ans:
    print(''' ESTOS SON LOS ENFOQUES DE ANÁLISIS DE INFORMACIÓN:
    1. 10 RUTAS MAS DEMANDADAS
    2. LOS 3 MEDIOS DE TRANSPORTE MÀS UTILIZADOS Y CUÁL REDUCIR
    3. ENFOQUE EN LAS TRANSACCIONES QUE LE GENERAN EL 80%
      ''') 
    ans=input("¿Qué análisis deseas hacer?: ")
    
    if ans == "1":
        print("Seleccionaste conocer 'Las 10 Rutas más demandadas'")
        exp_imp= input ("¿Deseas conocer los valores de importaciones o exportaciones?:  ")
        if exp_imp == "exportaciones":
            valores_paises =  valor_movimiento ("Exports")
            print('''Este es el top 10 de los países con mayores exportaciones''',valores_paises)
        elif exp_imp == "importaciones":
            valores_paises =  valor_movimiento ("Imports")
            print('''Este es el top 10 de los países con mayores importaciones:'''
                  ,valores_paises)
        elif exp_imp != "exportaciones" and "importaciones":
            print("Valor incorrecto, vuelve a seleccionar un valor (importaciones/exportaciones)")
            break
        
    if ans == "2":
        print("Seleccionaste conocer 'Los 3 medios de transporte más utilizados'")
        exp_imp= input ("¿Deseas conocer los valores de importaciones o exportaciones?:  ")
        if exp_imp == "exportaciones":
            valores_transporte =  transporte_utilizado ("Exports")
            print('''Este es el top 3 de medios de transporte utilizados para las exportaciones:  ''' ,valores_transporte)
            print("El medio de transporte: ",valores_transporte[-1], "Podría ser reducido")
        elif exp_imp == "importaciones":
            valores_transporte =  transporte_utilizado ("Imports")
            print(('''Este es el top 3 de medios de transporte utilizados para las importaciones:  ''' ,valores_transporte))
            print("El medio de transporte: ",valores_transporte[-1], "Podría ser reducido")
        elif exp_imp != "exportaciones" and "importaciones":
            print("Valor incorrecto, vuelve a seleccionar un valor (importaciones/exportaciones)")
    
    if ans == "3":
        print("Seleccionaste conocer 'Las rutas que equivalen al 80% del valor'")
        exp_imp= input ("¿Deseas conocer los valores de importaciones o exportaciones?:  ")
        if exp_imp == "exportaciones":
            valores_paises =  valor_movimiento ("Exports")
            paises_80  = porcentaje_pais(valor_movimiento("Exports"),.80)
            print('''Estos son los países que representan el 80% del valor de las operaciones de exportación:  ''')
            top_paises_80 = top_paises_porcentaje(paises_80,.80)
            print('''Su total es:  ''')
        elif exp_imp == "importaciones":
            valores_paises =  valor_movimiento ("Imports")
            paises_80  = porcentaje_pais(valor_movimiento("Imports"),.80)
            print('''Estos son los países que representan el 80% del valor de las operaciones de importación:  ''')
            top_paises_80 = top_paises_porcentaje(paises_80,.80)
        elif exp_imp != "exportaciones" and "importaciones":
            print("Valor incorrecto, vuelve a seleccionar un valor (importaciones/exportaciones)")    
    else:
        print("Favor de ingresar un valor de la lista (1,2,3)")
        
   
    


