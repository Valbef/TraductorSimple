import requests
import os
import platform
import subprocess


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

WINDOWS = platform.system() == "Windows"


# ============================================================
# LIMPIAR TERMINAL
# ============================================================

def limpiar_terminal():

    os.system(
        "cls" if WINDOWS else "clear"
    )


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

    print("L + Enter  →  Cambiar idiomas")
    print("C + Enter  →  Copiar traducción")
    print("Ctrl+C     →  Salir")

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

            return proceso.returncode == 0

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
    # LINUX
    # --------------------------------------------------------

    try:

        import shutil

        # ----------------------------------------------------
        # XCLIP
        # ----------------------------------------------------

        if shutil.which("xclip"):

            proceso = subprocess.run(
                [
                    "xclip",
                    "-selection",
                    "clipboard"
                ],
                input=texto,
                text=True,
                capture_output=True
            )

            if proceso.returncode == 0:

                return True

        # ----------------------------------------------------
        # XSEL
        # ----------------------------------------------------

        if shutil.which("xsel"):

            proceso = subprocess.run(
                [
                    "xsel",
                    "--clipboard",
                    "--input"
                ],
                input=texto,
                text=True,
                capture_output=True
            )

            if proceso.returncode == 0:

                return True

        # ----------------------------------------------------
        # WAYLAND
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
# MENSAJE
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

            candidato = (
                actual + " " + palabra
            )

        else:

            candidato = palabra

        if len(
            candidato.encode("utf-8")
        ) <= max_bytes:

            actual = candidato

        else:

            if actual:

                trozos.append(actual)

            # ------------------------------------------------
            # Palabra demasiado larga
            # ------------------------------------------------

            if len(
                palabra.encode("utf-8")
            ) > max_bytes:

                parte = ""

                for caracter in palabra:

                    prueba = (
                        parte + caracter
                    )

                    if len(
                        prueba.encode("utf-8")
                    ) <= max_bytes:

                        parte = prueba

                    else:

                        if parte:

                            trozos.append(
                                parte
                            )

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

    except requests.exceptions.RequestException as error:

        raise Exception(
            f"Error de conexión: {error}"
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
# PROGRAMA PRINCIPAL
# ============================================================

def main():

    global ultima_traduccion

    # --------------------------------------------------------
    # Indica si tenemos una traducción disponible para copiar.
    # --------------------------------------------------------

    traduccion_recibida = False

    mostrar_cabecera()

    while True:

        try:

            # =================================================
            # LEER UNA LÍNEA COMPLETA
            # =================================================
            #
            # input() se encarga de:
            #
            # - Enter
            # - Backspace
            # - edición de la línea
            # - Windows
            # - Linux
            # - Termux
            #
            # =================================================

            texto = input("Texto: ")

        except KeyboardInterrupt:

            print()
            print()
            print("Saliendo...")

            break

        except EOFError:

            print()
            print()
            print("Saliendo...")

            break

        # =====================================================
        # ELIMINAR ESPACIOS EXTERIORES
        # =====================================================

        texto = texto.strip()

        # =====================================================
        # ENTRADA VACÍA
        # =====================================================

        if not texto:

            continue

        # =====================================================
        # CAMBIAR IDIOMAS
        # =====================================================
        #
        # Escribir exactamente:
        #
        #     L
        #
        # y pulsar Enter.
        #
        # =====================================================

        if texto == "L":

            cambiar_idiomas()

            ultima_traduccion = ""

            traduccion_recibida = False

            continue

        # =====================================================
        # COPIAR TRADUCCIÓN
        # =====================================================
        #
        # Escribir:
        #
        #     C
        #
        # y pulsar Enter.
        #
        # Solo funciona si tenemos una traducción.
        # =====================================================

        if texto == "C":

            if not traduccion_recibida:

                mostrar_mensaje(
                    "No hay ninguna traducción para copiar."
                )

                continue

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

            continue

        # =====================================================
        # TRADUCIR
        # =====================================================

        print()
        print("Traduciendo...")
        print()

        traduccion_recibida = False

        try:

            resultado = traducir(
                texto
            )

            ultima_traduccion = resultado

            traduccion_recibida = True

            print("-" * 60)
            print("TRADUCCIÓN:")
            print()
            print(resultado)
            print("-" * 60)
            print()

        except Exception as error:

            ultima_traduccion = ""

            traduccion_recibida = False

            print("-" * 60)
            print("ERROR:")
            print()
            print(error)
            print("-" * 60)
            print()


# ============================================================
# INICIO
# ============================================================

if __name__ == "__main__":

    main()
