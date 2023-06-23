import http.client
import json
import requests
import os
from PIL import Image
from passlib.hash import sha256_crypt
import matplotlib.pyplot as plt
import random
import datetime


def opcionesMenu() -> None:
    print("\n+-----+ Menú +-----+")
    print("1. Iniciar sesión")
    print("2. Registrarse")
    print("3. Salir\n")

def opciones() -> None:
    print("\nOpciones:")
    print("1. Mostrar el plantel completo de un equipo")
    print("2. Mostrar la tabla de posiciones de la Liga Profesional")
    print("3. Datos de un equipo")
    print("4. Gráfico de goles en función de minutos para un equipo")
    print("5. Cargar dinero")
    print("6. Usuario que más dinero apostó")
    print("7. Usuario que más veces ganó")
    print("8. Apuestas")
    print("9. Cerrar sesion\n")

def pedirOpcion(opciones: list) -> int:
    opcion = input("Elegir opción: ")
    while numero_invalido(opcion) or opcion not in opciones:
        opcion = input("\nPor favor, ingrese una opción válida: ")
    opcion = int(opcion)
    return opcion

def registrarse() -> None:
    #Esta funcion permite al usuario registrarse, guardando sus datos en el archivo "usuarios.csv"
    registrarIdUser = str(input("Mail: "))
    registrarIdUser = validarMail(registrarIdUser)
    registrarUsername = str(input("Usuario: "))
    registrarPassword = str(input("Contraseña: "))
    hashPassword = sha256_crypt.hash(registrarPassword)
    registrarCantidadApostada = 0
    registrarFechaUltimaApuesta = "No se ha realizado ninguna apuesta"
    registrarDineroDisponible = 0
    file = open("usuarios.csv", "a")
    file.write(f"{registrarIdUser},{registrarUsername},{hashPassword},{registrarCantidadApostada},{registrarFechaUltimaApuesta},{registrarDineroDisponible}\n")
    file.close()

def obtenerDatos(datos: list) -> list:
    #Toma ciertos datos contenidos en una lista, y los devuelve como un diccionario con una lista para cada usuario.
    lista = []
    datosTotales = {}
    for elemento in datos:
        lista.append(elemento.split(","))
    for elemento in lista:
        datosTotales[elemento[0]] = elemento
    return datosTotales

def numero_invalido(numero):
    try:
        float(numero)
        return False
    except ValueError:
        return True

def id_invalido(id_equipo):
    id_valido = ["434", "435","436","437","438","439","440", "441", "442", "443", "445", "446", "448","449", "450" , "451", "452", "453", "455", "456", "457", "458", "459","460", "474","478", "1024","1025", "2432"]
    while id_equipo not in id_valido or numero_invalido(id_equipo):
        id_equipo = input("ID inválida, por favor intente nuevamente: ")    
    id_equipo = int(id_equipo)
    return id_equipo

def validarMail(mail):
    while mail.endswith(".com") != True:
        mail = str(input("\nMail inválido, debe usar \"@\" y terminar con \".com\": "))
        mail.endswith(".com")
    mail = list(mail)
    while "@" not in mail:
        mail = str(input("\nMail inválido, debe usar \"@\" y terminar con \".com\": "))
        mail = list(mail)
    mail = "".join(mail)
    return mail

def obtener_plantel_equipo(equipo_id):
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")

    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "c58299203753a8108c210738ab6b68a5"
    }

    conn.request("GET", f"/players/squads?team={equipo_id}", headers=headers)

    res = conn.getresponse()
    data = res.read()

    data_decoded = data.decode("utf-8")

    with open("plantel_equipo.json", "w") as json_file:
        json_file.write(data_decoded)

def mostrar_plantel_equipo(equipo_id):
    with open("plantel_equipo.json", "r") as json_file:
        data_loaded = json.load(json_file)

    plantel_json = data_loaded["response"]

    if len(plantel_json) > 0:
        for plantel in plantel_json:
            nombreEquipo = plantel['team']['name']
            print(f"+-----+ Plantel del equipo {nombreEquipo} +-----+")
            print("\nNombre | Edad | Posición")
            for jugador in plantel['players']:
                nombreJugador = jugador['name']
                edadJugador = jugador['age']
                posicionJugador = jugador['position']
                print(f"{nombreJugador} | {edadJugador} | {posicionJugador}")
    os.remove("plantel_equipo.json") #Nota: elimina el archivo para no ocupar memoria

def imprimir_ids_equipos() -> None:
    equipos = {
        "Gimnasia L.P.": 434,
        "River Plate": 435,
        "Racing Club": 436,
        "Rosario Central": 437,
        "Velez Sarsfield": 438,
        "Godoy Cruz": 439,
        "Belgrano Cordoba": 440,
        "Union Santa Fe": 441,
        "Defensa Y Justicia": 442,
        "Huracan": 445,
        "Lanus": 446,
        "Colon Santa Fe": 448,
        "Banfield": 449,
        "Estudiantes L.P.": 450,
        "Boca Juniors": 451,
        "Tigre": 452,
        "Independiente": 453,
        "Atletico Tucuman": 455,
        "Talleres Cordoba": 456,
        "Newells Old Boys": 457,
        "Argentinos JRS": 458,
        "Arsenal Sarandi": 459,
        "San Lorenzo": 460,
        "Sarmiento Junin": 474,
        "Instituto Cordoba": 478,
        "Platense": 1064,
        "Central Cordoba de Santiago": 1065,
        "Barracas Central": 2432
    }

    print("\nA continuación se muestran los equipos y sus respectivas IDs:")

    for equipo, id_equipo in equipos.items():
        print(f"{equipo}: {id_equipo}")

def posiciones_temporada() -> None:
    lista_años = ["2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"]
    print(f"\nLas temporadas disponibles son: 2015, 2016, 2017, 2018, 2019, 2020, 2021 y 2022")
    año = input("Ingrese el año para ver la tabla de posiciones: ")
    print()

    while numero_invalido(año) or año not in lista_años:
        año = input("Año inválido, intente nuevamente: ")
        print()

    año = int(año)
    archivo = f"posicion {año}.json"

    with open(f"Tabla de posiciones/{archivo}", 'r') as json_file:
        data = json.load(json_file)

    standings = data['response'][0]['league']['standings']

    for ranking in standings:
        print(ranking[0]["group"])
        for position in ranking:
            rank = position['rank']
            team = position['team']['name']
            points = position['points']
            goals_diff = position['goalsDiff']
            print(f"{rank}. {team}, {points} Pts, ({goals_diff})")
        print()

def mostrarInfoEquipo(equipoId) -> None:
    with open("info equipos.json", "r") as json_file:
        data_loaded = json.load(json_file)
    info_json = data_loaded["response"]
    for info in info_json:
        if info['team']['id'] == equipoId:
            nombreEquipo = info['team']['name']
            codigoEquipo = info['team']['code']
            paisEquipo = info['team']['country']
            fundacionEquipo = info['team']['founded']
            logoEquipo = info['team']['logo']
            nombreEstadio = info['venue']['name']
            direccionEstadio = info['venue']['address']
            ciudadEstadio = info['venue']['city']
            capacidadEstadio = info['venue']['capacity']
            superficieEstadio = info['venue']['surface']
            imagenEstadio = info['venue']['image']
            print(f"+-----+ Información básica sobre el equipo {nombreEquipo} +-----+")
            print(f"Codigo: {codigoEquipo}\tPaís de origen: {paisEquipo}\tAño de fundación: {fundacionEquipo}")
            #Mostrar logoEquipo
            print("\nCargando imagen...")
            r = requests.get(logoEquipo) 
            with open(f'logoEquipo{nombreEquipo}.png', 'wb') as f: 
                f.write(r.content)
            imagen = Image.open(f'logoEquipo{nombreEquipo}.png')
            imagen.show()
            os.remove(f'logoEquipo{nombreEquipo}.png') #Nota: elimina la imagen para no ocupar memoria
            print("\n+-----+ Información sobre su estadio +-----+")
            print(f"Nombre: {nombreEstadio}\tDirección: {direccionEstadio}")
            print(f"Ciudad: {ciudadEstadio}\tCapacidad: {capacidadEstadio}\tSuperficie: {superficieEstadio}")
            #Mostrar imagenEstadio
            print("\nCargando imagen...")
            r = requests.get(imagenEstadio) 
            with open(f'imagenEstadio{nombreEquipo}.png', 'wb') as f: 
                f.write(r.content)
            imagen = Image.open(f'imagenEstadio{nombreEquipo}.png')
            imagen.show()
            os.remove(f'imagenEstadio{nombreEquipo}.png') #Nota: elimina la imagen para no ocupar memoria
            break
    else:
        print(f"\nNo se encontró información para el equipo con ID {equipoId}")

def mostrar_grafico():
    imprimir_ids_equipos()
    print()
    equipo_id = input("Ingrese el ID del equipo: ")
    equipo_id = id_invalido(equipo_id)
    
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "c58299203753a8108c210738ab6b68a5"
    }
    conn.request("GET", f"/teams/statistics?season=2023&team={equipo_id}&league=128", headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")

    with open(f"equipo_{equipo_id}.json", "w") as json_file:
        json_file.write(data)

    with open(f"equipo_{equipo_id}.json", "r") as json_file:
        data_json = json.load(json_file)

    equipo_nombre = data_json["response"]["team"]["name"]
    goles = []
    minutos = []

    for minute_range, minute_info in data_json["response"]["goals"]["for"]["minute"].items():
        if minute_info["total"] is not None:
            goles.append(minute_info["total"])
            minutos.append(minute_range)

    plt.plot(minutos, goles)
    plt.xlabel("Minutos jugados")
    plt.ylabel("Goles realizados")
    plt.title(f"Gráfico Goles vs. Minutos para {equipo_nombre}")
    plt.show()
    os.remove(f"equipo_{equipo_id}.json") #Nota: elimina el archivo para no ocupar memoria (tuve que eliminar el file_path para que no quede una carpeta vacía. Pero si querés lo vuelvo a agregar -hice una copia-)

def cargarDinero(idUser, datosTotales, monto) -> None:
    #Añade dinero a la cuenta del usuario
    for lista in datosTotales.values():
        if idUser == lista[0]:
            lista[5] = float(lista[5])
            lista[5] += monto
            print("Monto agregado con éxito!")
            os.remove("usuarios.csv")
            with open("usuarios.csv", "a") as file:
                for usuario in datosTotales.values():
                    for datos in usuario:
                        file.write(f"{datos},")
                    file.write("\n")

def apuestas(equipoId, idUser, datosTotales, montoDisponible):
    with open("fixtures.json", "r") as json_file:
        json_file = json.load(json_file)
    fixtures = []
    for elemento in json_file["response"]:
        if elemento["teams"]["home"]["id"] == equipoId or elemento["teams"]["away"]["id"] == equipoId:
            fixtures.append(elemento["fixture"]["id"])
    
    print("\nEliga una ID para ingresar al partido que desea apostar")
    for fixture in fixtures:
        for elemento in json_file["response"]:
            if fixture == elemento["fixture"]["id"]:
                print(f"\n+---+ ID: {fixture} +---+")
                print(f"Local: {elemento['teams']['home']['name']}\nVisitante: {elemento['teams']['away']['name']}")

    elegirId = input("\nElegir ID: ")
    while numero_invalido(elegirId) or int(elegirId) not in fixtures:
        elegirId = input("ID inválida, intente nuevamente: ")
    
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")

    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "3acf8ad408e18c67e1da7a3a32ea624b"
        }

    conn.request("GET", f"/predictions?fixture={elegirId}", headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")

    with open(f"fixture_{elegirId}.json", "w") as jsonFile:
        jsonFile.write(data)

    with open(f"fixture_{elegirId}.json", "r") as jsonFile:
        dataJson = json.load(jsonFile)

    posiblesResultados = ["Ganador(L)", "Empate", "Ganador(V)"]
    apostarResultado = input("\nIngrese el resultado esperado /Ganador(L)/Empate/Ganador(V)/: ")
    if apostarResultado not in posiblesResultados:
        apostarResultado = input("Resultado inválido, intente nuevamente /Ganador(L)/Empate/Ganador(V)/: ")

    apostarMonto = input("\nIngrese el monto que desea apostar: ")
    while numero_invalido(apostarMonto):
        apostarMonto = input("\nMonto inválido, intente nuevamente: ")
    apostarMonto = float(apostarMonto)
    if apostarMonto > montoDisponible:
        print("\nUsted no cuenta con ese dinero en su cuenta")
        return None

    dado = random.randint(1,3)
    if dado == 1:
        resultado = "Ganador(L)"
    elif dado == 2:
        resultado = "Empate"
    elif dado == 3:
        resultado = "Ganador(V)"

    win_or_draw = dataJson["response"][0]["predictions"]["win_or_draw"]

    n = random.randint(1,4)

    if resultado in ["Ganador(L)", "Ganador(V)"]:
        if apostarResultado == resultado and win_or_draw == True:
            paga = apostarMonto*n*0.1
            print(f"\n{resultado}!\nFelicitaciones!\nHa ganado: {paga}")
        elif apostarResultado == resultado and win_or_draw == False:
            paga = apostarMonto*n
            print(f"\n{resultado}!\nFelicitaciones!\nHa ganado: {paga}")
        elif apostarResultado != resultado and win_or_draw == True:
            paga = 0
            print(f"\nHa ganado: {resultado}\nSuerte para la próxima!")
        elif apostarResultado != resultado and win_or_draw == False:
            paga = 0
            print(f"\nHa ganado: {resultado}\nSuerte para la próxima!")
    else:
        if win_or_draw == True:
            paga = apostarMonto*n*0.05
            print(f"\n{resultado}!\nFelicitaciones!\nHa ganado: {paga}")
        elif win_or_draw == False:
            paga = apostarMonto*n
            print(f"\n{resultado}!\nFelicitaciones!\nHa ganado: {paga}")

    añoApuesta = datetime.datetime.now().year
    mesApuesta = datetime.datetime.now().month
    diaApuesta = datetime.datetime.now().day
    fechaApuesta = f"{añoApuesta}" + f"{mesApuesta}" + f"{diaApuesta}"
    for lista in datosTotales.values():
        if idUser == lista[0]:
            lista[5] = float(lista[5])
            lista[5] += paga
            lista[4] = fechaApuesta
            lista[3] = float(lista[3])
            lista[3] += apostarMonto
            os.remove("usuarios.csv")
            with open("usuarios.csv", "a") as file:
                for usuario in datosTotales.values():
                    for datos in usuario:
                        file.write(f"{datos},")
                    file.write("\n")
    os.remove(f"fixture_{elegirId}.json")

    #Crear el archivo transacciones.csv con los resultados

def main() -> None:
    opcionesMenu()
    opcionMenu = pedirOpcion(["1","2","3"])
    while opcionMenu != 3:
        if opcionMenu == 1:
            userInicioSesion = str(input("Usuario: "))
            passwordInicioSesion = str(input("Contraseña: "))
            try:
                file = open("usuarios.csv", "r")
                datos = file.readlines()
                datosTotales = obtenerDatos(datos)
                file.close()
            except FileNotFoundError:
                print("\nEste usuario no se ha registrado")
                opcionesMenu()
                opcionMenu = pedirOpcion(["1","2","3"])
            for lista in datosTotales.values():
                if userInicioSesion == lista[1]:
                    if sha256_crypt.verify(passwordInicioSesion, lista[2]) == True:
                        print(f"\nSe ha iniciado sesion con exito!\nBienvenido {userInicioSesion}")
                        opciones()
                        opcion = pedirOpcion(["1","2","3","4","5","6","7","8","9"])
                        while opcion != 9:
                            if opcion == 1:
                                imprimir_ids_equipos()
                                equipo_id = input("\nIngrese el ID del equipo para ver el plantel: ")
                                equipo_id = id_invalido(equipo_id)
                                print()
                                obtener_plantel_equipo(equipo_id)
                                mostrar_plantel_equipo(equipo_id)
                                opciones()
                                opcion = pedirOpcion(["1","2","3","4","5","6","7","8","9"])
                            elif opcion == 2:
                                posiciones_temporada()
                                opciones()
                                opcion = pedirOpcion(["1","2","3","4","5","6","7","8","9"])
                            elif opcion == 3:
                                imprimir_ids_equipos()
                                equipoId = input("\nIngrese el ID del equipo para ver su información: ")
                                equipoId = id_invalido(equipoId)
                                print()
                                mostrarInfoEquipo(equipoId)
                                opciones()
                                opcion = pedirOpcion(["1","2","3","4","5","6","7","8","9"])
                            elif opcion == 4:
                                mostrar_grafico()
                                opciones()
                                opcion = pedirOpcion(["1","2","3","4","5","6","7","8","9"])
                            elif opcion == 5:
                                monto = input("Ingrese el monto que desea agregar: ")
                                while numero_invalido(monto):
                                    monto = input("\nMonto inválido, intente nuevamente: ")
                                monto = float(monto)
                                print()
                                cargarDinero(lista[0], datosTotales, monto)
                                opciones()
                                opcion = pedirOpcion(["1","2","3","4","5","6","7","8","9"])
                            elif opcion == 6:
                                pass
                                opciones()
                                opcion = pedirOpcion(["1","2","3","4","5","6","7","8","9"])
                            elif opcion == 7:
                                pass
                                opciones()
                                opcion = pedirOpcion(["1","2","3","4","5","6","7","8","9"])
                            elif opcion == 8:
                                imprimir_ids_equipos()
                                equipoId = input("\nIngrese el ID del equipo: ")
                                equipoId = id_invalido(equipoId)
                                lista[5] = float(lista[5])
                                apuestas(equipoId, lista[0], datosTotales, lista[5])
                                opciones()
                                opcion = pedirOpcion(["1","2","3","4","5","6","7","8","9"])
                        if opcion == 9:
                            opcionesMenu()
                            opcionMenu = pedirOpcion(["1","2","3"])
                            break
                    else:
                        print("\nLa contraseña es incorrecta")
                        opcionesMenu()
                        opcionMenu = pedirOpcion(["1","2","3"])
                        break
            else:
                print("\nEste usuario no se ha registrado")
                opcionesMenu()
                opcionMenu = pedirOpcion(["1","2","3"])
        elif opcionMenu == 2:
            registrarse()
            print("\nSe ha registrado con éxito!")
            opcionesMenu()
            opcionMenu = pedirOpcion(["1","2","3"])


main()
