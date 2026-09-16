import requests
import os
import sys
import signal
import platform


# ============================================================
# CONFIGURACIÓN
# ============================================================

IDIOMAS = {
    "es": "Español",
    "en": "Inglés"
}

origen = "es"
destino = "en"

API_URL = "https://api.mymemory.translated.net/get"

ultima_traduccion = ""

# Detectar sistema
WINDOWS = platform.system() == "Windows"


# ============================================================
# TERMINAL UNIX
# ============================================================

if not WINDOWS:
    import termios
    import tty


# ============================================================
# LIMPIAR TERMINAL
# ============================================================

def limpiar_terminal():
    os.system("cls" if WINDOWS else "clear")


# ============================================================
# CABECERA
# ============================================================

def mostrar_cabecera():

    limpiar_terminal()

    print("=" * 60)
    print("                    TRADUCTOR")
    print("=" * 60)
    print()

    print(
        f"              {IDIOMAS[origen]} → {IDIOMAS[destino]}"
    )

    print()

    print("=" * 60)
    print()

    print("Shift+L  →  Cambiar idiomas")
    print("Shift+C  →  Copiar traducción")
    print("Ctrl+C   →  Salir")

    print()
    print("-" * 60)
    print()


# ============================================================
# PORTAPAPELES
# ============================================================

def copiar_portapapeles(texto):

    if not texto:
        mostrar_mensaje(
            "No hay ninguna traducción para copiar."
        )
        return False

    # --------------------------------------------------------
    # WINDOWS
    # --------------------------------------------------------

    if WINDOWS:

        try:

            import subprocess

            proceso = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-Command",
                    "Set-Clipboard -Value ([Console]::In.ReadToEnd())"
                ],
                input=texto,
                text=True,
                capture_output=True
            )

            if proceso.returncode == 0:
                return True

            return False

        except Exception:
            return False

    # --------------------------------------------------------
    # TERMUX
    # --------------------------------------------------------

    if "TERMUX_VERSION" in os.environ:

        try:

            proceso = subprocess.run(
                ["termux-clipboard-set"],
                input=texto,
                text=True,
                capture_output=True
            )

            return proceso.returncode == 0

        except Exception:

            return False

    # --------------------------------------------------------
    # LINUX - xclip
    # --------------------------------------------------------

    try:

        import shutil
        import subprocess

        if shutil.which("xclip"):

            proceso = subprocess.run(
                ["xclip", "-selection", "clipboard"],
                input=texto,
                text=True,
                capture_output=True
            )

            if proceso.returncode == 0:
                return True

        # ----------------------------------------------------
        # LINUX - xsel
        # ----------------------------------------------------

        if shutil.which("xsel"):

            proceso = subprocess.run(
                ["xsel", "--clipboard", "--input"],
                input=texto,
                text=True,
                capture_output=True
            )

            if proceso.returncode == 0:
                return True

        # ----------------------------------------------------
        # Wayland - wl-copy
        # ----------------------------------------------------

        if shutil.which("wl-copy"):

            proceso = subprocess.run(
                ["wl-copy"],
                input=texto,
                text=True,
                capture_output=True
            )

            if proceso.returncode == 0:
                return True

    except Exception:

        pass

    return False


# ============================================================
# MENSAJE TEMPORAL
# ============================================================

def mostrar_mensaje(mensaje):

    print()
    print(mensaje)
    print()


# ============================================================
# DIVIDIR TEXTO LARGO
# ============================================================

def dividir_texto(texto, max_bytes=450):

    palabras = texto.split()

    trozos = []

    actual = ""

    for palabra in palabras:

        if actual:
            candidato = actual + " " + palabra
        else:
            candidato = palabra

        if len(candidato.encode("utf-8")) <= max_bytes:

            actual = candidato

        else:

            if actual:
                trozos.append(actual)

            # Palabra demasiado larga
            if len(palabra.encode("utf-8")) > max_bytes:

                parte = ""

                for caracter in palabra:

                    prueba = parte + caracter

                    if len(prueba.encode("utf-8")) <= max_bytes:

                        parte = prueba

                    else:

                        if parte:
                            trozos.append(parte)

                        parte = caracter

                actual = parte

            else:

                actual = palabra

    if actual:
        trozos.append(actual)

    return trozos


# ============================================================
# TRADUCIR UN TROZO
# ============================================================

def traducir_trozo(texto):

    parametros = {
        "q": texto,
        "langpair": f"{origen}|{destino}",
        "mt": "1"
    }

    try:

        respuesta = requests.get(
            API_URL,
            params=parametros,
            timeout=15
        )

        respuesta.raise_for_status()

        datos = respuesta.json()

        if datos.get("responseStatus") != 200:

            raise Exception(
                datos.get(
                    "responseDetails",
                    "Error desconocido"
                )
            )

        traduccion = (
            datos
            .get("responseData", {})
            .get("translatedText")
        )

        if not traduccion:

            raise Exception(
                "La API no devolvió ninguna traducción."
            )

        return traduccion

    except requests.exceptions.Timeout:

        raise Exception(
            "Tiempo de espera agotado."
        )

    except requests.exceptions.ConnectionError:

        raise Exception(
            "No se pudo conectar con el servicio de traducción."
        )

    except requests.exceptions.HTTPError as error:

        raise Exception(
            f"Error HTTP: {error}"
        )


# ============================================================
# TRADUCIR TEXTO COMPLETO
# ============================================================

def traducir(texto):

    trozos = dividir_texto(texto)

    traducciones = []

    for trozo in trozos:

        traducciones.append(
            traducir_trozo(trozo)
        )

    return " ".join(traducciones)


# ============================================================
# CAMBIAR IDIOMAS
# ============================================================

def cambiar_idiomas():

    global origen
    global destino

    origen, destino = destino, origen

    mostrar_cabecera()


# ============================================================
# LECTURA DE TECLADO
# ============================================================

class Teclado:

    def __init__(self):

        self.modo_original = None

        if not WINDOWS:

            self.modo_original = termios.tcgetattr(
                sys.stdin
            )

            tty.setraw(sys.stdin.fileno())

    def restaurar(self):

        if not WINDOWS and self.modo_original:

            termios.tcsetattr(
                sys.stdin,
                termios.TCSADRAIN,
                self.modo_original
            )

    def leer(self):

        # ====================================================
        # WINDOWS
        # ====================================================

        if WINDOWS:

            import msvcrt

            tecla = msvcrt.getwch()

            return tecla

        # ====================================================
        # LINUX / TERMUX
        # ====================================================

        return sys.stdin.read(1)


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():

    global ultima_traduccion

    teclado = Teclado()

    texto = ""

    mostrar_cabecera()

    print("Texto: ", end="", flush=True)

    try:

        while True:

            tecla = teclado.leer()

            # =================================================
            # CTRL+C
            # =================================================

            if tecla == "\x03":

                break

            # =================================================
            # ENTER
            # =================================================

            if tecla in ("\r", "\n"):

                if not texto.strip():
                    continue

                print()
                print()
                print("Traduciendo...")
                print()

                try:

                    resultado = traducir(texto)

                    ultima_traduccion = resultado

                    print("-" * 60)
                    print("TRADUCCIÓN:")
                    print()
                    print(resultado)
                    print("-" * 60)
                    print()

                except Exception as error:

                    ultima_traduccion = ""

                    print("-" * 60)
                    print("ERROR:")
                    print()
                    print(error)
                    print("-" * 60)
                    print()

                texto = ""

                print("Texto: ", end="", flush=True)

                continue

            # =================================================
            # BACKSPACE
            # =================================================

            if tecla in ("\x08", "\x7f"):

                if texto:

                    texto = texto[:-1]

                    print(
                        "\b \b",
                        end="",
                        flush=True
                    )

                continue

            # =================================================
            # SHIFT + L
            # =================================================
            #
            # En una terminal, Shift+L llega como "L".
            # La "l" minúscula normal llega como "l".
            #
            # =================================================

            if tecla == "L":

                cambiar_idiomas()

                texto = ""

                print(
                    "Texto: ",
                    end="",
                    flush=True
                )

                continue

            # =================================================
            # SHIFT + C
            # =================================================
            #
            # Shift+C llega como "C".
            #
            # =================================================

            if tecla == "C":

                if copiar_portapapeles(
                    ultima_traduccion
                ):

                    mostrar_mensaje(
                        "✓ Traducción copiada al portapapeles."
                    )

                else:

                    mostrar_mensaje(
                        "✗ No se pudo copiar al portapapeles."
                    )

                print(
                    "Texto: " + texto,
                    end="",
                    flush=True
                )

                continue

            # =================================================
            # CARACTER NORMAL
            # =================================================

            if tecla.isprintable():

                texto += tecla

                print(
                    tecla,
                    end="",
                    flush=True
                )

    except KeyboardInterrupt:

        pass

    finally:

        teclado.restaurar()

        print()
        print()
        print("Saliendo...")


# ============================================================
# INICIO
# ============================================================

if __name__ == "__main__":

    main()