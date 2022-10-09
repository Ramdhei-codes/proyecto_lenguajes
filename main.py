import json
from tabulate import tabulate

gramatica_json = open("gramatica.json")

gramatica2_json = open("gramatica2.json")

gramatica_1 = json.load(gramatica_json)
gramatica_2 = json.load(gramatica2_json)

def eliminar_recursion(gramatica):
    for prod in gramatica:
        alfas = []
        betas = []
        for key , value in prod.items():
            for j in value:
                if j[0] == key:
                    for char in value:
                        if char[0] == key:
                            alfas.append(char[1:])
                        else:
                            betas.append(char)
                   
                    nombre_nueva_prod = f"{key}p"
                    prod[key] = []
                    elementos_nueva_prod = []
                    
                    for beta in betas:
                        prod[key].append(f"{beta.strip()} {nombre_nueva_prod}")
                    for alfa in alfas:
                        elementos_nueva_prod.append(f"{alfa.strip()} {nombre_nueva_prod}")
                    elementos_nueva_prod.append("&")
                    gramatica.append({nombre_nueva_prod: elementos_nueva_prod})

def imprimir_gramatica(gramatica):
        for element in gramatica:
            for key, value in element.items():
                print(f"{key} -> {value}")

def primeros(gramatica):
    lista_primeros = []
    for element in gramatica:
        for key, value in element.items():
            primeros_prod_actual = []
            for i in value:
                characters = i.split(" ")
                valor_actual = characters[0]
                prod_actual = []
                if characters[0].islower() or not characters[0].isalnum():
                    if characters[0] not in primeros_prod_actual:
                        primeros_prod_actual.append(characters[0])
                else:
                    while valor_actual.isupper():
                        prod_actual = buscar_produccion(valor_actual, gramatica)
                        for value in prod_actual:
                            arr_value = value.split(" ")
                            if arr_value[0].islower() or not arr_value[0].isalnum():
                                if arr_value[0] not in primeros_prod_actual:
                                    primeros_prod_actual.append(arr_value[0])
                            valor_actual = arr_value[0]              
            lista_primeros.append({key: primeros_prod_actual})
    return lista_primeros

def siguientes(gramatica:list):
    lista_primeros = primeros(gramatica)
    lista_siguientes = []
    lista_nt = lista_no_terminales(gramatica)

    indice_produccion_actual = 0

    while indice_produccion_actual < len(gramatica):
        nt_prod_actual = list(gramatica[indice_produccion_actual].keys())[0]
        siguientes_prod_actual = []
        for produccion in gramatica:
            for nt, derivados in produccion.items():
                for derivado in derivados:
                    arr_derivado = derivado.split(" ")
                    if nt_prod_actual in arr_derivado:
                        indice_nt_actual = arr_derivado.index(nt_prod_actual)

                        if indice_produccion_actual == 0:
                            siguientes_prod_actual.append("$")

                        if not indice_nt_actual == len(arr_derivado)-1:
                        
                            if arr_derivado[indice_nt_actual+1].islower() or not arr_derivado[indice_nt_actual+1].isalnum():

                                if arr_derivado[indice_nt_actual+1] not in siguientes_prod_actual:
                                    siguientes_prod_actual.append(arr_derivado[indice_nt_actual+1])
                            else:
                                lista_primeros_del_siguiente = buscar_produccion(arr_derivado[indice_nt_actual+1], lista_primeros)
                                if "&" in lista_primeros_del_siguiente:
                                    lista_primeros_del_siguiente.remove("&")
                                    siguientes_raiz = buscar_produccion(nt, lista_siguientes)
                                    for siguiente in siguientes_raiz:
                                        if siguiente not in lista_primeros_del_siguiente:
                                            lista_primeros_del_siguiente.append(siguiente)
                                for sig in lista_primeros_del_siguiente:
                                    if sig not in siguientes_prod_actual:
                                        siguientes_prod_actual.append(sig)
                        else:
                            siguientes_raiz_l = buscar_produccion(nt, lista_siguientes)
                            for sig in siguientes_raiz_l:
                                if sig not in siguientes_prod_actual:
                                    siguientes_prod_actual.append(sig)
                        
        lista_siguientes.append({nt_prod_actual: siguientes_prod_actual})
        indice_produccion_actual+=1
            
            
    return lista_siguientes

def conjunto_prediccion(gramatica, imprimir_tabla=0):
    lista_primeros = primeros(gramatica)
    lista_siguientes = siguientes(gramatica)

    lista_t = lista_terminales(gramatica)

    conjunto_pred = []
    valores_tabla_conjunto_pred = []

    for produccion in gramatica:
        conjunto_prediccion_prod_actual = []
        lista_tabla_prod_actual = [list(produccion.keys())[0]]

        for key, value in produccion.items():

            for i in range(len(lista_t)):
                lista_tabla_prod_actual.append(" ")

            for derivado in value:

                arr_value = derivado.split(" ")

                if arr_value[0] == "&":
                    siguientes_esta_prod = buscar_produccion(key, lista_siguientes)
                    conjunto_prediccion_prod_actual.extend(siguientes_esta_prod)
                    llenar_fila_tabla(lista_tabla_prod_actual, siguientes_esta_prod, derivado, lista_t)
                elif arr_value[0].islower() or not arr_value[0].isalnum():
                    conjunto_prediccion_prod_actual.append(arr_value[0])
                    llenar_fila_tabla(lista_tabla_prod_actual, [arr_value[0]], derivado, lista_t)
                else:
                    primeros_esta_prod = buscar_produccion(arr_value[0], lista_primeros)
                    conjunto_prediccion_prod_actual.extend(primeros_esta_prod)
                    llenar_fila_tabla(lista_tabla_prod_actual, primeros_esta_prod, derivado, lista_t)
        valores_tabla_conjunto_pred.append(lista_tabla_prod_actual)
        conjunto_pred.append({key: conjunto_prediccion_prod_actual})

    if imprimir_tabla == 1:
        tabla_analisis_sintactico(lista_t, valores_tabla_conjunto_pred)
    return conjunto_pred

def tabla_analisis_sintactico(encabezados, valores):
    encabezados.insert(0, "NT/VT")
    print(tabulate(valores, headers=encabezados, tablefmt="pretty"))


def llenar_fila_tabla(lista_tabla_prod, terminales_a_anadir, valor, lista_terminales):
    
    for terminal in lista_terminales:
        for t in terminales_a_anadir:
            if t == terminal:
                lista_tabla_prod[lista_terminales.index(terminal)+1] = valor

    


def esLL1(conjunto_prediccion):
    for produccion in conjunto_prediccion:
        for key, value in produccion.items():
            prod_sin_repetidos = set(value)

            repetidos_ll1 = len(value) != len(prod_sin_repetidos)

            if repetidos_ll1:
                break
        
        if repetidos_ll1:
            break

    if repetidos_ll1:
        print("--"*30)
        print("NO ES UNA GRAMÁTICA LL1")
        print("--"*30)
    else:
        print("--"*30)
        print("ES UNA GRAMÁTICA LL1")
        print("--"*30)




def lista_no_terminales(gramatica):
    lista_nt = []
    for produccion in gramatica:
        for key, value in produccion.items():
            lista_nt.append(key)

    return lista_nt

def lista_terminales(gramatica):
    lista_t = ["$"]
    for produccion in gramatica:
        for key, value in produccion.items():
            for derivado in value:
                arr_derivado = derivado.split(" ")
                for el in arr_derivado:
                    if (el.islower() or not el.isalnum()) and el != "&":
                        lista_t.append(el)

    return lista_t

            

def buscar_produccion(nombre_produccion, gramatica):
    elementos_produccion = []
    for prod in gramatica:
        if list(prod.keys())[0] == nombre_produccion:
            for value in list(prod.values())[0]:
                elementos_produccion.append(value)
    return elementos_produccion


if __name__ == "__main__":
    eliminar_recursion(gramatica_1)
    imprimir_gramatica(gramatica_1)
    primeros(gramatica_1)
    sig_gram = siguientes(gramatica_1)
    esLL1(conjunto_prediccion(gramatica_1))

    conjunto_prediccion(gramatica_1,1)
