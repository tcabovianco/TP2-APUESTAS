import http.client
import json
import requests
import os
from PIL import Image
from passlib.hash import sha256_crypt
import matplotlib.pyplot as plt
import random
import datetime
import termcolor

def opcionesMenu() -> None:
    termcolor.cprint ("════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════", "cyan")
    print("\n+-----+ Menú +-----+")
    termcolor.cprint ("════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════", "cyan")
    print("1. Iniciar sesión")
    print("2. Registrarse")
    print("3. Salir\n")
    termcolor.cprint ("════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════", "cyan")

def opciones() -> None:
    termcolor.cprint ("════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════", "cyan")
    print("\nOpciones:")
    termcolor.cprint ("════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════", "cyan")
    print("1. Mostrar el plantel completo de un equipo")
    print("2. Mostrar la tabla de posiciones de la Liga Profesional")
    print("3. Datos de un equipo")
    print("4. Gráfico de goles en función de minutos para un equipo")
    print("5. Cargar dinero")
    print("6. Usuario que más dinero apostó")
    print("7. Usuario que más veces ganó")
    print("8. Apuestas")
    print("9. Cerrar sesion\n")
    termcolor.cprint ("════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════", "cyan")

def pedirOpcion(opciones: list) -> int:
    termcolor.cprint ("════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════", "cyan")
    opcion = input("Elegir opción: ")
    while numero_invalido(opcion) or opcion not in opciones:
        opcion = input("\nPor favor, ingrese una opción válida: ")
    opcion = int(opcion)
    termcolor.cprint ("════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════", "cyan")
    return opcion

def registrarse() -> None:
    termcolor.cprint ("════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════", "cyan")
    #Esta funcion permite al usuario registrarse, guardando sus datos en el archivo "usuarios.csv"
    registrarIdUser = str(input("Mail: "))
    registrarIdUser = validarMail(registrarIdUser)
    termcolor.cprint ("════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════", "cyan")
    registrarUsername = str(input("Usuario: "))
    termcolor.cprint ("════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════", "cyan")
    registrarPassword = str(input("Contraseña: "))
    termcolor.cprint ("════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════", "cyan")
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
    termcolor.cprint ("════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════", "cyan")
    print("\nA continuación se muestran los equipos y sus respectivas IDs:")
    termcolor.cprint ("════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════", "cyan")

    for equipo, id_equipo in equipos.items():
        print(f"{equipo}: {id_equipo}")
    termcolor.cprint ("════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════", "cyan")
    
def posiciones_temporada() -> None:
    lista_años = ["2015", "2016", "2017", "2018", "2019"]
    termcolor.cprint("════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════", "cyan")
    print("\nLas temporadas disponibles son: 2015, 2016, 2017, 2018, 2019")
    año = input("Ingrese el año para ver la tabla de posiciones: ")
    termcolor.cprint("════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════", "cyan")

    while año not in lista_años:
        año = input("Año inválido, intente nuevamente: ")
        print()

    conn = http.client.HTTPSConnection("v3.football.api-sports.io")
    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "c58299203753a8108c210738ab6b68a5"
    }

    conn.request("GET", f"/standings?league=128&season={año}", headers=headers)
    res = conn.getresponse()
    data = res.read()

    archivo = f"posicion {año}.json"

    with open(f"Tabla de posiciones/{archivo}", 'wb') as json_file:
        json_file.write(data)

    with open(f"Tabla de posiciones/{archivo}", 'r') as json_file:
        data = json.load(json_file)

    standings = data['response'][0]['league']['standings']

    termcolor.cprint("════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════", "cyan")
    for ranking in standings:
        print(ranking[0]["group"])
        for position in ranking:
            rank = position['rank']
            team = position['team']['name']
            points = position['points']
            goals_diff = position['goalsDiff']
            print(f"{rank}. {team}, {points} Pts, ({goals_diff})")
        print()
    termcolor.cprint("════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════", "cyan")

def mostrarInfoEquipo(equipoId) -> None:
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")

    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "c58299203753a8108c210738ab6b68a5"
    }

    conn.request("GET", "/teams?league=128&season=2023", headers=headers)

    res = conn.getresponse()
    data = res.read()

    data_decoded = data.decode("utf-8")

    file_path = "info_equipos.json"
    with open(file_path, "w") as json_file:
        json_file.write(data_decoded)

    print("Datos guardados en el archivo JSON:", file_path)
    with open(file_path, "r") as json_file:
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
            
            # Mostrar logoEquipo
            print("\nCargando imagen...")
            r = requests.get(logoEquipo)
            with open(f'logoEquipo{nombreEquipo}.png', 'wb') as f:
                f.write(r.content)
            imagen = Image.open(f'logoEquipo{nombreEquipo}.png')
            imagen.show()
            os.remove(f'logoEquipo{nombreEquipo}.png')  # Nota: elimina la imagen para no ocupar memoria
            
            print("\n+-----+ Información sobre su estadio +-----+")
            print(f"Nombre: {nombreEstadio}\tDirección: {direccionEstadio}")
            print(f"Ciudad: {ciudadEstadio}\tCapacidad: {capacidadEstadio}\tSuperficie: {superficieEstadio}")
            
            # Mostrar imagenEstadio
            print("\nCargando imagen...")
            r = requests.get(imagenEstadio)
            with open(f'imagenEstadio{nombreEquipo}.png', 'wb') as f:
                f.write(r.content)
            imagen = Image.open(f'imagenEstadio{nombreEquipo}.png')
            imagen.show()
            os.remove(f'imagenEstadio{nombreEquipo}.png')  # Nota: elimina la imagen para no ocupar memoria
            
            break
    else:
        print(f"\nNo se encontró información para el equipo con ID {equipoId}")

def mostrar_grafico():
    imprimir_ids_equipos()
    print()
    termcolor.cprint ("════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════", "cyan")
    equipo_id = input("Ingrese el ID del equipo: ")
    equipo_id = id_invalido(equipo_id)
    termcolor.cprint ("════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════", "cyan")
    
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
    añoDeposita = datetime.datetime.now().year
    mesDeposita = datetime.datetime.now().month
    diaDeposita = datetime.datetime.now().day
    fechaDeposita = f"{añoDeposita}" + f"{mesDeposita}" + f"{diaDeposita}"
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
            with open("transacciones.csv", "a") as fileTransacciones:
                fileTransacciones.write(f"{idUser},{fechaDeposita},Deposita,{monto}\n")

def tirar_dados():
    valores_dados = [
        termcolor.colored("┌───────┐\n│       │\n│   ●   │\n│       │\n└───────┘", "magenta", attrs=["bold"]),
        termcolor.colored("┌───────┐\n│ ●     │\n│       │\n│     ● │\n└───────┘", "magenta", attrs=["bold"]),
        termcolor.colored("┌───────┐\n│ ●     │\n│   ●   │\n│     ● │\n└───────┘", "magenta", attrs=["bold"]),
        termcolor.colored("┌───────┐\n│ ●   ● │\n│       │\n│ ●   ● │\n└───────┘", "magenta", attrs=["bold"]),
        termcolor.colored("┌───────┐\n│ ●   ● │\n│   ●   │\n│ ●   ● │\n└───────┘", "magenta", attrs=["bold"]),
        termcolor.colored("┌───────┐\n│ ●   ● │\n│ ●   ● │\n│ ●   ● │\n└───────┘", "magenta", attrs=["bold"]),
    ]
    respuesta = random.randint(1, 3)
    termcolor.cprint("Se están tirando los dados para determinar el ganador...", "cyan")
    termcolor.cprint("☘ ¡Mucha suerte! ☘", "green", attrs=["bold"])
    termcolor.cprint("... El número es ...", "cyan")
    termcolor.cprint ("════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════", "cyan")
    print(valores_dados[respuesta-1])
    termcolor.cprint(f"El número que salió en los dados es {respuesta}", "yellow", attrs=["bold"])
    termcolor.cprint ("════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════", "cyan")
    return respuesta

def tirar_dados_2():
    valores_dados = [
        termcolor.colored("┌───────┐\n│       │\n│   ●   │\n│       │\n└───────┘", "magenta", attrs=["bold"]),
        termcolor.colored("┌───────┐\n│ ●     │\n│       │\n│     ● │\n└───────┘", "magenta", attrs=["bold"]),
        termcolor.colored("┌───────┐\n│ ●     │\n│   ●   │\n│     ● │\n└───────┘", "magenta", attrs=["bold"]),
        termcolor.colored("┌───────┐\n│ ●   ● │\n│       │\n│ ●   ● │\n└───────┘", "magenta", attrs=["bold"]),
        termcolor.colored("┌───────┐\n│ ●   ● │\n│   ●   │\n│ ●   ● │\n└───────┘", "magenta", attrs=["bold"]),
        termcolor.colored("┌───────┐\n│ ●   ● │\n│ ●   ● │\n│ ●   ● │\n└───────┘", "magenta", attrs=["bold"]),
    ]
    respuesta = random.randint(1, 4)
    termcolor.cprint("Se están tirando los dados para determinar su pago...", "cyan")
    termcolor.cprint("☘ ¡Mucha suerte! ☘", "green", attrs=["bold"])
    termcolor.cprint("... El número es ...", "cyan")
    termcolor.cprint ("════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════", "cyan")
    print(valores_dados[respuesta-1])
    termcolor.cprint(f"El número que salió en los dados es {respuesta}", "yellow", attrs=["bold"])
    termcolor.cprint ("════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════", "cyan")
    return respuesta

def apostar(equipoId, idUser, datosTotales, montoDisponible):
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

    win_or_draw = dataJson["response"][0]["predictions"]["win_or_draw"]
    local = dataJson["response"][0]["teams"]["home"]
    visitante = dataJson["response"][0]["teams"]["away"]

    if elegirId == local["id"] and win_or_draw == True:
        print(f"\nSi apostas por {local['name']}, se paga el %10 de lo que paga la apuesta")
        print(f"Si apostas por {visitante['name']}, se paga el %100 de lo que paga la apuesta")
    elif elegirId == local["id"] and win_or_draw == False:
        print(f"\nSi apostas por {visitante['name']}, se paga el %10 de lo que paga la apuesta")
        print(f"Si apostas por {local['name']}, se paga el %100 de lo que paga la apuesta")
    elif elegirId != local["id"] and win_or_draw == True:
        print(f"\nSi apostas por {visitante['name']}, se paga el %10 de lo que paga la apuesta")
        print(f"Si apostas por {local['name']}, se paga el %100 de lo que paga la apuesta")
    elif elegirId != local["id"] and win_or_draw == False:
        print(f"\nSi apostas por {local['name']}, se paga el %10 de lo que paga la apuesta")
        print(f"Si apostas por {visitante['name']}, se paga el %100 de lo que paga la apuesta")

    posiblesResultados = ["Ganador(L)", "Empate", "Ganador(V)"]
    apostarResultado = input("\nIngrese el resultado esperado para el equipo que eligio /Ganador(L)/Empate/Ganador(V)/: ")
    if apostarResultado not in posiblesResultados:
        apostarResultado = input("Resultado inválido, intente nuevamente /Ganador(L)/Empate/Ganador(V)/: ")

    apostarMonto = input("\nIngrese el monto que desea apostar: ")
    while numero_invalido(apostarMonto):
        apostarMonto = input("\nMonto inválido, intente nuevamente: ")
    apostarMonto = float(apostarMonto)
    if apostarMonto > montoDisponible or apostarMonto <= 0:
        if apostarMonto > montoDisponible:
            print("\nUsted no cuenta con ese monto en su cuenta")
            return None
        else:
            print("\nEse monto no es posible de apostar")
            return None

    dado = tirar_dados()
    if dado == 1:
        resultado = "Ganador(L)"
    elif dado == 2:
        resultado = "Empate"
    elif dado == 3:
        resultado = "Ganador(V)"

    n = tirar_dados_2 ()

    if resultado in ["Ganador(L)", "Ganador(V)"]:
        if apostarResultado == resultado and win_or_draw == True:
            paga = apostarMonto + apostarMonto*n*0.1
            resultadoFinal = "Gana"
            print(f"\n{resultado}!\nFelicitaciones!\nHa ganado: {paga}")
        elif apostarResultado == resultado and win_or_draw == False:
            paga = apostarMonto + apostarMonto*n
            resultadoFinal = "Gana"
            print(f"\n{resultado}!\nFelicitaciones!\nHa ganado: {paga}")
        elif apostarResultado != resultado and win_or_draw == True:
            paga = -apostarMonto
            resultadoFinal = "Pierde"
            print(f"\nResultado: {resultado}\nSuerte para la próxima!")
        elif apostarResultado != resultado and win_or_draw == False:
            paga = -apostarMonto
            resultadoFinal = "Pierde"
            print(f"\nResultado: {resultado}\nSuerte para la próxima!")
    else:
        if apostarResultado == resultado and win_or_draw == True:
            paga = apostarMonto + apostarMonto*n*0.05
            resultadoFinal = "Gana"
            print(f"\n{resultado}!\nFelicitaciones!\nHa ganado: {paga}")
        elif apostarResultado == resultado and win_or_draw == False:
            paga = apostarMonto + apostarMonto*n
            resultadoFinal = "Gana"
            print(f"\n{resultado}!\nFelicitaciones!\nHa ganado: {paga}")
        elif apostarResultado != resultado and win_or_draw == True:
            paga = -apostarMonto
            resultadoFinal = "Pierde"
            print(f"\nResultado: {resultado}\nSuerte para la próxima!")
        elif apostarResultado != resultado and win_or_draw == False:
            paga = -apostarMonto
            resultadoFinal = "Pierde"
            print(f"\nResultado: {resultado}\nSuerte para la próxima!")

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

    with open("transacciones.csv", "a") as fileTransacciones:
        fileTransacciones.write(f"{idUser},{fechaApuesta},{resultadoFinal},{paga}\n")

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
                                apostar(equipoId, lista[0], datosTotales, lista[5])
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
