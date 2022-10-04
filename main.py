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
                
                if characters[0].islower() or not characters[0].isalnum():
                    primeros_prod_actual.append(characters[0])
            lista_primeros.append({key: primeros_prod_actual})
    print(lista_primeros)
            



def main():
    eliminar_recursion(gramatica1)
    primeros(gramatica1)
    # imprimir_gramatica(gramatica1)

main()

