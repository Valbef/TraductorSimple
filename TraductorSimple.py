# ============================================================
# TRADUCTOR OFFLINE
# Español <-> Inglés
#
# Diccionario base:
#     traducciones.py
#
# Diccionario personalizado:
#     traducciones_usuario.py
#
# Este archivo contiene el MOTOR del traductor.
#
# Compatible con:
#     Windows
#     Linux
#     Termux
#
# Sin conexión a Internet.
# Sin librerías externas de Python.
#
# ============================================================
#
# COMANDOS:
#
#     L + Enter  -> Cambiar idiomas
#     G + Enter  -> Guardar traducción personalizada
#     B + Enter  -> Borrar traducción personalizada
#     V + Enter  -> Ver traducciones personalizadas
#     C + Enter  -> Copiar traducción
#     Enter      -> Siguiente
#     Ctrl+C     -> Salir
#
# ============================================================
#
# REGLAS:
#
#     - Ignora mayúsculas/minúsculas.
#     - NO ignora acentos.
#     - Las traducciones personalizadas tienen prioridad.
#     - Las frases largas tienen prioridad sobre palabras.
#     - Se conservan espacios y puntuación.
#     - Se reconocen preguntas con:
#
#           ¿pregunta?
#           pregunta?
#           ¿pregunta
#
#       cuando la estructura permite identificarla.
#
# ============================================================


import ast
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from traducciones import TRADUCCIONES


# ============================================================
# CONFIGURACIÓN
# ============================================================

IDIOMA_ORIGEN_INICIAL = "es"
IDIOMA_DESTINO_INICIAL = "en"

NOMBRE_ARCHIVO_USUARIO = "traducciones_usuario.py"

RUTA_ARCHIVO_USUARIO = (
    Path(__file__).resolve().parent
    / NOMBRE_ARCHIVO_USUARIO
)


# ============================================================
# DICCIONARIO PERSONALIZADO
# ============================================================

def crear_archivo_usuario():
    """
    Crea traducciones_usuario.py si todavía no existe.

    El usuario también puede editar este archivo
    manualmente.
    """

    if RUTA_ARCHIVO_USUARIO.exists():
        return

    contenido = '''# ============================================================
# TRADUCCIONES PERSONALIZADAS
#
# Este archivo es gestionado por TraductorSimple.py.
#
# También puedes editarlo manualmente.
#
# Formato:
#
# TRADUCCIONES_USUARIO = {
#
#     ("es", "en"): {
#         "tengo hambre": "I'm hungry",
#     },
#
#     ("en", "es"): {
#         "I'm hungry": "tengo hambre",
#     },
#
# }
#
# Los acentos se respetan.
# Las mayúsculas/minúsculas se ignoran durante la búsqueda.
# ============================================================

TRADUCCIONES_USUARIO = {

    ("es", "en"): {
    },

    ("en", "es"): {
    },

}
'''

    try:
        RUTA_ARCHIVO_USUARIO.write_text(
            contenido,
            encoding="utf-8"
        )

    except OSError as error:
        print()
        print(
            "Aviso: no se pudo crear "
            f"{NOMBRE_ARCHIVO_USUARIO}: {error}"
        )


def cargar_traducciones_usuario():
    """
    Carga de forma segura TRADUCCIONES_USUARIO.

    NO ejecuta el archivo.

    Utiliza ast.literal_eval() para leer solamente
    estructuras de datos de Python.
    """

    crear_archivo_usuario()

    if not RUTA_ARCHIVO_USUARIO.exists():
        return {}

    try:

        contenido = RUTA_ARCHIVO_USUARIO.read_text(
            encoding="utf-8"
        )

        arbol = ast.parse(
            contenido,
            filename=str(RUTA_ARCHIVO_USUARIO)
        )

        valor = None

        for nodo in arbol.body:

            if not isinstance(
                nodo,
                ast.Assign
            ):
                continue

            for objetivo in nodo.targets:

                if (
                    isinstance(
                        objetivo,
                        ast.Name
                    )
                    and objetivo.id
                    == "TRADUCCIONES_USUARIO"
                ):

                    valor = ast.literal_eval(
                        nodo.value
                    )

                    break

            if valor is not None:
                break

        if not isinstance(valor, dict):
            return {}

        resultado = {}

        for clave, diccionario in valor.items():

            if not (
                isinstance(clave, tuple)
                and len(clave) == 2
            ):
                continue

            idioma_origen = clave[0]
            idioma_destino = clave[1]

            if not (
                isinstance(
                    idioma_origen,
                    str
                )
                and isinstance(
                    idioma_destino,
                    str
                )
            ):
                continue

            if not isinstance(
                diccionario,
                dict
            ):
                continue

            resultado[
                (
                    idioma_origen,
                    idioma_destino
                )
            ] = {}

            for origen, destino in diccionario.items():

                if not (
                    isinstance(origen, str)
                    and isinstance(destino, str)
                ):
                    continue

                resultado[
                    (
                        idioma_origen,
                        idioma_destino
                    )
                ][origen] = destino

        return resultado

    except (
        SyntaxError,
        ValueError,
        TypeError,
        OSError
    ) as error:

        print()
        print(
            "Aviso: no se pudo leer "
            f"{NOMBRE_ARCHIVO_USUARIO}."
        )
        print(error)
        print()

        return {}


# ============================================================
# CARGAR TRADUCCIONES PERSONALIZADAS
# ============================================================

TRADUCCIONES_USUARIO = (
    cargar_traducciones_usuario()
)


# ============================================================
# GUARDAR DICCIONARIO PERSONALIZADO
# ============================================================

def guardar_traducciones_usuario(
    diccionario
):
    """
    Guarda el diccionario personalizado en:

        traducciones_usuario.py

    Utiliza un archivo temporal y os.replace()
    para reducir el riesgo de corrupción.
    """

    contenido = (
        "# ============================================================\n"
        "# TRADUCCIONES PERSONALIZADAS\n"
        "# Archivo gestionado por TraductorSimple.py\n"
        "# También puede editarse manualmente.\n"
        "# ============================================================\n\n"
        "TRADUCCIONES_USUARIO = "
        + repr(diccionario)
        + "\n"
    )

    ruta_temporal = None

    try:

        directorio = RUTA_ARCHIVO_USUARIO.parent

        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=directorio,
            prefix="traducciones_usuario_",
            suffix=".tmp",
            delete=False
        ) as archivo:

            archivo.write(contenido)

            archivo.flush()

            ruta_temporal = Path(
                archivo.name
            )

        os.replace(
            ruta_temporal,
            RUTA_ARCHIVO_USUARIO
        )

        return True

    except OSError as error:

        if (
            ruta_temporal is not None
            and ruta_temporal.exists()
        ):

            try:
                ruta_temporal.unlink()
            except OSError:
                pass

        print()
        print(
            "Error al guardar "
            f"{NOMBRE_ARCHIVO_USUARIO}:"
        )
        print(error)
        print()

        return False


# ============================================================
# NORMALIZACIÓN
# ============================================================

def normalizar(texto):
    """
    Limpia espacios innecesarios.

    NO elimina:
        - acentos
        - signos
        - palabras

    Solamente:
        - convierte a texto
        - elimina espacios exteriores
        - convierte varios espacios en uno
    """

    if texto is None:
        return ""

    texto = str(texto).strip()

    texto = re.sub(
        r"\s+",
        " ",
        texto
    )

    return texto


def normalizar_busqueda(texto):
    """
    Normalización para búsquedas.

    Ignora:
        - mayúsculas/minúsculas

    Conserva:
        - acentos
        - signos
    """

    return normalizar(texto).casefold()


# ============================================================
# NORMALIZAR FRASE PARA COMPARACIÓN
# ============================================================

def normalizar_frase_para_indice(texto):
    """
    Normaliza una frase para utilizarla en los índices
    de frases.

    La puntuación exterior se ignora para que:

        tengo hambre

    pueda coincidir dentro de:

        tengo hambre!

    """

    texto = normalizar(texto)

    if not texto:
        return ""

    texto = texto.casefold()

    # Quitar solamente puntuación de los extremos.

    texto = re.sub(
        r'^[¿¡"\'(),.!?;:]+',
        "",
        texto
    )

    texto = re.sub(
        r'[¿¡"\'(),.!?;:]+$',
        "",
        texto
    )

    return normalizar(texto)

# ============================================================
# LIMPIAR PANTALLA
# ============================================================

def limpiar_pantalla():
    """
    Limpia completamente la terminal.

    Compatible con:

        Windows
        Linux
        Termux
    """

    try:

        comando = (
            "cls"
            if os.name == "nt"
            else "clear"
        )

        os.system(comando)

    except Exception:
        pass


# ============================================================
# CREAR ÍNDICES
# ============================================================

def crear_indice(diccionario):
    """
    Crea un índice de búsqueda exacta.
    """

    indice = {}

    for origen, destino in diccionario.items():

        clave = normalizar_busqueda(
            origen
        )

        if not clave:
            continue

        indice[clave] = destino

    return indice


# ============================================================
# ÍNDICES BASE Y PERSONALIZADOS
# ============================================================

INDICES = {
    idiomas: crear_indice(diccionario)
    for idiomas, diccionario
    in TRADUCCIONES.items()
}


INDICES_USUARIO = {
    idiomas: crear_indice(diccionario)
    for idiomas, diccionario
    in TRADUCCIONES_USUARIO.items()
}


# ============================================================
# RECONSTRUIR ÍNDICES
# ============================================================

def reconstruir_indices():
    """
    Reconstruye los índices personalizados.
    """

    global INDICES_USUARIO

    INDICES_USUARIO = {
        idiomas: crear_indice(diccionario)
        for idiomas, diccionario
        in TRADUCCIONES_USUARIO.items()
    }


# ============================================================
# BÚSQUEDA EXACTA
# ============================================================

def buscar_exacta(
    texto,
    idioma_origen,
    idioma_destino
):
    """
    Busca una frase completa.

    Personalizadas:
        PRIORIDAD 1

    Base:
        PRIORIDAD 2
    """

    clave = (
        idioma_origen,
        idioma_destino
    )

    texto_normalizado = (
        normalizar_busqueda(texto)
    )

    indice_usuario = (
        INDICES_USUARIO.get(clave)
    )

    if indice_usuario:

        resultado = indice_usuario.get(
            texto_normalizado
        )

        if resultado is not None:
            return resultado

    indice = INDICES.get(clave)

    if indice:

        resultado = indice.get(
            texto_normalizado
        )

        if resultado is not None:
            return resultado

    return None


# ============================================================
# DETECTAR PREGUNTAS
# ============================================================

def es_pregunta(texto):
    """
    Detecta preguntas tanto con:

        ¿pregunta?

    como:

        pregunta?

    También reconoce:

        ¿pregunta

    cuando empieza con el signo de apertura.

    """

    texto = normalizar(texto)

    if not texto:
        return False

    return (
        texto.startswith("¿")
        or texto.endswith("?")
    )


# ============================================================
# QUITAR SIGNOS DE PREGUNTA EXTERIORES
# ============================================================

def limpiar_marcadores_pregunta(texto):
    """
    Elimina únicamente los signos de pregunta
    exteriores para facilitar el análisis.

    Ejemplos:

        ¿dónde estás?
        dónde estás?

    se convierten internamente en:

        dónde estás

    """

    texto = normalizar(texto)

    if texto.startswith("¿"):
        texto = texto[1:].lstrip()

    if texto.endswith("?"):
        texto = texto[:-1].rstrip()

    return texto


# ============================================================
# AÑADIR FORMATO DE PREGUNTA
# ============================================================

def formatear_pregunta(
    traduccion,
    idioma_destino
):
    """
    Añade el formato de pregunta apropiado.

    Español:
        ¿ ... ?

    Inglés:
        ... ?

    """

    traduccion = normalizar(traduccion)

    if not traduccion:
        return traduccion

    # Eliminar posibles signos existentes.

    traduccion = re.sub(
        r'^[¿¡]+',
        "",
        traduccion
    )

    traduccion = re.sub(
        r'[?]+$',
        "",
        traduccion
    )

    traduccion = traduccion.strip()

    if idioma_destino == "es":
        return f"¿{traduccion}?"

    return f"{traduccion}?"


# ============================================================
# TRADUCCIÓN INTERNA DE UNA PARTE
# ============================================================

def traducir_parte(
    texto,
    idioma_origen,
    idioma_destino
):
    """
    Intenta traducir una parte mediante coincidencia exacta.
    """

    texto = normalizar(texto)

    if not texto:
        return None

    resultado = buscar_exacta(
        texto,
        idioma_origen,
        idioma_destino
    )

    if resultado is not None:
        return resultado

    return None


# ============================================================
# REGLAS ESPECIALES
# ============================================================

def reglas_especiales(
    texto,
    idioma_origen,
    idioma_destino
):
    """
    Reglas contextuales para preguntas frecuentes.

    IMPORTANTE:

    Se analiza tanto:

        ¿pregunta?

    como:

        pregunta?

    """

    texto_limpio = normalizar(texto)

    if not texto_limpio:
        return None

    pregunta = es_pregunta(
        texto_limpio
    )

    texto_sin_pregunta = (
        limpiar_marcadores_pregunta(
            texto_limpio
        )
        if pregunta
        else texto_limpio
    )

    texto_cf = (
        texto_sin_pregunta.casefold()
    )

    # ========================================================
    # ESPAÑOL -> INGLÉS
    # ========================================================

    if (
        idioma_origen == "es"
        and idioma_destino == "en"
        and pregunta
    ):

        # ----------------------------------------------------
        # CÓMO ESTÁS
        # ----------------------------------------------------

        if re.fullmatch(
            r"cómo estás",
            texto_cf
        ):
            return "how are you?"

        # ----------------------------------------------------
        # CÓMO ESTÁ ...
        # ----------------------------------------------------

        coincidencia = re.fullmatch(
            r"cómo está (.+)",
            texto_cf
        )

        if coincidencia:

            resto = coincidencia.group(1)

            traduccion = traducir_parte(
                resto,
                "es",
                "en"
            )

            if traduccion is not None:

                return (
                    f"how is "
                    f"{traduccion}?"
                )

        # ----------------------------------------------------
        # CÓMO ESTÁN ...
        # ----------------------------------------------------

        coincidencia = re.fullmatch(
            r"cómo están (.+)",
            texto_cf
        )

        if coincidencia:

            resto = coincidencia.group(1)

            traduccion = traducir_parte(
                resto,
                "es",
                "en"
            )

            if traduccion is not None:

                return (
                    f"how are "
                    f"{traduccion}?"
                )

        # ----------------------------------------------------
        # QUÉ QUIERES
        # ----------------------------------------------------

        coincidencia = re.fullmatch(
            r"qué quieres(?: (.+))?",
            texto_cf
        )

        if coincidencia:

            resto = coincidencia.group(1)

            if resto:

                traduccion = traducir_parte(
                    resto,
                    "es",
                    "en"
                )

                if traduccion is not None:

                    return (
                        f"what do you want "
                        f"{traduccion}?"
                    )

            return "what do you want?"

        # ----------------------------------------------------
        # QUÉ NECESITAS
        # ----------------------------------------------------

        coincidencia = re.fullmatch(
            r"qué necesitas(?: (.+))?",
            texto_cf
        )

        if coincidencia:

            resto = coincidencia.group(1)

            if resto:

                traduccion = traducir_parte(
                    resto,
                    "es",
                    "en"
                )

                if traduccion is not None:

                    return (
                        f"what do you need "
                        f"{traduccion}?"
                    )

            return "what do you need?"

        # ----------------------------------------------------
        # QUÉ ES
        # ----------------------------------------------------

        coincidencia = re.fullmatch(
            r"qué es (.+)",
            texto_cf
        )

        if coincidencia:

            resto = coincidencia.group(1)

            traduccion = traducir_parte(
                resto,
                "es",
                "en"
            )

            if traduccion is not None:

                return (
                    f"what is "
                    f"{traduccion}?"
                )

        # ----------------------------------------------------
        # QUÉ SON
        # ----------------------------------------------------

        coincidencia = re.fullmatch(
            r"qué son (.+)",
            texto_cf
        )

        if coincidencia:

            resto = coincidencia.group(1)

            traduccion = traducir_parte(
                resto,
                "es",
                "en"
            )

            if traduccion is not None:

                return (
                    f"what are "
                    f"{traduccion}?"
                )

        # ----------------------------------------------------
        # DÓNDE ESTÁ
        # ----------------------------------------------------

        coincidencia = re.fullmatch(
            r"dónde está (.+)",
            texto_cf
        )

        if coincidencia:

            resto = coincidencia.group(1)

            traduccion = traducir_parte(
                resto,
                "es",
                "en"
            )

            if traduccion is not None:

                return (
                    f"where is "
                    f"{traduccion}?"
                )

        # ----------------------------------------------------
        # DÓNDE ESTÁN
        # ----------------------------------------------------

        coincidencia = re.fullmatch(
            r"dónde están (.+)",
            texto_cf
        )

        if coincidencia:

            resto = coincidencia.group(1)

            traduccion = traducir_parte(
                resto,
                "es",
                "en"
            )

            if traduccion is not None:

                return (
                    f"where are "
                    f"{traduccion}?"
                )

        # ----------------------------------------------------
        # DÓNDE
        # ----------------------------------------------------

        coincidencia = re.fullmatch(
            r"dónde (.+)",
            texto_cf
        )

        if coincidencia:

            resto = coincidencia.group(1)

            traduccion = traducir_parte(
                resto,
                "es",
                "en"
            )

            if traduccion is not None:

                return (
                    f"where "
                    f"{traduccion}?"
                )

        # ----------------------------------------------------
        # CUÁNDO
        # ----------------------------------------------------

        coincidencia = re.fullmatch(
            r"cuándo (.+)",
            texto_cf
        )

        if coincidencia:

            resto = coincidencia.group(1)

            traduccion = traducir_parte(
                resto,
                "es",
                "en"
            )

            if traduccion is not None:

                return (
                    f"when "
                    f"{traduccion}?"
                )

        # ----------------------------------------------------
        # POR QUÉ
        # ----------------------------------------------------

        coincidencia = re.fullmatch(
            r"por qué (.+)",
            texto_cf
        )

        if coincidencia:

            resto = coincidencia.group(1)

            traduccion = traducir_parte(
                resto,
                "es",
                "en"
            )

            if traduccion is not None:

                return (
                    f"why "
                    f"{traduccion}?"
                )

        # ----------------------------------------------------
        # CANTIDADES
        # ----------------------------------------------------

        patrones_cantidad = [
            (
                r"cuánto (.+)",
                "how much"
            ),
            (
                r"cuánta (.+)",
                "how much"
            ),
            (
                r"cuántos (.+)",
                "how many"
            ),
            (
                r"cuántas (.+)",
                "how many"
            ),
        ]

        for patron, comienzo in (
            patrones_cantidad
        ):

            coincidencia = re.fullmatch(
                patron,
                texto_cf
            )

            if not coincidencia:
                continue

            resto = coincidencia.group(1)

            traduccion = traducir_parte(
                resto,
                "es",
                "en"
            )

            if traduccion is not None:

                return (
                    f"{comienzo} "
                    f"{traduccion}?"
                )

        # ----------------------------------------------------
        # QUÉ ...
        # ----------------------------------------------------

        coincidencia = re.fullmatch(
            r"qué (.+)",
            texto_cf
        )

        if coincidencia:

            resto = coincidencia.group(1)

            traduccion = traducir_parte(
                resto,
                "es",
                "en"
            )

            if traduccion is not None:

                return (
                    f"what "
                    f"{traduccion}?"
                )

    # ========================================================
    # INGLÉS -> ESPAÑOL
    # ========================================================

    if (
        idioma_origen == "en"
        and idioma_destino == "es"
        and pregunta
    ):

        # ----------------------------------------------------
        # HOW ARE YOU
        # ----------------------------------------------------

        if re.fullmatch(
            r"how are you",
            texto_cf
        ):
            return "¿cómo estás?"

        # ----------------------------------------------------
        # HOW IS ...
        # ----------------------------------------------------

        coincidencia = re.fullmatch(
            r"how is (.+)",
            texto_cf
        )

        if coincidencia:

            resto = coincidencia.group(1)

            traduccion = traducir_parte(
                resto,
                "en",
                "es"
            )

            if traduccion is not None:

                return (
                    f"¿cómo está "
                    f"{traduccion}?"
                )

        # ----------------------------------------------------
        # HOW ARE ...
        # ----------------------------------------------------

        coincidencia = re.fullmatch(
            r"how are (.+)",
            texto_cf
        )

        if coincidencia:

            resto = coincidencia.group(1)

            traduccion = traducir_parte(
                resto,
                "en",
                "es"
            )

            if traduccion is not None:

                return (
                    f"¿cómo están "
                    f"{traduccion}?"
                )

        # ----------------------------------------------------
        # WHAT IS ...
        # ----------------------------------------------------

        coincidencia = re.fullmatch(
            r"what is (.+)",
            texto_cf
        )

        if coincidencia:

            resto = coincidencia.group(1)

            traduccion = traducir_parte(
                resto,
                "en",
                "es"
            )

            if traduccion is not None:

                return (
                    f"¿qué es "
                    f"{traduccion}?"
                )

        # ----------------------------------------------------
        # WHAT ARE ...
        # ----------------------------------------------------

        coincidencia = re.fullmatch(
            r"what are (.+)",
            texto_cf
        )

        if coincidencia:

            resto = coincidencia.group(1)

            traduccion = traducir_parte(
                resto,
                "en",
                "es"
            )

            if traduccion is not None:

                return (
                    f"¿qué son "
                    f"{traduccion}?"
                )

        # ----------------------------------------------------
        # WHERE IS ...
        # ----------------------------------------------------

        coincidencia = re.fullmatch(
            r"where is (.+)",
            texto_cf
        )

        if coincidencia:

            resto = coincidencia.group(1)

            traduccion = traducir_parte(
                resto,
                "en",
                "es"
            )

            if traduccion is not None:

                return (
                    f"¿dónde está "
                    f"{traduccion}?"
                )

        # ----------------------------------------------------
        # WHERE ARE ...
        # ----------------------------------------------------

        coincidencia = re.fullmatch(
            r"where are (.+)",
            texto_cf
        )

        if coincidencia:

            resto = coincidencia.group(1)

            traduccion = traducir_parte(
                resto,
                "en",
                "es"
            )

            if traduccion is not None:

                return (
                    f"¿dónde están "
                    f"{traduccion}?"
                )

        # ----------------------------------------------------
        # WHAT DO YOU WANT
        # ----------------------------------------------------

        coincidencia = re.fullmatch(
            r"what do you want(?: (.+))?",
            texto_cf
        )

        if coincidencia:

            resto = coincidencia.group(1)

            if resto:

                traduccion = traducir_parte(
                    resto,
                    "en",
                    "es"
                )

                if traduccion is not None:

                    return (
                        f"¿qué quieres "
                        f"{traduccion}?"
                    )

            return "¿qué quieres?"

        # ----------------------------------------------------
        # WHAT DO YOU NEED
        # ----------------------------------------------------

        coincidencia = re.fullmatch(
            r"what do you need(?: (.+))?",
            texto_cf
        )

        if coincidencia:

            resto = coincidencia.group(1)

            if resto:

                traduccion = traducir_parte(
                    resto,
                    "en",
                    "es"
                )

                if traduccion is not None:

                    return (
                        f"¿qué necesitas "
                        f"{traduccion}?"
                    )

            return "¿qué necesitas?"

        # ----------------------------------------------------
        # WHAT ...
        # ----------------------------------------------------

        coincidencia = re.fullmatch(
            r"what (.+)",
            texto_cf
        )

        if coincidencia:

            resto = coincidencia.group(1)

            traduccion = traducir_parte(
                resto,
                "en",
                "es"
            )

            if traduccion is not None:

                return (
                    f"¿qué "
                    f"{traduccion}?"
                )

    return None


# ============================================================
# SEPARAR PUNTUACIÓN
# ============================================================

PATRON_PUNTUACION = re.compile(
    r'^([¿¡"\'(),.!?;:]*)(.*?)([¿¡"\'(),.!?;:]*)$'
)


def separar_puntuacion(palabra):
    """
    Separa:

        puntuación inicial
        cuerpo
        puntuación final
    """

    coincidencia = (
        PATRON_PUNTUACION.match(
            palabra
        )
    )

    if not coincidencia:
        return "", palabra, ""

    return (
        coincidencia.group(1),
        coincidencia.group(2),
        coincidencia.group(3)
    )


# ============================================================
# TOKENIZACIÓN
# ============================================================

PATRON_TOKENS = re.compile(
    r'\s+'
    r'|[¿¡"\'(),.!?;:]+'
    r'|[^\s¿¡"\'(),.!?;:]+'
)


def tokenizar_texto(texto):
    """
    Divide el texto conservando:

        - palabras
        - espacios
        - puntuación
    """

    return PATRON_TOKENS.findall(
        texto
    )


def es_token_palabra(token):
    """
    Determina si un token puede formar parte
    de una frase traducible.
    """

    if not token:
        return False

    if token.isspace():
        return False

    if re.fullmatch(
        r'[¿¡"\'(),.!?;:]+',
        token
    ):
        return False

    return True


# ============================================================
# CREAR ÍNDICE DE FRASES
# ============================================================

def crear_indice_frases(diccionario):
    """
    Crea un índice basado en tuplas de palabras.

    Ejemplo:

        "tengo hambre"

    se convierte en:

        ("tengo", "hambre")

    """

    indice = {}

    for origen, destino in diccionario.items():

        origen_normalizado = (
            normalizar_frase_para_indice(
                origen
            )
        )

        if not origen_normalizado:
            continue

        tokens = origen_normalizado.split()

        if not tokens:
            continue

        tokens_cf = tuple(
            token.casefold()
            for token in tokens
        )

        indice[tokens_cf] = {
            "traduccion": destino,
            "texto_original": origen,
            "cantidad": len(tokens_cf)
        }

    return indice


# ============================================================
# ÍNDICES DE FRASES
# ============================================================

INDICES_FRASES = {}

INDICES_FRASES_USUARIO = {}


def reconstruir_indices_frases():
    """
    Reconstruye los índices de frases.
    """

    global INDICES_FRASES
    global INDICES_FRASES_USUARIO

    INDICES_FRASES = {
        idiomas: crear_indice_frases(
            diccionario
        )
        for idiomas, diccionario
        in TRADUCCIONES.items()
    }

    INDICES_FRASES_USUARIO = {
        idiomas: crear_indice_frases(
            diccionario
        )
        for idiomas, diccionario
        in TRADUCCIONES_USUARIO.items()
    }


reconstruir_indices_frases()


# ============================================================
# OBTENER PALABRAS CONSECUTIVAS
# ============================================================

def obtener_palabras_desde(
    tokens,
    posicion
):
    """
    Obtiene palabras consecutivas a partir de una posición.

    No atraviesa signos de puntuación.

    Devuelve:

        palabras
        índices_consumidos
    """

    palabras = []

    indices = []

    indice = posicion

    while indice < len(tokens):

        token = tokens[indice]

        if not es_token_palabra(token):
            break

        palabras.append(
            token.casefold()
        )

        indices.append(
            indice
        )

        indice += 1

        if indice >= len(tokens):
            break

        if not tokens[indice].isspace():
            break

        indice += 1

    return (
        palabras,
        indices
    )


# ============================================================
# BUSCAR FRASE PARCIAL MÁS LARGA
# ============================================================

def buscar_frase_parcial(
    tokens,
    posicion,
    idioma_origen,
    idioma_destino
):
    """
    Busca la coincidencia más larga posible.

    EJEMPLO:

        tengo hambre

    Si existen:

        tengo -> I have

        tengo hambre -> I'm hungry

    devuelve:

        tengo hambre -> I'm hungry

    y NO:

        tengo -> I have
        hambre -> hungry

    ------------------------------------------------------------

    PRIORIDAD:

        1. Personalizada más larga
        2. Base más larga

    Es decir:

        personalizada de 2 palabras

    gana a:

        base de 2 palabras

    y cualquier coincidencia más corta.
    """

    clave = (
        idioma_origen,
        idioma_destino
    )

    (
        palabras,
        indices
    ) = obtener_palabras_desde(
        tokens,
        posicion
    )

    if not palabras:
        return None

    # ========================================================
    # PERSONALIZADAS
    # ========================================================

    indice_usuario = (
        INDICES_FRASES_USUARIO.get(
            clave,
            {}
        )
    )

    mejor_usuario = None

    for cantidad in range(
        len(palabras),
        0,
        -1
    ):

        candidato = tuple(
            palabras[:cantidad]
        )

        entrada = indice_usuario.get(
            candidato
        )

        if entrada is not None:

            mejor_usuario = (
                cantidad,
                entrada["traduccion"]
            )

            break

    # ========================================================
    # BASE
    # ========================================================

    indice_base = (
        INDICES_FRASES.get(
            clave,
            {}
        )
    )

    mejor_base = None

    for cantidad in range(
        len(palabras),
        0,
        -1
    ):

        candidato = tuple(
            palabras[:cantidad]
        )

        entrada = indice_base.get(
            candidato
        )

        if entrada is not None:

            mejor_base = (
                cantidad,
                entrada["traduccion"]
            )

            break

    # ========================================================
    # COMPARAR RESULTADOS
    # ========================================================

    if mejor_usuario is None:
        return mejor_base

    if mejor_base is None:
        return mejor_usuario

    # Si tienen la misma longitud:
    # personalizada gana.

    if (
        mejor_usuario[0]
        >= mejor_base[0]
    ):
        return mejor_usuario

    return mejor_base


# ============================================================
# AVANZAR TOKENS
# ============================================================

def avanzar_palabras(
    tokens,
    posicion,
    cantidad
):
    """
    Avanza exactamente 'cantidad' palabras
    y los espacios que haya entre ellas.

    NO consume la puntuación siguiente.

    Esto es importante para conservar:

        tengo hambre!

    como:

        I'm hungry!
    """

    palabras = 0

    indice = posicion

    while (
        indice < len(tokens)
        and palabras < cantidad
    ):

        token = tokens[indice]

        if es_token_palabra(token):

            palabras += 1

            indice += 1

            if palabras >= cantidad:
                break

            if (
                indice < len(tokens)
                and tokens[indice].isspace()
            ):

                indice += 1

                continue

            continue

        indice += 1

    return indice


# ============================================================
# TRADUCIR FRASES PARCIALES
# ============================================================

def traducir_frases_parciales(
    texto,
    idioma_origen,
    idioma_destino
):
    """
    Traduce frases dentro de un texto.

    Características:

        - Mayor coincidencia gana.
        - Personalizadas tienen prioridad.
        - Se conserva la puntuación.
        - Se conservan los espacios.
        - No se mezclan palabras de una frase larga.
          cuando existe una traducción completa.
    """

    tokens = tokenizar_texto(
        texto
    )

    if not tokens:
        return None

    resultado = []

    posicion = 0

    hubo_traduccion = False

    while posicion < len(tokens):

        token = tokens[posicion]

        # ====================================================
        # ESPACIOS
        # ====================================================

        if token.isspace():

            resultado.append(token)

            posicion += 1

            continue

        # ====================================================
        # PUNTUACIÓN
        # ====================================================

        if not es_token_palabra(token):

            resultado.append(token)

            posicion += 1

            continue

        # ====================================================
        # FRASE MÁS LARGA
        # ====================================================

        coincidencia = buscar_frase_parcial(
            tokens,
            posicion,
            idioma_origen,
            idioma_destino
        )

        if coincidencia is not None:

            cantidad, traduccion = (
                coincidencia
            )

            resultado.append(
                traduccion
            )

            hubo_traduccion = True

            posicion = avanzar_palabras(
                tokens,
                posicion,
                cantidad
            )

            continue

        # ====================================================
        # PALABRA INDIVIDUAL
        # ====================================================

        traduccion = buscar_palabra_en_direccion(
            token,
            idioma_origen,
            idioma_destino
        )

        if traduccion is not None:

            resultado.append(
                traduccion
            )

            hubo_traduccion = True

        else:

            resultado.append(
                token
            )

        posicion += 1

    if not hubo_traduccion:
        return None

    return "".join(resultado)


# ============================================================
# BUSCAR PALABRA
# ============================================================

def buscar_palabra(
    palabra,
    diccionario
):
    """
    Busca una palabra ignorando mayúsculas/minúsculas.

    Los acentos se conservan.
    """

    if palabra in diccionario:
        return diccionario[palabra]

    palabra_cf = palabra.casefold()

    for origen, destino in (
        diccionario.items()
    ):

        if (
            origen.casefold()
            == palabra_cf
        ):
            return destino

    return None


def buscar_palabra_en_direccion(
    palabra,
    idioma_origen,
    idioma_destino
):
    """
    Busca primero en personalizadas y después
    en el diccionario base.
    """

    clave = (
        idioma_origen,
        idioma_destino
    )

    diccionario_usuario = (
        TRADUCCIONES_USUARIO.get(
            clave,
            {}
        )
    )

    resultado = buscar_palabra(
        palabra,
        diccionario_usuario
    )

    if resultado is not None:
        return resultado

    diccionario_base = (
        TRADUCCIONES.get(
            clave,
            {}
        )
    )

    resultado = buscar_palabra(
        palabra,
        diccionario_base
    )

    return resultado


# ============================================================
# TRADUCCIÓN PALABRA POR PALABRA
# ============================================================

def traducir_palabras(
    texto,
    idioma_origen,
    idioma_destino
):
    """
    Último recurso.

    Traduce palabras individuales.

    Las palabras desconocidas se conservan.
    """

    if not normalizar(texto):
        return None

    tokens = tokenizar_texto(
        texto
    )

    if not tokens:
        return None

    resultado = []

    hubo_traduccion = False

    for token in tokens:

        if (
            token.isspace()
            or not es_token_palabra(token)
        ):

            resultado.append(token)

            continue

        traduccion = buscar_palabra_en_direccion(
            token,
            idioma_origen,
            idioma_destino
        )

        if traduccion is None:

            resultado.append(
                token
            )

            continue

        resultado.append(
            traduccion
        )

        hubo_traduccion = True

    if not hubo_traduccion:
        return None

    return "".join(resultado)


# ============================================================
# FUNCIÓN PRINCIPAL DE TRADUCCIÓN
# ============================================================

def traducir(
    texto,
    idioma_origen,
    idioma_destino
):
    """
    Motor principal.

    Orden:

        1. Frase exacta personalizada
        2. Frase exacta base
        3. Reglas contextuales
        4. Frases parciales más largas
        5. Palabras individuales
        6. Texto original

    """

    texto = normalizar(texto)

    if not texto:
        return ""

    clave = (
        idioma_origen,
        idioma_destino
    )

    if (
        clave not in TRADUCCIONES
        and clave not in TRADUCCIONES_USUARIO
    ):
        return texto

    # ========================================================
    # 1. FRASE EXACTA
    # ========================================================

    resultado = buscar_exacta(
        texto,
        idioma_origen,
        idioma_destino
    )

    if resultado is not None:

        # Si el usuario escribió una pregunta
        # y la traducción personalizada/base no
        # incluye signos, se conserva la traducción
        # tal como está definida.
        return resultado

    # ========================================================
    # 2. REGLAS CONTEXTUALES
    # ========================================================

    resultado = reglas_especiales(
        texto,
        idioma_origen,
        idioma_destino
    )

    if resultado is not None:
        return resultado

    # ========================================================
    # 3. FRASES PARCIALES
    # ========================================================

    resultado = traducir_frases_parciales(
        texto,
        idioma_origen,
        idioma_destino
    )

    if resultado is not None:

        # Si era una pregunta y el resultado no termina
        # en ?, añadimos el signo correspondiente.

        if es_pregunta(texto):

            if not resultado.endswith("?"):

                resultado = formatear_pregunta(
                    resultado,
                    idioma_destino
                )

        return resultado

    # ========================================================
    # 4. PALABRAS INDIVIDUALES
    # ========================================================

    resultado = traducir_palabras(
        texto,
        idioma_origen,
        idioma_destino
    )

    if resultado is not None:

        if es_pregunta(texto):

            if not resultado.endswith("?"):

                resultado = formatear_pregunta(
                    resultado,
                    idioma_destino
                )

        return resultado

    # ========================================================
    # 5. DESCONOCIDO
    # ========================================================

    return texto


# ============================================================
# GESTIÓN DE TRADUCCIONES PERSONALIZADAS
# ============================================================

def guardar_traduccion_personalizada(
    texto_origen,
    texto_destino,
    idioma_origen,
    idioma_destino
):
    """
    Añade o reemplaza una traducción personalizada.
    """

    texto_origen = normalizar(
        texto_origen
    )

    texto_destino = normalizar(
        texto_destino
    )

    if not texto_origen:
        return False

    if not texto_destino:
        return False

    clave = (
        idioma_origen,
        idioma_destino
    )

    if clave not in TRADUCCIONES_USUARIO:

        TRADUCCIONES_USUARIO[
            clave
        ] = {}

    # ========================================================
    # Buscar clave existente respetando casefold()
    # ========================================================

    clave_existente = None

    objetivo = normalizar_busqueda(
        texto_origen
    )

    for origen in (
        TRADUCCIONES_USUARIO[
            clave
        ].keys()
    ):

        if (
            normalizar_busqueda(
                origen
            )
            == objetivo
        ):

            clave_existente = origen

            break

    if clave_existente is not None:

        del TRADUCCIONES_USUARIO[
            clave
        ][clave_existente]

    TRADUCCIONES_USUARIO[
        clave
    ][texto_origen] = (
        texto_destino
    )

    if not guardar_traducciones_usuario(
        TRADUCCIONES_USUARIO
    ):

        return False

    reconstruir_indices()

    reconstruir_indices_frases()

    return True


def borrar_traduccion_personalizada(
    texto_origen,
    idioma_origen,
    idioma_destino
):
    """
    Borra una traducción personalizada.

    La búsqueda ignora mayúsculas/minúsculas
    pero conserva la sensibilidad a los acentos.
    """

    clave = (
        idioma_origen,
        idioma_destino
    )

    diccionario = (
        TRADUCCIONES_USUARIO.get(
            clave
        )
    )

    if not diccionario:
        return False

    objetivo = normalizar_busqueda(
        texto_origen
    )

    encontrada = None

    for origen in diccionario:

        if (
            normalizar_busqueda(
                origen
            )
            == objetivo
        ):

            encontrada = origen

            break

    if encontrada is None:
        return False

    del diccionario[
        encontrada
    ]

    if not diccionario:

        del TRADUCCIONES_USUARIO[
            clave
        ]

    if not guardar_traducciones_usuario(
        TRADUCCIONES_USUARIO
    ):

        return False

    reconstruir_indices()

    reconstruir_indices_frases()

    return True


# ============================================================
# MOSTRAR TRADUCCIONES PERSONALIZADAS
# ============================================================

def mostrar_traducciones_usuario(
    idioma_origen=None,
    idioma_destino=None
):
    """
    Muestra las traducciones personalizadas.

    Si se indican idiomas, muestra únicamente esa dirección.
    """

    print()
    print("=" * 50)
    print("          TRADUCCIONES PERSONALIZADAS")
    print("=" * 50)
    print()

    if (
        idioma_origen is not None
        and idioma_destino is not None
    ):

        claves = [
            (
                idioma_origen,
                idioma_destino
            )
        ]

    else:

        claves = list(
            TRADUCCIONES_USUARIO.keys()
        )

    total = 0

    for clave in claves:

        diccionario = (
            TRADUCCIONES_USUARIO.get(
                clave,
                {}
            )
        )

        if not diccionario:
            continue

        origen, destino = clave

        print(
            f"{origen.upper()} → "
            f"{destino.upper()}"
        )

        print("-" * 50)

        for texto, traduccion in (
            diccionario.items()
        ):

            print(
                f"  {texto}  →  "
                f"{traduccion}"
            )

            total += 1

        print()

    if total == 0:

        print(
            "No hay traducciones "
            "personalizadas guardadas."
        )

    print("=" * 50)
    print()


# ============================================================
# PORTAPAPELES
# ============================================================

def copiar_portapapeles(texto):
    """
    Intenta copiar texto al portapapeles.

    Windows:
        clip

    Termux:
        termux-clipboard-set

    Linux:
        wl-copy
        xclip
        xsel
    """

    if not texto:
        return False

    # ========================================================
    # WINDOWS
    # ========================================================

    if shutil.which("clip"):

        try:

            proceso = subprocess.Popen(
                ["clip"],
                stdin=subprocess.PIPE,
                text=True
            )

            proceso.communicate(texto)

            return (
                proceso.returncode == 0
            )

        except Exception:
            pass

    # ========================================================
    # TERMUX
    # ========================================================

    if shutil.which(
        "termux-clipboard-set"
    ):

        try:

            proceso = subprocess.Popen(
                [
                    "termux-clipboard-set"
                ],
                stdin=subprocess.PIPE,
                text=True
            )

            proceso.communicate(texto)

            return (
                proceso.returncode == 0
            )

        except Exception:
            pass

    # ========================================================
    # LINUX / WAYLAND
    # ========================================================

    if shutil.which("wl-copy"):

        try:

            proceso = subprocess.Popen(
                ["wl-copy"],
                stdin=subprocess.PIPE,
                text=True
            )

            proceso.communicate(texto)

            return (
                proceso.returncode == 0
            )

        except Exception:
            pass

    # ========================================================
    # LINUX / XCLIP
    # ========================================================

    if shutil.which("xclip"):

        try:

            proceso = subprocess.Popen(
                [
                    "xclip",
                    "-selection",
                    "clipboard"
                ],
                stdin=subprocess.PIPE,
                text=True
            )

            proceso.communicate(texto)

            return (
                proceso.returncode == 0
            )

        except Exception:
            pass

    # ========================================================
    # LINUX / XSEL
    # ========================================================

    if shutil.which("xsel"):

        try:

            proceso = subprocess.Popen(
                [
                    "xsel",
                    "--clipboard",
                    "--input"
                ],
                stdin=subprocess.PIPE,
                text=True
            )

            proceso.communicate(texto)

            return (
                proceso.returncode == 0
            )

        except Exception:
            pass

    return False


# ============================================================
# MENÚ
# ============================================================

def mostrar_menu(
    idioma_origen,
    idioma_destino
):

    print()
    print("=" * 50)
    print("                    TRADUCTOR")
    print("=" * 50)
    print()

    print(
        f"              {idioma_origen.upper()} → "
        f"{idioma_destino.upper()}"
    )

    print()
    print("  L + Enter  →  Cambiar idiomas")
    print("  G + Enter  →  Guardar traducción")
    print("  B + Enter  →  Borrar traducción")
    print("  V + Enter  →  Ver traducciones")
    print("  C + Enter  →  Copiar traducción")
    print("  Enter      →  Siguiente")
    print("  Q + Enter  →  Salir")
    print()
    print("-" * 50)


# ============================================================
# COMANDO G
# ============================================================

def comando_guardar(
    idioma_origen,
    idioma_destino
):
    """
    Permite guardar manualmente una traducción.

    G + Enter
    """

    print()
    print("=" * 50)
    print("       GUARDAR TRADUCCIÓN PERSONALIZADA")
    print("=" * 50)
    print()

    print(
        f"Dirección: "
        f"{idioma_origen.upper()} → "
        f"{idioma_destino.upper()}"
    )

    print()

    try:

        origen = input(
            "Frase o palabra original: "
        )

        if not origen.strip():

            print()
            print(
                "No se ha introducido "
                "ninguna frase."
            )

            return

        destino = input(
            "Traducción personalizada: "
        )

        if not destino.strip():

            print()
            print(
                "No se ha introducido "
                "ninguna traducción."
            )

            return

        origen = normalizar(
            origen
        )

        destino = normalizar(
            destino
        )

        # ====================================================
        # Comprobar traducción personalizada existente
        # ====================================================

        diccionario = (
            TRADUCCIONES_USUARIO.get(
                (
                    idioma_origen,
                    idioma_destino
                ),
                {}
            )
        )

        encontrada = None

        objetivo = normalizar_busqueda(
            origen
        )

        for clave in diccionario:

            if (
                normalizar_busqueda(
                    clave
                )
                == objetivo
            ):

                encontrada = clave

                break

        if encontrada is not None:

            anterior = diccionario[
                encontrada
            ]

            print()
            print(
                "Ya existe una traducción "
                "personalizada para esa frase."
            )

            print(
                f"Actual: {anterior}"
            )

            print()

            confirmar = input(
                "¿Reemplazarla? [S/N]: "
            )

            if (
                confirmar.strip().casefold()
                not in (
                    "s",
                    "si",
                    "sí"
                )
            ):

                print()
                print(
                    "Operación cancelada."
                )

                return

        # ====================================================
        # Guardar
        # ====================================================

        if guardar_traduccion_personalizada(
            origen,
            destino,
            idioma_origen,
            idioma_destino
        ):

            print()
            print(
                "✓ Traducción personalizada "
                "guardada correctamente."
            )

            print()
            print(
                f"{origen}  →  {destino}"
            )

        else:

            print()
            print(
                "No se pudo guardar "
                "la traducción."
            )

    except EOFError:

        print()
        print(
            "Operación cancelada."
        )

    return



# ============================================================
# COMANDO B
# ============================================================

def comando_borrar(
    idioma_origen,
    idioma_destino
):
    """
    Permite borrar una traducción personalizada.
    """

    print()
    print("=" * 50)
    print("       BORRAR TRADUCCIÓN PERSONALIZADA")
    print("=" * 50)
    print()

    print(
        f"Dirección: "
        f"{idioma_origen.upper()} → "
        f"{idioma_destino.upper()}"
    )

    print()

    try:

        origen = input(
            "Frase o palabra que quieres borrar: "
        )

        if not origen.strip():

            print()
            print(
                "No se ha introducido "
                "ninguna frase."
            )

            return

        diccionario = (
            TRADUCCIONES_USUARIO.get(
                (
                    idioma_origen,
                    idioma_destino
                ),
                {}
            )
        )

        encontrada = None
        traduccion = None

        objetivo = normalizar_busqueda(
            origen
        )

        for clave, valor in (
            diccionario.items()
        ):

            if (
                normalizar_busqueda(
                    clave
                )
                == objetivo
            ):

                encontrada = clave
                traduccion = valor

                break

        if encontrada is None:

            print()
            print(
                "No existe una traducción "
                "personalizada con ese texto."
            )

            return

        print()
        print(
            f"{encontrada}  →  "
            f"{traduccion}"
        )

        print()

        confirmar = input(
            "¿Borrar esta traducción? [S/N]: "
        )

        if (
            confirmar.strip().casefold()
            not in (
                "s",
                "si",
                "sí"
            )
        ):

            print()
            print(
                "Operación cancelada."
            )

            return

        if borrar_traduccion_personalizada(
            encontrada,
            idioma_origen,
            idioma_destino
        ):

            print()
            print(
                "✓ Traducción eliminada."
            )

        else:

            print()
            print(
                "No se pudo eliminar "
                "la traducción."
            )

    except (
        KeyboardInterrupt,
        EOFError
    ):

        print()
        print(
            "Operación cancelada."
        )


# ============================================================
# COMANDO V
# ============================================================

def comando_ver(
    idioma_origen,
    idioma_destino
):
    """
    Muestra las traducciones personalizadas
    del idioma actual.
    """

    mostrar_traducciones_usuario(
        idioma_origen,
        idioma_destino
    )

    try:

        input(
            "Pulsa Enter para continuar..."
        )

    except EOFError:

        pass



# ============================================================
# COMPROBAR SI EXISTE ALGUNA TRADUCCIÓN
# ============================================================

def tiene_traduccion(
    texto,
    idioma_origen,
    idioma_destino
):
    """
    Comprueba si existe alguna traducción para el texto.

    Se utiliza para distinguir entre:

        "texto desconocido"
        
    y:

        "texto traducido correctamente"

    Devuelve:

        True  -> se encontró alguna traducción
        False -> no se encontró ninguna
    """

    texto = normalizar(texto)

    if not texto:
        return False

    # --------------------------------------------------------
    # 1. FRASE EXACTA
    # --------------------------------------------------------

    resultado = buscar_exacta(
        texto,
        idioma_origen,
        idioma_destino
    )

    if resultado is not None:
        return True

    # --------------------------------------------------------
    # 2. REGLAS ESPECIALES
    # --------------------------------------------------------

    resultado = reglas_especiales(
        texto,
        idioma_origen,
        idioma_destino
    )

    if resultado is not None:
        return True

    # --------------------------------------------------------
    # 3. FRASES PARCIALES
    # --------------------------------------------------------

    resultado = traducir_frases_parciales(
        texto,
        idioma_origen,
        idioma_destino
    )

    if resultado is not None:
        return True

    # --------------------------------------------------------
    # 4. PALABRAS INDIVIDUALES
    # --------------------------------------------------------

    resultado = traducir_palabras(
        texto,
        idioma_origen,
        idioma_destino
    )

    if resultado is not None:
        return True

    return False


# ============================================================
# PREGUNTAR SI SE QUIERE GUARDAR UNA TRADUCCIÓN
# ============================================================

def preguntar_guardar_si_no_encontrada(
    texto,
    idioma_origen,
    idioma_destino
):
    """
    Pregunta al usuario si quiere introducir manualmente
    una traducción cuando no se ha encontrado ninguna.

    Si responde afirmativamente, permite introducirla
    directamente sin tener que utilizar G.
    """

    print()
    print("=" * 50)
    print("       TRADUCCIÓN NO ENCONTRADA")
    print("=" * 50)
    print()

    print(
        f"No se ha encontrado una traducción para:"
    )

    print()
    print(
        f'  "{texto}"'
    )

    print()

    try:

        respuesta = input(
            "¿Quieres introducir una "
            "traducción personalizada? [S/N]: "
        )

        if (
            respuesta.strip().casefold()
            not in ("s", "si", "sí")
        ):

            print()
            print(
                "No se ha guardado ninguna "
                "traducción."
            )

            return None

        print()

        traduccion = input(
            "Introduce la traducción: "
        )

        if not traduccion.strip():

            print()
            print(
                "No se ha introducido "
                "ninguna traducción."
            )

            return None

        traduccion = normalizar(
            traduccion
        )

        if guardar_traduccion_personalizada(
            texto,
            traduccion,
            idioma_origen,
            idioma_destino
        ):

            print()
            print(
                "✓ Traducción personalizada "
                "guardada correctamente."
            )

            print()
            print(
                f"{texto}  →  {traduccion}"
            )

            return traduccion

        print()
        print(
            "No se pudo guardar "
            "la traducción."
        )

        return None

    except (
        KeyboardInterrupt,
        EOFError
    ):

        print()
        print(
            "Operación cancelada."
        )

        return None



# ============================================================
# ESPERAR COMANDO DESPUÉS DE UNA TRADUCCIÓN
# ============================================================

def esperar_comando_traduccion(
    ultima_traduccion,
    idioma_origen,
    idioma_destino
):
    """
    Espera una acción después de mostrar una traducción.

    Enter -> siguiente
    C     -> copiar
    G     -> guardar
    B     -> borrar
    V     -> ver
    L     -> cambiar idioma
    Q     -> salir

    Devuelve:

        "continuar"
        "salir"
        "idiomas"
        "guardar"
        "borrar"
        "ver"
        "copiar"
    """

    while True:

        try:

            comando = input(
                "Comando (Enter = siguiente): "
            )

            comando = (
                comando.strip().casefold()
            )

            # ------------------------------------------------
            # ENTER -> SIGUIENTE
            # ------------------------------------------------

            if not comando:
                return "continuar"

            # ------------------------------------------------
            # Q -> SALIR
            # ------------------------------------------------

            if comando == "q":
                return "salir"

            # ------------------------------------------------
            # C -> COPIAR
            # ------------------------------------------------

            if comando == "c":

                if not ultima_traduccion:

                    print()
                    print(
                        "No hay ninguna traducción "
                        "para copiar."
                    )

                elif copiar_portapapeles(
                    ultima_traduccion
                ):

                    print()
                    print(
                        "✓ Traducción copiada "
                        "al portapapeles."
                    )

                else:

                    print()
                    print(
                        "No se pudo acceder al "
                        "portapapeles en este sistema."
                    )

                print()

                continue

            # ------------------------------------------------
            # G -> GUARDAR
            # ------------------------------------------------

            if comando == "g":

                comando_guardar(
                    idioma_origen,
                    idioma_destino
                )

                print()

                continue

            # ------------------------------------------------
            # B -> BORRAR
            # ------------------------------------------------

            if comando == "b":

                comando_borrar(
                    idioma_origen,
                    idioma_destino
                )

                print()

                continue

            # ------------------------------------------------
            # V -> VER
            # ------------------------------------------------

            if comando == "v":

                comando_ver(
                    idioma_origen,
                    idioma_destino
                )

                print()

                continue

            # ------------------------------------------------
            # L -> CAMBIAR IDIOMA
            # ------------------------------------------------

            if comando == "l":

                return "idiomas"

            # ------------------------------------------------
            # COMANDO DESCONOCIDO
            # ------------------------------------------------

            print()
            print(
                "Comando no válido."
            )

            print(
                "Usa C, G, B, V, L, Q "
                "o pulsa Enter."
            )

            print()

        except (
            KeyboardInterrupt,
            EOFError
        ):

            return "salir"

# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():

    idioma_origen = (
        IDIOMA_ORIGEN_INICIAL
    )

    idioma_destino = (
        IDIOMA_DESTINO_INICIAL
    )

    ultima_traduccion = ""

    while True:

        try:

            # =================================================
            # LIMPIAR PANTALLA
            # =================================================

            limpiar_pantalla()

            # =================================================
            # MOSTRAR MENÚ
            # =================================================

            mostrar_menu(
                idioma_origen,
                idioma_destino
            )

            texto = input(
                "Texto: "
            )

            comando = (
                texto.strip().casefold()
            )

            # =================================================
            # CAMBIAR IDIOMAS
            # =================================================

            if comando == "l":

                (
                    idioma_origen,
                    idioma_destino
                ) = (
                    idioma_destino,
                    idioma_origen
                )

                print()
                print(
                    "Idiomas cambiados: "
                    f"{idioma_origen.upper()} → "
                    f"{idioma_destino.upper()}"
                )

                input(
                    "\nPulsa Enter para continuar..."
                )

                continue

            # =================================================
            # GUARDAR TRADUCCIÓN
            # =================================================

            if comando == "g":

                comando_guardar(
                    idioma_origen,
                    idioma_destino
                )

                input(
                    "\nPulsa Enter para continuar..."
                )

                continue

            # =================================================
            # BORRAR TRADUCCIÓN
            # =================================================

            if comando == "b":

                comando_borrar(
                    idioma_origen,
                    idioma_destino
                )

                input(
                    "\nPulsa Enter para continuar..."
                )

                continue

            # =================================================
            # VER TRADUCCIONES
            # =================================================

            if comando == "v":

                comando_ver(
                    idioma_origen,
                    idioma_destino
                )

                continue

            # =================================================
            # COPIAR
            # =================================================

            if comando == "c":

                if not ultima_traduccion:

                    print()
                    print(
                        "No hay ninguna traducción "
                        "para copiar."
                    )

                    input(
                        "\nPulsa Enter para continuar..."
                    )

                    continue

                if copiar_portapapeles(
                    ultima_traduccion
                ):

                    print()
                    print(
                        "✓ Traducción copiada "
                        "al portapapeles."
                    )

                else:

                    print()
                    print(
                        "No se pudo acceder al "
                        "portapapeles en este sistema."
                    )

                input(
                    "\nPulsa Enter para continuar..."
                )

                continue

            #================================
            #  SALIR
            #================================

            if comando == "q":

                print()
                print("Saliendo...")

                break


            # =================================================
            # TEXTO VACÍO
            # =================================================

            if not texto.strip():

                continue

            # =================================================
            # TRADUCIR
            # =================================================

            print()
            print(
                "Traduciendo..."
            )

            encontrada = tiene_traduccion(
                texto,
                idioma_origen,
                idioma_destino
            )

            # =================================================
            # NO SE ENCONTRÓ TRADUCCIÓN
            # =================================================

            if not encontrada:

                print()
                print("-" * 50)
                print()
                print(
                    "TRADUCCIÓN:"
                )
                print()
                print(
                    texto
                )
                print()
                print("-" * 50)

                traduccion_nueva = (
                    preguntar_guardar_si_no_encontrada(
                        texto,
                        idioma_origen,
                        idioma_destino
                    )
                )

                if traduccion_nueva is not None:

                    ultima_traduccion = (
                        traduccion_nueva
                    )

                else:

                    ultima_traduccion = texto

                input(
                    "\nPulsa Enter para continuar..."
                )

                continue

            # =================================================
            # TRADUCCIÓN ENCONTRADA
            # =================================================

            resultado = traducir(
                texto,
                idioma_origen,
                idioma_destino
            )

            ultima_traduccion = (
                resultado
            )

            print()
            print("-" * 50)
            print()
            print(
                "TRADUCCIÓN:"
            )
            print()
            print(
                resultado
            )
            print()
            print("-" * 50)
            print()

            accion = esperar_comando_traduccion(
                ultima_traduccion,
                idioma_origen,
                idioma_destino
            )

            if accion == "salir":

                print()
                print("Saliendo...")
                break

            if accion == "idiomas":

                (
                    idioma_origen,
                    idioma_destino
                ) = (
                    idioma_destino,
                    idioma_origen
                )

                print()
                print(
                    "Idiomas cambiados: "
                    f"{idioma_origen.upper()} → "
                    f"{idioma_destino.upper()}"
                )

                continue

            if accion == "continuar":

                continue


        except KeyboardInterrupt:

            # =================================================
            # CTRL+C
            # =================================================

            print()
            print()
            print(
                "Saliendo..."
            )

            break

        except EOFError:

            # =================================================
            # CTRL+D / EOF
            # =================================================

            print()
            print()
            print(
                "Saliendo..."
            )

            break

        except Exception as error:

            print()
            print(
                "ERROR:",
                error
            )

            print()

            try:

                input(
                    "Pulsa Enter para continuar..."
                )

            except (
                KeyboardInterrupt,
                EOFError
            ):

                print()
                print(
                    "Saliendo..."
                )

                break


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":
    main()
