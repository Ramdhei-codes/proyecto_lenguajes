gramatica = {
    "E": ["E + T", "T"],
    "T": ["T * F", "F"],
    "F": ["id", "( E )"]
}

gramatica1 = [
    {"E": ["E + T", "T"]},
    {"T": ["T * F", "F"]},
    {"F": ["id", "( E )"]}
]

gramatica2 = [
    {"S": ["S xx", "A B C D"]},
    {"A": ["p", "&", "B D", "A p B"]},
    {"B": ["q C H", "q B H", "&"]},
    {"H": ["xyxx"]},
    {"D": ["d", "&"]},
    {"C": ["idd S fx", "id"]}
]

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

def lista_no_terminales(gramatica):
    lista_nt = []
    for produccion in gramatica:
        for key, value in produccion.items():
            lista_nt.append(key)

    return lista_nt

            

def buscar_produccion(nombre_produccion, gramatica):
    elementos_produccion = []
    for prod in gramatica:
        if list(prod.keys())[0] == nombre_produccion:
            for value in list(prod.values())[0]:
                elementos_produccion.append(value)
    return elementos_produccion
            



def main():
    eliminar_recursion(gramatica2)
    # imprimir_gramatica(gramatica1)
    print("-"*50)
    primeros(gramatica2)
    print("-"*50)

    sig_gram = siguientes(gramatica2)
    imprimir_gramatica(sig_gram)
    # print(lista_no_terminales(gramatica1))
    

main()

