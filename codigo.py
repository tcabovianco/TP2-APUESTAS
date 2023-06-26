import http.client, json, requests, os, random, datetime, termcolor, pyfiglet
import matplotlib.pyplot as plt
from passlib.hash import sha256_crypt
from colorama import init
from PIL import Image


def imprimirLinea() -> None:
    #Imprime una linea de color cyan

    init(autoreset = True)
    termcolor.cprint ("════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════", "cyan")


def opcionesMenu() -> None:
    #Imprime las opciones del menú

    imprimirLinea()
    print("+---------------+ Menú +---------------+")
    imprimirLinea()
    print("1. Iniciar sesión")
    print("2. Registrarse")
    print("3. Salir")
    imprimirLinea()


def opciones() -> None:
    # Imprime las opciones

    imprimirLinea()
    termcolor.cprint("+---------------+ Opciones +---------------+", "magenta")
    imprimirLinea()
    termcolor.cprint("1. Mostrar el plantel completo de un equipo", "yellow", attrs=["bold"])
    termcolor.cprint("2. Mostrar la tabla de posiciones de la Liga Profesional", "yellow", attrs=["bold"])
    termcolor.cprint("3. Datos de un equipo", "yellow", attrs=["bold"])
    termcolor.cprint("4. Gráfico de goles en función de minutos para un equipo", "yellow", attrs=["bold"])
    termcolor.cprint("5. Cargar dinero", "yellow", attrs=["bold"])
    termcolor.cprint("6. Usuario que más dinero apostó", "yellow", attrs=["bold"])
    termcolor.cprint("7. Usuario que más veces ganó", "yellow", attrs=["bold"])
    termcolor.cprint("8. Apuestas", "yellow", attrs=["bold"])
    termcolor.cprint("9. Cerrar sesión", "white",attrs=["bold"])
    imprimirLinea()


def pedirOpcion(opciones: list) -> int:
    #Pide una opción al usuario y valida que la misma exista

    opcion = input(termcolor.colored("Elegir opción: ", attrs=["bold"]))

    while numero_invalido(opcion) or opcion not in opciones:
        opcion = input(termcolor.colored("Por favor, ingrese una opción válida: ", "red", attrs=["bold"]))

    opcion = int(opcion)
    imprimirLinea()

    return opcion


def registrarse() -> None:
    #Permite al usuario registrarse, guardando sus datos en el archivo "usuarios.csv"; donde: Mail,Username,Password,CantidadApostada,FechaUltimaApuesta,DineroDisponible

    idUser = input(termcolor.colored("Mail: ", attrs=["bold"]))
    idUser = validarMail(idUser)
     username = input(termcolor.colored("Usuario: ", attrs=["bold"]))
    password = input(termcolor.colored("Contraseña: ", attrs=["bold"]))
    hashPassword = sha256_crypt.hash(password)
    
    with open("usuarios.csv", "a") as f:
        f.write(f"{idUser},{username},{hashPassword}, 0, No se ha realizado ninguna apuesta, 0\n")


def obtenerDatos(datos: list) -> list:
    #Toma ciertos datos contenidos en una lista, y los devuelve como un diccionario con una lista para cada usuario

    x = []
    datosTotales = {}

    for dato in datos:
        x.append(dato.split(","))

    for dato in x:
        datosTotales[dato[0]] = dato

    return datosTotales


def numero_invalido(numero: str) -> bool:
    #Valida que el valor ingresado sea un número

    try:
        float(numero)
        return False

    except ValueError:
        return True


def id_invalido(id_equipo: str) -> int:
    #Valida que la id de un equipo exista

    id_valido = ["434", "435","436","437","438","439","440", "441", "442", "443", "445", "446", "448","449", "450" , "451", "452", "453", "455", "456", "457", "458", "459","460", "474","478", "1024","1025", "2432"]

    while id_equipo not in id_valido or numero_invalido(id_equipo):
        id_equipo = input(termcolor.colored("ID inválida, por favor intente nuevamente: ", "red", attrs=["bold"])) 
  
    id_equipo = int(id_equipo)

    return id_equipo


def validarMail(mail: str) -> str:
    #Valida que el valor ingresado contenga ".com" y "@"

    while mail.endswith(".com") != True:
        mail = input(termcolor.colored("Mail inválido, debe usar \"@\" y terminar con \".com\": ", "red", attrs=["bold"]))
        mail.endswith(".com")

    mail = list(mail)

    while "@" not in mail:
        mail = input(termcolor.colored("Mail inválido, debe usar \"@\" y terminar con \".com\": ", "red", attrs=["bold"]))
        mail = list(mail)

    mail = "".join(mail)

    return mail


def fechaActual() -> str:
    #Define la fecha en la que se llama a la función

    año = datetime.datetime.now().year
    mes = datetime.datetime.now().month
    dia = datetime.datetime.now().day

    fecha = f"{año}" + f"{mes}" + f"{dia}"

    return fecha


def obtener_plantel_equipo(equipo_id: int) -> None:
    #Crea un archivo .json con los datos del plantel del equipo ingresado

    conn = http.client.HTTPSConnection("v3.football.api-sports.io")

    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "3acf8ad408e18c67e1da7a3a32ea624b"}

    conn.request("GET", f"/players/squads?team={equipo_id}", headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")

    with open("plantel_equipo.json", "w") as json_file:
        json_file.write(data)


def mostrar_plantel_equipo() -> None:
    #Imprime los datos del plantel del equipo elegido, y luego, elimina el archivo .json para ahorrar espacio

    with open("plantel_equipo.json", "r") as json_file:
        data = json.load(json_file)

    plantel_json = data["response"]

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
    print()

    os.remove("plantel_equipo.json")


def imprimir_ids_equipos() -> None:
    #Imprime las ids de cada equipo de la Liga Profesional

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
    print("A continuación se muestran los equipos y sus respectivas IDs")
    imprimirLinea()

    for equipo, id_equipo in equipos.items():
        equipo_coloreado = termcolor.colored(equipo, "magenta")
        idEquipo_coloreada = termcolor.colored(str(idEquipo), "cyan")
        print(f"{equipo_coloreado}: {idEquipo_coloreada}")
    imprimirLinea()


def posiciones_temporada() -> None:
    #Imprime las posiciones de la temporada elegida

    lista_años = ["2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"]
    termcolor.cprint(termcolor.colored("Las temporadas disponibles son: ", attrs=["bold"]) + ", ".join(termcolor.colored(año, "yellow") for año in lista_años))

    año = input(termcolor.colored("\nIngrese el año para ver la tabla de posiciones: ", attrs=["bold"]))
    imprimirLinea()

    while año not in lista_años:
        año = input(termcolor.colored("Año inválido, intente nuevamente: ", "red" ,attrs=["bold"]))

    conn = http.client.HTTPSConnection("v3.football.api-sports.io")

    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "c58299203753a8108c210738ab6b68a5"}

    conn.request("GET", f"/standings?league=128&season={año}", headers=headers)
    res = conn.getresponse()
    data = res.read()

    archivo = f"posicion {año}.json"

    with open(f"Tabla de posiciones/{archivo}", 'wb') as json_file:
        json_file.write(data)

    with open(f"Tabla de posiciones/{archivo}", 'r') as json_file:
        data = json.load(json_file)

    standings = data['response'][0]['league']['standings']
    imprimirLinea()
    
    for ranking in standings:
        
        if año in ["2020", "2021", "2022"]:
            print(termcolor.colored(f"+----+ {ranking[0]['group']} +----+", "cyan"))

        for position in ranking:
            rank = position['rank']
            team = position['team']['name']
            points = position['points']
            goals_diff = position['goalsDiff']

            rank_coloreado = termcolor.colored(str(rank), "magenta")
            team_coloreado = termcolor.colored(team, "cyan")
            points_coloreados = termcolor.colored(str(points) + " Pts", "yellow")
            goals_diff_coloreado = termcolor.colored("(" + str(goals_diff) + ")", "white")

            print(f"{rank_coloreado}. {team_coloreado}, {points_coloreados}, {goals_diff_coloreado}")
        print()

def mostrarInfoEquipo(equipoId: int) -> None:
    #Imprime la información del equipo elegido, incluyendo las fotos de su logo y su estadio. Las mismas son eliminadas posteriormente para así ahorrar espacio

    conn = http.client.HTTPSConnection("v3.football.api-sports.io")

    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "3acf8ad408e18c67e1da7a3a32ea624b"}

    conn.request("GET", "/teams?league=128&season=2023", headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")

    with open("info_equipos.json", "w") as json_file:
        json_file.write(data)
    
    with open("info_equipos.json", "r") as json_file:
        data = json.load(json_file)
    
    info_json = data["response"]

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
            
            print(termcolor.colored(f"+-----+ Información básica sobre el equipo {nombreEquipo} +-----+", "blue",attrs=["bold"]))
            print(f"Codigo: {termcolor.colored(codigoEquipo, 'magenta')}\tPaís de origen: {termcolor.colored(paisEquipo, 'cyan')}\tAño de fundación: {termcolor.colored(fundacionEquipo, 'yellow')}")
            
            # Mostrar logoEquipo
            termcolor.cprint("\nCargando imagen...", "blue")
            r = requests.get(logoEquipo)

            with open(f'logoEquipo{nombreEquipo}.png', 'wb') as f:
                f.write(r.content)

            imagen = Image.open(f'logoEquipo{nombreEquipo}.png')
            imagen.show()
            os.remove(f'logoEquipo{nombreEquipo}.png')
            
            termcolor.cprint("\n+-----+ Información sobre su estadio +-----+", "blue",attrs=["bold"]))
            print(f"Nombre: {termcolor.colored(nombreEstadio, 'magenta')}\tDirección: {termcolor.colored(direccionEstadio, 'cyan')}")
            print(f"Ciudad: {termcolor.colored(ciudadEstadio, 'yellow')}\tCapacidad: {termcolor.colored(capacidadEstadio, 'magenta')}\tSuperficie: {termcolor.colored(superficieEstadio, 'cyan')}")
            
            # Mostrar imagenEstadio
            termcolor.cprint("\nCargando imagen...", "blue")
            r = requests.get(imagenEstadio)

            with open(f'imagenEstadio{nombreEquipo}.png', 'wb') as f:
                f.write(r.content)

            imagen = Image.open(f'imagenEstadio{nombreEquipo}.png')
            imagen.show()
            os.remove(f'imagenEstadio{nombreEquipo}.png')
            os.remove("info_equipos.json")
            
            break
    else:
        termcolor.cprint(f"\nNo se encontró información para el equipo con ID {equipoId}", "red", attrs=["bold"])


def mostrar_grafico() -> None:
    #Imprime el gráfico del equipo elegido

    imprimir_ids_equipos()
    equipo_id = input(termcolor.colored("Ingrese el ID del equipo: ", attrs=["bold"]))
    equipo_id = id_invalido(equipo_id)
    
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")

    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "c58299203753a8108c210738ab6b68a5"}

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
    os.remove(f"equipo_{equipo_id}.json")


def cargarDinero(idUser: int, datosTotales: list, monto: float) -> None:
    #Añade dinero a la cuenta del usuario

    fechaDeposita = fechaActual()
    for lista in datosTotales.values():

        if idUser == lista[0]:
            lista[5] = float(lista[5])
            lista[5] += monto

            print("Monto agregado con éxito!")
            os.remove("usuarios.csv")

            with open("usuarios.csv", "a") as f:

                for usuario in datosTotales.values():
                    for datos in usuario:
                        f.write(f"{datos},")
                    f.write("\n")

            with open("transacciones.csv", "a") as fT:
                fT.write(f"{idUser},{fechaDeposita},Deposita,{monto}\n")


def mayorApostador(datosTotales: list) -> None:
    #Obtiene el usuario que más apostó y el monto apostado

    montoApostado = 0
    montoApostado = float(montoApostado)

    for datos in datosTotales.values():
        datos[3] = float(datos[3])

        if datos[3] > montoApostado:
            montoApostado = datos[3]
            user = datos[1]

    return user, montoApostado


def obtener_usuario_mas_ganador() -> None:
    # Obtiene el usuario más ganador a partir del archivo transacciones

    victorias_por_usuario = {}

    try:
        with open("transacciones.csv", "r") as fT:

            for linea in fT:
                datos = linea.strip().split(",")
                idUser = datos[0]
                resultadoFinal = datos[2]

                if resultadoFinal == "Gana":
                    if idUser in victorias_por_usuario:
                        victorias_por_usuario[idUser] += 1
                    else:
                        victorias_por_usuario[idUser] = 1

    except FileNotFoundError:
        termcolor.cprint("Ningun usuario ha apostado aún", "red", attrs=["bold"])
        return None

    try:
        usuario_mas_ganador = max(victorias_por_usuario, key=victorias_por_usuario.get)
        cantidad_victorias = victorias_por_usuario[usuario_mas_ganador]

        termcolor.cprint(f"El usuario más ganador es: {usuario_mas_ganador}", "green", attrs=["bold"])
        termcolor.cprint(f"Cantidad de victorias: {cantidad_victorias}", "cyan", attrs=["bold"])

    except ValueError:
        termcolor.cprint("Ningún usuario ha ganado una apuesta aún", "red", attrs=["bold"])
        return None


def tirar_dados() -> int:
    #Función que define el resultado del partido

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
    imprimirLinea()
    print(valores_dados[respuesta-1])

    termcolor.cprint(f"El número que salió en los dados es {respuesta}", "yellow", attrs=["bold"])
    imprimirLinea()

    return respuesta


def tirar_dados_2() -> int:
    #Función que define por cuánto se multiplica la apuesta

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
    imprimirLinea()
    print(valores_dados[respuesta-1])

    termcolor.cprint(f"El número que salió en los dados es {respuesta}", "yellow", attrs=["bold"])
    imprimirLinea()

    return respuesta

def imprimir_ganador():
    texto = "FELICIDADES!"
    colores = ['yellow', 'green', 'blue', 'magenta', 'cyan', 'red','yellow', 'green', 'blue', 'magenta', 'cyan', 'red']
    letras_figlet = [pyfiglet.figlet_format(letra) for letra in texto]
    letras_coloreadas = [' '.join(termcolor.colored(letra.split('\n')[i], color, attrs=['bold']) for letra, color in zip(letras_figlet, colores)) for i in range(len(letras_figlet[0].split('\n')))]
    texto_combinado = '\n'.join(letras_coloreadas)
    print(texto_combinado)
    
def imprimir_perdedor():
    texto = pyfiglet.figlet_format("PERDIÓ")
    mostrar_texto = termcolor.colored(texto, 'red', attrs=['bold'])
    print(mostrar_texto)   
    
def apostar(equipoId: int, idUser: int, datosTotales: list, montoDisponible: float) -> None:

    conn = http.client.HTTPSConnection("v3.football.api-sports.io")

    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "3acf8ad408e18c67e1da7a3a32ea624b"}

    conn.request("GET", "/fixtures?league=128&season=2023", headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")

    with open("fixtures.json", "w") as json_file:
        json_file.write(data)

    with open("fixtures.json", "r") as json_file:
        json_file = json.load(json_file)
    
    fixtures = []

    for elemento in json_file["response"]:
        if elemento["teams"]["home"]["id"] == equipoId or elemento["teams"]["away"]["id"] == equipoId:
            fixtures.append(elemento["fixture"]["id"])
    
    termcolor.cprint("\nElija una ID para ingresar al partido donde desea apostar\n", attrs=["bold"])

    for fixture in fixtures:
        for elemento in json_file["response"]:
            if fixture == elemento["fixture"]["id"]:
                print(f"+---+ ID: {fixture} +---+")
                print(f"Local: {elemento['teams']['home']['name']}\nVisitante: {elemento['teams']['away']['name']}\n")
    imprimirLinea()

    elegirId = input(termcolor.colored("Elegir ID: ", attrs=["bold"]))
    while numero_invalido(elegirId) or int(elegirId) not in fixtures:
        elegirId = input(termcolor.colored("ID inválida, intente nuevamente: ", "red", attrs=["bold"]))
    imprimirLinea()
        
    conn = http.client.HTTPSConnection("v3.football.api-sports.io")

    headers = {
        'x-rapidapi-host': "v3.football.api-sports.io",
        'x-rapidapi-key': "3acf8ad408e18c67e1da7a3a32ea624b"}

    conn.request("GET", f"/predictions?fixture={elegirId}", headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")

    with open(f"fixture_{elegirId}.json", "w") as json_file:
        json_file.write(data)

    with open(f"fixture_{elegirId}.json", "r") as json_file:
        data = json.load(json_file)

    win_or_draw = data["response"][0]["predictions"]["win_or_draw"]
    local = data["response"][0]["teams"]["home"]
    visitante = data["response"][0]["teams"]["away"]

    print(f"Local: {local['name']}\tVisitante: {visitante['name']}")

    if elegirId == local["id"] and win_or_draw == True:
        termcolor.cprint(f"\nSi apostas por {local['name']}, y ganas, se paga el %10 de lo que paga la apuesta", "cyan", attrs=["bold"])
        termcolor.cprint(f"Si apostas por {visitante['name']}, y ganas, se paga el %100 de lo que paga la apuesta", "magenta", attrs=["bold"])
        termcolor.cprint("Si apostas por Empate, y ganas, se paga el %5 de lo que paga la apuesta", "yellow", attrs=["bold"])

    elif elegirId == local["id"] and win_or_draw == False:
        termcolor.cprint(f"\nSi apostas por {visitante['name']}, y ganas, se paga el %10 de lo que paga la apuesta", "cyan", attrs=["bold"])
        termcolor.cprint(f"Si apostas por {local['name']}, y ganas, se paga el %100 de lo que paga la apuesta", "magenta", attrs=["bold"])
        termcolor.cprint("Si apostas por Empate, y ganas, se paga el %5 de lo que paga la apuesta", "yellow", attrs=["bold"])

    elif elegirId != local["id"] and win_or_draw == True:
        termcolor.cprint(f"\nSi apostas por {visitante['name']}, y ganas, se paga el %10 de lo que paga la apuesta", "cyan", attrs=["bold"])
        termcolor.cprint(f"Si apostas por {local['name']}, y ganas, se paga el %100 de lo que paga la apuesta", "magenta", attrs=["bold"])
        termcolor.cprint("Si apostas por Empate, y ganas, se paga el %5 de lo que paga la apuesta", "yellow", attrs=["bold"])

    elif elegirId != local["id"] and win_or_draw == False:
        termcolor.cprint(f"\nSi apostas por {local['name']}, y ganas, se paga el %10 de lo que paga la apuesta", "cyan", attrs=["bold"])
        termcolor.cprint(f"Si apostas por {visitante['name']}, y ganas, se paga el %100 de lo que paga la apuesta", "magenta", attrs=["bold"])
        termcolor.cprint("Si apostas por Empate, y ganas, se paga el %5 de lo que paga la apuesta", "yellow", attrs=["bold"])

    posiblesResultados = ["Ganador(L)", "Empate", "Ganador(V)"]
    apostarResultado = input(termcolor.colored("\nIngrese el resultado esperado para el equipo que eligio /Ganador(L)/Empate/Ganador(V)/: ", attrs=["bold"]))
    if apostarResultado not in posiblesResultados:
        apostarResultado = input(termcolor.colored("Resultado inválido, intente nuevamente /Ganador(L)/Empate/Ganador(V)/: ", "red", attrs=["bold"]))

    apostarMonto = input(termcolor.colored("\nIngrese el monto que desea apostar: ", attrs=["bold"]))
    while numero_invalido(apostarMonto):
        apostarMonto = input(termcolor.colored("\nMonto inválido, intente nuevamente: ", "red"))
    apostarMonto = float(apostarMonto)
    print()

    if apostarMonto > montoDisponible or apostarMonto <= 0:
        if apostarMonto > montoDisponible:
            termcolor.cprint("\nUsted no cuenta con ese monto en su cuenta", "red")
            os.remove(f"fixture_{elegirId}.json")
            os.remove("fixtures.json")
            return None
        else:
            termcolor.cprint("\nEse monto no es posible de apostar", "red")
            return None

    dado = tirar_dados()
    if dado == 1:
        resultado = "Ganador(L)"
    elif dado == 2:
        resultado = "Empate"
    elif dado == 3:
        resultado = "Ganador(V)"

    n = tirar_dados_2()

    if resultado in ["Ganador(L)", "Ganador(V)"]:
        if apostarResultado == resultado and win_or_draw == True:
            paga = apostarMonto + apostarMonto*n*0.1
            resultadoFinal = "Gana"
            imprimir_ganador()
            termcolor.cprint(f"{resultado}!\nFelicitaciones!\nHa ganado: {paga}", "green", attrs=["bold"])

        elif apostarResultado == resultado and win_or_draw == False:
            paga = apostarMonto + apostarMonto*n
            resultadoFinal = "Gana"
            imprimir_ganador()
            imprimirLinea()
            termcolor.cprint(f"{resultado}!\nFelicitaciones!\nHa ganado: {paga}", "green", attrs=["bold"])

        elif apostarResultado != resultado and win_or_draw == True:
            paga = -apostarMonto
            resultadoFinal = "Pierde"
            imprimir_perdedor()
            imprimirLinea()
            termcolor.cprint(f"Resultado: {resultado}\nSuerte para la próxima! ☘", "red", attrs=["bold"])

        elif apostarResultado != resultado and win_or_draw == False:
            paga = -apostarMonto
            resultadoFinal = "Pierde"
            imprimir_perdedor()
            imprimirLinea()
            termcolor.cprint(f"Resultado: {resultado}\nSuerte para la próxima! ☘", "red", attrs=["bold"])

    else:
        if apostarResultado == resultado and win_or_draw == True:
            paga = apostarMonto + apostarMonto*n*0.05
            resultadoFinal = "Gana"
            imprimir_ganador()
            imprimirLinea()
            termcolor.cprint(f"{resultado}!\nFelicitaciones!\nHa ganado: {paga}", "green", attrs=["bold"])

        elif apostarResultado == resultado and win_or_draw == False:
            paga = apostarMonto + apostarMonto*n
            resultadoFinal = "Gana"
            imprimir_ganador()
            imprimirLinea()
            termcolor.cprint(f"{resultado}!\nFelicitaciones!\nHa ganado: {paga}", "green", attrs=["bold"])

        elif apostarResultado != resultado and win_or_draw == True:
            paga = -apostarMonto
            resultadoFinal = "Pierde"
            imprimir_perdedor()
            imprimirLinea()
            termcolor.cprint(f"Resultado: {resultado}\nSuerte para la próxima! ☘", "red", attrs=["bold"])

        elif apostarResultado != resultado and win_or_draw == False:
            paga = -apostarMonto
            resultadoFinal = "Pierde"
            imprimir_perdedor()
            imprimirLinea()
            termcolor.cprint(f"Resultado: {resultado}\nSuerte para la próxima! ☘", "red", attrs=["bold"])

    fechaApuesta = fechaActual()
    for lista in datosTotales.values():
        if idUser == lista[0]:
            lista[5] = float(lista[5])
            lista[5] += paga
            lista[4] = fechaApuesta
            lista[3] = float(lista[3])
            lista[3] += apostarMonto
            os.remove("usuarios.csv")

            with open("usuarios.csv", "a") as f:
                for usuario in datosTotales.values():
                    for datos in usuario:
                        f.write(f"{datos},")
                    f.write("\n")

    with open("transacciones.csv", "a") as fT:
        fT.write(f"{idUser},{fechaApuesta},{resultadoFinal},{paga}\n")

    os.remove(f"fixture_{elegirId}.json")
    os.remove("fixtures.json")




def main() -> None:
    #Sección principal del código

    OPCIONESMENU = ["1","2","3"]
    OPCIONES = ["1","2","3","4","5","6","7","8","9"]

    opcionesMenu()
    opcionMenu = pedirOpcion(OPCIONESMENU)

    while opcionMenu != 3:

        if opcionMenu == 1:
            user = input(termcolor.colored("Usuario: "),  attrs=["bold"])
            password = input(termcolor.colored("Contraseña: ", attrs=["bold"]))

            try:
                with open("usuarios.csv", "r") as f:
                    datos = f.readlines()
                datosTotales = obtenerDatos(datos)

            except FileNotFoundError:
                termcolor.cprint("\nEste usuario no se ha registrado", "red",  attrs=["bold"])

                opcionesMenu()
                opcionMenu = pedirOpcion(OPCIONESMENU)

            try:
                for lista in datosTotales.values():

                    if user == lista[1]:
                        if sha256_crypt.verify(password, lista[2]) == True:
                            termcolor.cprint(f"\nSe ha iniciado sesion con exito!\nBienvenido {user}", "cyan" ,attrs=["bold"])

                            opciones()
                            opcion = pedirOpcion(OPCIONES)

                            while opcion != 9:

                                if opcion == 1:
                                    imprimir_ids_equipos()

                                    equipo_id = input(termcolor.colored("Ingrese el ", attrs=["bold"]) + termcolor.colored("ID", "cyan", attrs=["bold"]) + termcolor.colored(" del equipo para ver el plantel: ", attrs=["bold"]))
                                    
        
                                    equipo_id = id_invalido(equipo_id)

                                    print()
                                    obtener_plantel_equipo(equipo_id)
                                    mostrar_plantel_equipo()

                                    opciones()
                                    opcion = pedirOpcion(OPCIONES)

                                elif opcion == 2:
                                    posiciones_temporada()

                                    opciones()
                                    opcion = pedirOpcion(OPCIONES)

                                elif opcion == 3:
                                    imprimir_ids_equipos()

                                    equipoId =  input(termcolor.colored("Ingrese el ", attrs=["bold"]) + termcolor.colored("ID", "cyan", attrs=["bold"]) + termcolor.colored(" del equipo para ver su información: ", attrs=["bold"]))
                                    equipoId = id_invalido(equipoId)

                                    print()
                                    mostrarInfoEquipo(equipoId)

                                    opciones()
                                    opcion = pedirOpcion(OPCIONES)

                                elif opcion == 4:
                                    mostrar_grafico()

                                    opciones()
                                    opcion = pedirOpcion(OPCIONES)

                                elif opcion == 5:
                                    monto = input(termcolor.colored("Ingrese el monto que desea agregar: ", attrs=["bold"]))
                                    while numero_invalido(monto):
                                        monto = input(termcolor.colored("Monto inválido, intente nuevamente: ", "red", attrs=["bold"]))
                                    monto = float(monto)

                                    print()
                                    cargarDinero(lista[0], datosTotales, monto)

                                    opciones()
                                    opcion = pedirOpcion(OPCIONES)

                                elif opcion == 6:
                                    user, montoApostado = mayorApostador(datosTotales)
                                    termcolor.cprint(f"El usuario que más apostó fue {user}. Con un total de {montoApostado}!", "cyan", attrs=["bold"])

                                    opciones()
                                    opcion = pedirOpcion(OPCIONES)

                                elif opcion == 7:
                                    obtener_usuario_mas_ganador()

                                    opciones()
                                    opcion = pedirOpcion(OPCIONES)

                                elif opcion == 8:
                                    imprimir_ids_equipos()

                                    equipoId = input(termcolor.colored("Ingrese el ", attrs=["bold"]) + termcolor.colored("ID", "cyan", attrs=["bold"]) + termcolor.colored(" del equipo: ", attrs=["bold"]))
                                    
                                    equipoId = id_invalido(equipoId)

                                    lista[5] = float(lista[5])
                                    apostar(equipoId, lista[0], datosTotales, lista[5])

                                    opciones()
                                    opcion = pedirOpcion(OPCIONES)

                            if opcion == 9:
                                opcionesMenu()
                                opcionMenu = pedirOpcion(OPCIONESMENU)
                                break
                        else:
                            termcolor.cprint("\nLa contraseña es incorrecta", "red", attrs=["bold"])

                            opcionesMenu()
                            opcionMenu = pedirOpcion(OPCIONESMENU)
                            break
                else:
                    termcolor.cprint("\nEste usuario no se ha registrado", "red", attrs=["bold"])

                    opcionesMenu()
                    opcionMenu = pedirOpcion(OPCIONESMENU)

            except UnboundLocalError:
                termcolor.cprint("Por favor reinicie la página para continuar", "blue", attrs=["bold"])
                return None

        elif opcionMenu == 2:
            registrarse()
            termcolor.cprint("\nSe ha registrado con éxito!", "green", attrs=["bold"])

            opcionesMenu()
            opcionMenu = pedirOpcion(OPCIONESMENU)

main()
