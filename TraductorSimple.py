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

TRADUCCIONES_PERSONALIZADAS = {

    # ========================================================
    # ESPAÑOL → INGLÉS
    # ========================================================

    ("es", "en"): {

        # Expresiones religiosas
        "a dios": "goodbye",
        "adiós": "goodbye",
        "adios": "goodbye",
        "por Dios": "for God's sake",
        "por dios": "for God's sake",
        "Dios mío": "my God",
        "dios mío": "my God",
        "Dios mio": "my God",
        "dios mio": "my God",

        "gracias a Dios": "thank God",
        "gracias a dios": "thank God",
        "bendito sea Dios": "blessed be God",
        "bendito sea dios": "blessed be God",

        "Dios te bendiga": "God bless you",
        "dios te bendiga": "God bless you",
        "Dios los bendiga": "God bless you all",
        "dios los bendiga": "God bless you all",
        "que Dios te bendiga": "may God bless you",
        "que dios te bendiga": "may God bless you",
        "que Dios los bendiga": "may God bless you all",
        "que dios los bendiga": "may God bless you all",

        "si Dios quiere": "God willing",
        "si dios quiere": "God willing",
        "Dios mediante": "God willing",
        "dios mediante": "God willing",
        "con la ayuda de Dios": "with God's help",
        "con la ayuda de dios": "with God's help",

        "Dios sabe": "God knows",
        "dios sabe": "God knows",
        "solo Dios sabe": "only God knows",
        "solo dios sabe": "only God knows",
        "Dios lo sabe": "God knows",
        "dios lo sabe": "God knows",
        "Dios sabrá": "God will know",
        "dios sabra": "God will know",

        "Dios mío, ayúdame": "My God, help me",
        "dios mío ayúdame": "My God, help me",
        "Dios mio ayudame": "My God, help me",
        "dios mio ayudame": "My God, help me",
        "Dios mío, qué horror": "My God, how awful",
        "dios mío que horror": "My God, how awful",
        "Dios mío, qué pasa": "My God, what's happening",
        "dios mio que pasa": "My God, what's happening",

        "por el amor de Dios": "for God's sake",
        "por el amor de dios": "for God's sake",
        "por Dios, para": "for God's sake, stop",
        "por dios, para": "for God's sake, stop",

        "alabado sea Dios": "praise God",
        "alabado sea dios": "praise God",
        "gloria a Dios": "glory to God",
        "gloria a dios": "glory to God",
        "gloria al Señor": "glory to the Lord",
        "gloria al señor": "glory to the Lord",

        "Señor, ayúdame": "Lord, help me",
        "señor, ayúdame": "Lord, help me",
        "Señor ayúdame": "Lord, help me",
        "señor ayudame": "Lord, help me",
        "Dios, ayúdame": "God, help me",
        "dios ayudame": "God, help me",

        "que Dios me ayude": "may God help me",
        "que dios me ayude": "may God help me",
        "que Dios nos ayude": "may God help us",
        "que dios nos ayude": "may God help us",

        "Dios tenga piedad": "may God have mercy",
        "dios tenga piedad": "may God have mercy",
        "Dios tenga misericordia": "may God have mercy",
        "dios tenga misericordia": "may God have mercy",
        "ten piedad, Dios mío": "have mercy, my God",
        "ten piedad dios mío": "have mercy, my God",

        "por voluntad de Dios": "by God's will",
        "por voluntad de dios": "by God's will",
        "la voluntad de Dios": "the will of God",
        "la voluntad de dios": "the will of God",

        "palabra de Dios": "word of God",
        "palabra de dios": "word of God",
        "amor de Dios": "love of God",
        "amor de dios": "love of God",
        "gracia de Dios": "grace of God",
        "gracia de dios": "grace of God",

        "fe en Dios": "faith in God",
        "fe en dios": "faith in God",
        "creo en Dios": "I believe in God",
        "creo en dios": "I believe in God",
        "confío en Dios": "I trust in God",
        "confio en dios": "I trust in God",

        "Dios está conmigo": "God is with me",
        "dios esta conmigo": "God is with me",
        "Dios está contigo": "God is with you",
        "dios esta contigo": "God is with you",
        "Dios está con nosotros": "God is with us",
        "dios esta con nosotros": "God is with us",

        "que Dios te acompañe": "may God be with you",
        "que dios te acompañe": "may God be with you",
        "que Dios te proteja": "may God protect you",
        "que dios te proteja": "may God protect you",
        "que Dios nos proteja": "may God protect us",
        "que dios nos proteja": "may God protect us",

        "descansa en paz": "rest in peace",
        "que descanse en paz": "may he rest in peace",
        "en paz descanse": "may he rest in peace",

        "amén": "amen",
        "amen": "amen",
        "aleluya": "hallelujah",

        "Jesús": "Jesus",
        "jesus": "Jesus",
        "Jesucristo": "Jesus Christ",
        "jesucristo": "Jesus Christ",
        "Cristo": "Christ",
        "cristo": "Christ",
        "Señor": "Lord",
        "señor": "Lord",

        "en el nombre de Dios": "in the name of God",
        "en el nombre de dios": "in the name of God",
        "en el nombre de Jesús": "in the name of Jesus",
        "en el nombre de jesus": "in the name of Jesus",

        "gracias Señor": "thank you, Lord",
        "gracias señor": "thank you, Lord",
        "Señor ten piedad": "Lord have mercy",
        "señor ten piedad": "Lord have mercy",
        "que Dios te guarde": "may God keep you",
        "que dios te guarde": "may God keep you",

        "es una bendición": "it's a blessing",
        "es una bendicion": "it's a blessing",
        "qué bendición": "what a blessing",
        "que bendicion": "what a blessing",
        "milagro de Dios": "miracle of God",
        "milagro de dios": "miracle of God",
        "es un milagro": "it's a miracle",

        "Dios es bueno": "God is good",
        "dios es bueno": "God is good",
        "Dios es grande": "God is great",
        "dios es grande": "God is great",
        "Dios es amor": "God is love",
        "dios es amor": "God is love",

        "si Dios lo permite": "if God allows it",
        "si dios lo permite": "if God allows it",
        "que Dios quiera": "God willing",
        "con Dios": "with God",
        "junto a Dios": "with God",
        "cerca de Dios": "close to God",


        # Saludos y despedidas
        "buenos días": "good morning",
        "buen día": "good morning",
        "buen dia": "good day",
        "buenas tardes": "good afternoon",
        "buenas noches": "good evening",
        "hasta luego": "see you later",
        "hasta pronto": "see you soon",
        "nos vemos": "see you",
        "qué tal": "how are you",
        "que tal": "how are you",
        "hola": "hello",
        "hola a todos": "hello everyone",
        "hola amigo": "hello friend",
        "hola amiga": "hello friend",
        "buenos dias": "good morning",
        "cómo estás": "how are you",
        "como estas": "like this",
        "cómo estás?": "how are you?",
        "como estas?": "how are you?",
        "cómo te va": "how are you doing",
        "como te va": "how are you doing",

        # Conversación
        "¿cómo estás?": "how are you?",
        "¿cómo estás": "how are you?",
        "mucho gusto": "nice to meet you",
        "encantado de conocerte": "nice to meet you",
        "encantada de conocerte": "nice to meet you",
        "qué haces?": "what are you doing?",
        "que haces?": "what are you doing?",
        "qué pasa": "what's going on",
        "que pasa": "what's going on",
        "qué pasa?": "what's going on?",
        "que pasa?": "what's going on?",
        "qué ocurre": "what's happening",
        "que ocurre": "what's happening",
        "qué quieres": "what do you want",
        "que quieres": "what do you want",
        "qué quieres?": "what do you want?",
        "qué necesitas": "what do you need",
        "que necesitas": "what do you need",
        "qué dices": "what are you saying",
        "que dices": "what are you saying",
        "qué estás haciendo": "what are you doing",
        "que estas haciendo": "what are you doing",
        "dónde estás": "where are you",
        "donde estas": "where are you",
        "dónde estás?": "where are you?",
        "donde estas?": "where are you?",
        "dónde vas": "where are you going",
        "donde vas": "where are you going",
        "dónde vives": "where do you live",
        "donde vives": "where do you live",

        # Agradecimientos
        "gracias": "thank you",
        "muchas gracias": "thank you very much",
        "de nada": "you're welcome",
        "no hay de qué": "you're welcome",
        "no hay de que": "you're welcome",
        "mil gracias": "thanks a lot",
        "gracias por todo": "thank you for everything",
        "gracias por tu ayuda": "thank you for your help",
        "gracias por ayudarme": "thank you for helping me",
        "no te preocupes": "don't worry",

        # Cortesía
        "por favor": "please",
        "perdón": "sorry",
        "perdon": "sorry",
        "lo siento": "I'm sorry",
        "disculpa": "excuse me",
        "disculpe": "excuse me",
        "con permiso": "excuse me",
        "claro que sí": "of course",
        "claro que si": "of course",
        "no pasa nada": "it's okay",
        "sin problema": "no problem",
        "ningún problema": "no problem",
        "ningun problema": "no problem",

        # Afirmación / negación
        "si": "yes",
        "no": "no",
        "claro": "of course",
        "por supuesto": "of course",
        "vale": "okay",
        "de acuerdo": "okay",
        "está bien": "it's okay",
        "esta bien": "it's okay",
        "tal vez": "maybe",
        "quizás": "maybe",
        "quizas": "maybe",
        "no lo sé": "I don't know",
        "no lo se": "I don't know",
        "no sé": "I don't know",
        "no se": "I don't know",
        "no entiendo": "I don't understand",
        "entiendo": "I understand",
        "ya entiendo": "I understand now",
        "lo entiendo": "I understand",
        "no puedo": "I can't",
        "puedo": "I can",
        "no quiero": "I don't want to",
        "quiero": "I want to",
        "no puedo hacerlo": "I can't do it",
        "puedo hacerlo": "I can do it",

        # Expresiones frecuentes
        "te quiero": "I love you",
        "te amo": "I love you",
        "te extraño": "I miss you",
        "te echo de menos": "I miss you",
        "tengo hambre": "I'm hungry",
        "tengo sed": "I'm thirsty",
        "tengo sueño": "I'm sleepy",
        "tengo miedo": "I'm scared",
        "¿qué pasa?": "what's going on?",
        "¿qué haces?": "what are you doing?",
        "que haces": "what are you doing?",
        "¿dónde estás?": "where are you?",
        "donde estás": "where you are",
        "¿qué quieres?": "what do you want?",
        "te quiero mucho": "I love you very much",
        "me gustas": "I like you",
        "me gusta": "I like it",
        "no me gusta": "I don't like it",
        "me encanta": "I love it",
        "odio esto": "I hate this",
        "estoy feliz": "I'm happy",
        "estoy triste": "I'm sad",
        "estoy cansado": "I'm tired",
        "estoy cansada": "I'm tired",
        "estoy aburrido": "I'm bored",
        "estoy aburrida": "I'm bored",
        "estoy ocupado": "I'm busy",
        "estoy ocupada": "I'm busy",
        "estoy preocupado": "I'm worried",
        "estoy preocupada": "I'm worried",
        "estoy enfadado": "I'm angry",
        "estoy enfadada": "I'm angry",

        # Tiempo
        "ahora": "now",
        "hoy": "today",
        "mañana": "tomorrow",
        "ayer": "yesterday",
        "esta mañana": "this morning",
        "esta tarde": "this afternoon",
        "esta noche": "tonight",
        "ahora mismo": "right now",
        "esta semana": "this week",
        "la semana que viene": "next week",
        "la semana pasada": "last week",
        "más tarde": "later",
        "mas tarde": "later",
        "después": "later",
        "despues": "later",
        "antes": "before",
        "pronto": "soon",

        # Personas
        "mi amigo": "my friend",
        "mi amiga": "my friend",
        "mi hermano": "my brother",
        "mi hermana": "my sister",
        "mi padre": "my father",
        "mi madre": "my mother",
        "mi mamá": "my mom",
        "mi mama": "my mom",
        "mi papá": "my dad",
        "mi papa": "my dad",
        "mi hijo": "my son",
        "mi hija": "my daughter",
        "mi novio": "my boyfriend",
        "mi novia": "my girlfriend",
        "mi marido": "my husband",
        "mi esposa": "my wife",

        # TRABAJO
        "estoy trabajando": "I'm working",
        "estoy en el trabajo": "I'm at work",
        "tengo trabajo": "I have work",
        "no tengo trabajo": "I don't have a job",
        "terminé de trabajar": "I finished work",
        "termine de trabajar": "I finished work",



        # Lugares / objetos comunes
        "mi casa": "my house",
        "mi coche": "my car",
        "mi teléfono": "my phone",
        "mi movil": "my phone",
        "mi móvil": "my phone",
        "mi habitación":"my room",
        "mi habitacion":"my room",
        "mi abitacion": "my room",
        "ordenador": "computer",
        "computadora": "computer",
        "aleatorio": "random",
        "teléfono móvil": "mobile phone",
        "telefono movil": "mobile phone",


        # DESPLAZAMIENTO
        "voy": "I'm going",
        "voy a casa": "I'm going home",
        "me voy a casa": "I'm going home",
        "voy al trabajo": "I'm going to work",
        "voy a trabajar": "I'm going to work",
        "voy a dormir": "I'm going to sleep",
        "me voy a dormir": "I'm going to bed",
        "voy a comer": "I'm going to eat",
        "voy a salir": "I'm going out",
        "estoy saliendo": "I'm leaving",
        "estoy de camino": "I'm on my way",
        "ya voy": "I'm coming",
        "ahora voy": "I'm coming now",
        "ya voy para allá": "I'm on my way",
        "ya voy para alla": "I'm on my way",
        "voy para casa": "I'm going home",
        "estoy llegando": "I'm arriving",
        "ya llegué": "I've arrived",
        "ya llegue": "I've arrived",



        # Frases frecuentes
        "te llamo luego": "I'll call you later",
        "hablamos luego": "talk to you later",
        "nos vemos mañana": "see you tomorrow",
        "hasta mañana": "see you tomorrow",
        "nos vemos luego": "see you later",
        "me voy": "I'm leaving",
        "ya me voy": "I'm leaving now",
        "me tengo que ir": "I have to go",
        "tengo que irme": "I have to go",
        "tengo que ir": "I have to go",
        "voy a irme": "I'm going to leave",
        "me marcho": "I'm leaving",
        "hasta la próxima": "see you next time",
        "hasta la proxima": "see you next time",
        "buen viaje": "have a good trip",
        "que tengas un buen día": "have a good day",
        "que tengas un buen dia": "have a good day",
        "tengo frío": "I'm cold",
        "tengo frio": "I'm cold",
        "tengo calor": "I'm hot",
        "tengo prisa": "I'm in a hurry",
        "tengo tiempo": "I have time",
        "no tengo tiempo": "I don't have time",
        "necesito dormir": "I need to sleep",
        "necesito comer": "I need to eat",
        "necesito irme": "I need to leave",
        "ayúdame": "help me",
        "ayudame": "help me",
        "necesito ayuda": "I need help",
        "ayuda": "help",
        "qué ha pasado": "what happened",
        "que ha pasado": "what happened",
        "no funciona": "it doesn't work",
        "funciona": "it works",
        "hay un problema": "there is a problem",
        "tenemos un problema": "we have a problem",
        "no funciona bien": "it doesn't work properly",
        "qué quieres decir": "what do you mean",
        "que quieres decir": "what do you mean",
        "qué significa": "what does it mean",
        "que significa": "what does it mean",
        "cómo se dice": "how do you say",
        "como se dice": "how do you say",
        "cómo se dice en inglés": "how do you say it in English",
        "como se dice en ingles": "how do you say it in English",
        "dame un momento": "give me a moment",
        "espera un momento": "wait a moment",
        "espera": "wait",
        "un momento": "one moment",
        "ven aquí": "come here",
        "ven aqui": "come here",
        "mira esto": "look at this",
        "escúchame": "listen to me",
        "escuchame": "listen to me",
        "mírame": "look at me",
        "mirame": "look at me",
        "déjame en paz": "leave me alone",
        "dejame en paz": "leave me alone",
        "ten cuidado": "be careful",
        "todo está bien": "everything is fine",
        "todo esta bien": "everything is fine",
        "está todo bien": "everything is okay",
        "esta todo bien": "everything is okay",
        "qué buena idea": "what a good idea",
        "que buena idea": "what a good idea",
        "no tengo ni idea": "I have no idea",
        "eso es verdad": "that's true",
        "es verdad": "it's true",
        "tienes razón": "you're right",
        "tienes razon": "you're right",
        "tienes toda la razón": "you're absolutely right",
        "tienes toda la razon": "you're absolutely right",
        "no tienes razón": "you're wrong",
        "no tienes razon": "you're wrong",
        "dónde está el hotel": "where is the hotel",
        "donde esta el hotel": "where is the hotel",
        "dónde está el aeropuerto": "where is the airport",
        "donde esta el aeropuerto": "where is the airport",
        "quiero ir al aeropuerto": "I want to go to the airport",
        "estoy perdido": "I'm lost",
        "estoy perdida": "I'm lost",
        "¿cuánto cuesta?": "how much does it cost?",
        "cuánto cuesta": "how much does it cost",
        "cuanto cuesta": "how much does it cost",

    },

    # ========================================================
    # INGLÉS → ESPAÑOL
    # ========================================================

    ("en", "es"): {

        # ====================================================
        # EXPRESIONES RELIGIOSAS
        # ====================================================

        "goodbye": "adiós",
        "bye": "adiós",
        "farewell": "adiós",

        "for God's sake": "por Dios",
        "for gods sake": "por Dios",
        "my God": "Dios mío",
        "my god": "Dios mío",

        "thank God": "gracias a Dios",
        "blessed be God": "bendito sea Dios",
        "God bless you": "Dios te bendiga",
        "God bless you all": "Dios los bendiga",
        "may God bless you": "que Dios te bendiga",
        "may God bless you all": "que Dios los bendiga",

        "God willing": "si Dios quiere",
        "if God allows it": "si Dios lo permite",
        "with God's help": "con la ayuda de Dios",

        "God knows": "Dios sabe",
        "only God knows": "solo Dios sabe",
        "God will know": "Dios sabrá",

        "My God, help me": "Dios mío, ayúdame",
        "my God, help me": "Dios mío, ayúdame",
        "My God, how awful": "Dios mío, qué horror",
        "my God, how awful": "Dios mío, qué horror",
        "My God, what's happening": "Dios mío, qué está pasando",
        "my God, what's happening": "Dios mío, qué está pasando",

        "praise God": "alabado sea Dios",
        "glory to God": "gloria a Dios",
        "glory to the Lord": "gloria al Señor",
        "Lord, help me": "Señor, ayúdame",
        "God, help me": "Dios, ayúdame",
        "may God help me": "que Dios me ayude",
        "may God help us": "que Dios nos ayude",
        "may God have mercy": "que Dios tenga piedad",
        "have mercy, my God": "ten piedad, Dios mío",
        "by God's will": "por voluntad de Dios",
        "the will of God": "la voluntad de Dios",

        "word of God": "palabra de Dios",
        "love of God": "amor de Dios",
        "grace of God": "gracia de Dios",

        "faith in God": "fe en Dios",
        "I believe in God": "creo en Dios",
        "I trust in God": "confío en Dios",

        "God is with me": "Dios está conmigo",
        "God is with you": "Dios está contigo",
        "God is with us": "Dios está con nosotros",

        "may God be with you": "que Dios te acompañe",
        "may God protect you": "que Dios te proteja",
        "may God protect us": "que Dios nos proteja",
        "may God keep you": "que Dios te guarde",

        "rest in peace": "descansa en paz",
        "may he rest in peace": "que descanse en paz",
        "may she rest in peace": "que descanse en paz",

        "amen": "amén",
        "hallelujah": "aleluya",

        "Jesus": "Jesús",
        "Jesus Christ": "Jesucristo",
        "Christ": "Cristo",
        "Lord": "Señor",

        "in the name of God": "en el nombre de Dios",
        "in the name of Jesus": "en el nombre de Jesús",

        "thank you, Lord": "gracias, Señor",
        "Lord have mercy": "Señor, ten piedad",

        "it's a blessing": "es una bendición",
        "what a blessing": "qué bendición",
        "miracle of God": "milagro de Dios",
        "it's a miracle": "es un milagro",

        "God is good": "Dios es bueno",
        "God is great": "Dios es grande",
        "God is love": "Dios es amor",

        # ====================================================
        # SALUDOS
        # ====================================================

        "hello": "hola",
        "hi": "hola",
        "hello everyone": "hola a todos",
        "hello friend": "hola amigo",
        "good morning": "buenos días",
        "good day": "buen día",
        "good afternoon": "buenas tardes",
        "good evening": "buenas tardes",
        "good night": "buenas noches",

        "how are you": "¿cómo estás?",
        "how are you?": "¿cómo estás?",
        "how are you doing": "¿cómo te va?",
        "how are you doing?": "¿cómo te va?",

        # ====================================================
        # DESPEDIDAS
        # ====================================================

        "see you": "nos vemos",
        "see you later": "hasta luego",
        "see you soon": "hasta pronto",
        "see you tomorrow": "nos vemos mañana",
        "see you next time": "hasta la próxima",
        "I'm leaving": "me voy",
        "I'm leaving now": "ya me voy",
        "I have to go": "me tengo que ir",
        "I need to leave": "necesito irme",
        "I'm going to leave": "voy a irme",
        "I'm going home": "me voy a casa",
        "I'm going out": "voy a salir",

        # ====================================================
        # AGRADECIMIENTOS
        # ====================================================

        "thank you": "gracias",
        "thanks": "gracias",
        "thank you very much": "muchas gracias",
        "thanks a lot": "mil gracias",
        "thank you for everything": "gracias por todo",
        "thank you for your help": "gracias por tu ayuda",
        "thank you for helping me": "gracias por ayudarme",

        "you're welcome": "de nada",
        "no problem": "no hay problema",
        "don't worry": "no te preocupes",

        # ====================================================
        # CORTESÍA
        # ====================================================

        "please": "por favor",
        "sorry": "lo siento",
        "excuse me": "disculpa",
        "of course": "por supuesto",
        "yes": "sí",
        "no": "no",
        "okay": "vale",
        "it's okay": "está bien",
        "that's okay": "está bien",
        "no worries": "no te preocupes",

        # ====================================================
        # CONVERSACIÓN
        # ====================================================

        "what are you doing": "¿qué haces?",
        "what are you doing?": "¿qué haces?",
        "what's going on": "¿qué pasa?",
        "what's going on?": "¿qué pasa?",
        "what's happening": "¿qué está pasando?",
        "what's happening?": "¿qué está pasando?",

        "what do you want": "¿qué quieres?",
        "what do you want?": "¿qué quieres?",
        "what do you need": "¿qué necesitas?",
        "what do you need?": "¿qué necesitas?",

        "what are you saying": "¿qué estás diciendo?",
        "what are you saying?": "¿qué estás diciendo?",

        "where are you": "¿dónde estás?",
        "where are you?": "¿dónde estás?",
        "where are you going": "¿adónde vas?",
        "where are you going?": "¿adónde vas?",

        "where do you live": "¿dónde vives?",
        "where do you live?": "¿dónde vives?",

        "what do you mean": "¿qué quieres decir?",
        "what do you mean?": "¿qué quieres decir?",
        "what does it mean": "¿qué significa?",
        "what does it mean?": "¿qué significa?",

        # ====================================================
        # RESPUESTAS
        # ====================================================

        "maybe": "quizás",
        "I don't know": "no lo sé",
        "I don't understand": "no entiendo",
        "I understand": "entiendo",
        "I understand now": "ya entiendo",
        "I can": "puedo",
        "I can't": "no puedo",
        "I want to": "quiero",
        "I don't want to": "no quiero",
        "I can do it": "puedo hacerlo",
        "I can't do it": "no puedo hacerlo",

        # ====================================================
        # SENTIMIENTOS
        # ====================================================

        "I love you": "te quiero",
        "I love you very much": "te quiero mucho",
        "I miss you": "te extraño",
        "I like you": "me gustas",
        "I like it": "me gusta",
        "I don't like it": "no me gusta",
        "I love it": "me encanta",
        "I hate this": "odio esto",

        "I'm happy": "estoy feliz",
        "I'm sad": "estoy triste",
        "I'm tired": "estoy cansado",
        "I'm bored": "estoy aburrido",
        "I'm busy": "estoy ocupado",
        "I'm worried": "estoy preocupado",
        "I'm scared": "tengo miedo",
        "I'm angry": "estoy enfadado",

        # ====================================================
        # NECESIDADES
        # ====================================================

        "I'm hungry": "tengo hambre",
        "I'm thirsty": "tengo sed",
        "I'm sleepy": "tengo sueño",
        "I'm cold": "tengo frío",
        "I'm hot": "tengo calor",
        "I'm in a hurry": "tengo prisa",
        "I have time": "tengo tiempo",
        "I don't have time": "no tengo tiempo",

        "I need help": "necesito ayuda",
        "I need to sleep": "necesito dormir",
        "I need to eat": "necesito comer",

        # ====================================================
        # TIEMPO
        # ====================================================

        "now": "ahora",
        "right now": "ahora mismo",
        "today": "hoy",
        "tomorrow": "mañana",
        "yesterday": "ayer",
        "this morning": "esta mañana",
        "this afternoon": "esta tarde",
        "tonight": "esta noche",
        "this week": "esta semana",
        "next week": "la semana que viene",
        "last week": "la semana pasada",
        "later": "más tarde",
        "before": "antes",
        "soon": "pronto",

        # ====================================================
        # FAMILIA
        # ====================================================

        "my mother": "mi madre",
        "my mom": "mi mamá",
        "my father": "mi padre",
        "my dad": "mi papá",
        "my brother": "mi hermano",
        "my sister": "mi hermana",
        "my son": "mi hijo",
        "my daughter": "mi hija",
        "my friend": "mi amigo",
        "my boyfriend": "mi novio",
        "my girlfriend": "mi novia",
        "my husband": "mi marido",
        "my wife": "mi esposa",

        # ====================================================
        # CASA / OBJETOS
        # ====================================================

        "my house": "mi casa",
        "at home": "en casa",
        "I'm at home": "estoy en casa",
        "my room": "mi habitación",
        "my car": "mi coche",
        "my phone": "mi teléfono",
        "computer": "ordenador",
        "mobile phone": "teléfono móvil",
        "random": "aleatorio",

        # ====================================================
        # DESPLAZAMIENTO
        # ====================================================

        "I'm going": "voy",
        "I'm going to work": "voy a trabajar",
        "I'm going to sleep": "voy a dormir",
        "I'm going to bed": "me voy a dormir",
        "I'm going to eat": "voy a comer",
        "I'm on my way": "estoy de camino",
        "I'm coming": "ya voy",
        "I'm coming now": "ahora voy",
        "I'm arriving": "estoy llegando",
        "I've arrived": "ya llegué",

        # ====================================================
        # TRABAJO
        # ====================================================

        "I'm working": "estoy trabajando",
        "I'm at work": "estoy en el trabajo",
        "I have work": "tengo trabajo",
        "I don't have a job": "no tengo trabajo",
        "I finished work": "terminé de trabajar",

        # ====================================================
        # COMIDA
        # ====================================================

        "I want to eat": "quiero comer",
        "let's eat": "vamos a comer",
        "let's have dinner": "vamos a cenar",
        "let's have breakfast": "vamos a desayunar",
        "what are we eating": "¿qué comemos?",
        "what are we eating?": "¿qué comemos?",
        "it's delicious": "está delicioso",
        "it's very good": "está muy bueno",

        # ====================================================
        # AYUDA / PROBLEMAS
        # ====================================================

        "help": "ayuda",
        "help me": "ayúdame",
        "what happened": "¿qué ha pasado?",
        "it doesn't work": "no funciona",
        "it works": "funciona",
        "there is a problem": "hay un problema",
        "we have a problem": "tenemos un problema",
        "it doesn't work properly": "no funciona bien",

        # ====================================================
        # FRASES FRECUENTES
        # ====================================================

        "give me a moment": "dame un momento",
        "wait a moment": "espera un momento",
        "wait": "espera",
        "one moment": "un momento",
        "come here": "ven aquí",
        "look at this": "mira esto",
        "listen to me": "escúchame",
        "look at me": "mírame",
        "leave me alone": "déjame en paz",
        "be careful": "ten cuidado",

        "everything is fine": "todo está bien",
        "everything is okay": "está todo bien",
        "what a good idea": "qué buena idea",
        "I have no idea": "no tengo ni idea",
        "that's true": "eso es verdad",
        "it's true": "es verdad",
        "you're right": "tienes razón",
        "you're absolutely right": "tienes toda la razón",
        "you're wrong": "estás equivocado",

        # ====================================================
        # LLAMADAS / COMUNICACIÓN
        # ====================================================

        "I'll call you later": "te llamo luego",
        "talk to you later": "hablamos luego",

        # ====================================================
        # VIAJES
        # ====================================================

        "have a good trip": "buen viaje",
        "where is the hotel": "¿dónde está el hotel?",
        "where is the airport": "¿dónde está el aeropuerto?",
        "I want to go to the airport": "quiero ir al aeropuerto",
        "I'm lost": "estoy perdido",
        "how much does it cost": "¿cuánto cuesta?",
        "how much does it cost?": "¿cuánto cuesta?",

    },
}
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
    print("Enter      →  Siguiente")
    print("Ctrl+C     →  Salir")

    print()
    print("-" * 60)
    print()


# ============================================================
# PORTAPAPELES
# ============================================================

def copiar_portapapeles(texto):

    if not texto:

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

    personalizada = buscar_traduccion_personalizada(texto)

    if personalizada is not None:

        return personalizada

    trozos = dividir_texto(texto)

    traducciones = []

    for trozo in trozos:

        traducciones.append(
            traducir_trozo(trozo)
        )

    return " ".join(traducciones)



def buscar_traduccion_personalizada(texto):

    traducciones = TRADUCCIONES_PERSONALIZADAS.get(
        (origen, destino),
        {}
    )

    texto_normalizado = texto.strip().lower()

    for original, traduccion in traducciones.items():

        if texto_normalizado == original.lower():

            return traduccion

    return None


# ============================================================
# CAMBIAR IDIOMAS
# ============================================================

def cambiar_idiomas():

    global origen
    global destino

    origen, destino = destino, origen


# ============================================================
# ESPERAR ENTER PARA CONTINUAR
# ============================================================

def esperar_enter():

    while True:

        try:

            entrada = input()

        except KeyboardInterrupt:

            raise

        except EOFError:

            return False

        # ----------------------------------------------------
        # Solamente Enter.
        # ----------------------------------------------------

        if entrada == "":

            return True

        # ----------------------------------------------------
        # Si escribe algo, no hacemos nada.
        # Volvemos a pedir únicamente Enter.
        # ----------------------------------------------------

        print(
            "Pulsa solamente Enter para continuar.",
            flush=True
        )


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():

    global ultima_traduccion

    # --------------------------------------------------------
    # Indica si existe una traducción que se puede copiar.
    # --------------------------------------------------------

    traduccion_recibida = False

    mostrar_cabecera()

    while True:

        try:

            # =================================================
            # ESCRIBIR TEXTO
            # =================================================

            texto = input("Texto: ")

        except KeyboardInterrupt:

            limpiar_terminal()

            print()
            print("Saliendo...")
            print()

            break

        except EOFError:

            limpiar_terminal()

            print()
            print("Saliendo...")
            print()

            break

        # =====================================================
        # QUITAR ESPACIOS
        # =====================================================

        texto = texto.strip()

        # =====================================================
        # ENTER SOLO
        # =====================================================
        #
        # Si no estamos escribiendo una traducción y se pulsa
        # Enter, simplemente seguimos esperando.
        #
        # =====================================================

        if not texto:

            continue

        # =====================================================
        # CAMBIAR IDIOMAS
        # =====================================================
        #
        # L + Enter
        #
        # =====================================================

        if texto == "L":

            cambiar_idiomas()

            ultima_traduccion = ""

            traduccion_recibida = False

            mostrar_cabecera()

            continue

        # =====================================================
        # COPIAR TRADUCCIÓN
        # =====================================================
        #
        # C + Enter
        #
        # =====================================================

        if texto == "C":

            if not traduccion_recibida:

                mostrar_mensaje(
                    "No hay ninguna traducción para copiar."
                )

                print(
                    "Pulsa Enter para continuar: ",
                    end="",
                    flush=True
                )

                try:

                    if not esperar_enter():

                        break

                except KeyboardInterrupt:

                    break

                mostrar_cabecera()

                continue

            # ------------------------------------------------
            # Copiar
            # ------------------------------------------------

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

            # ------------------------------------------------
            # Después de copiar NO limpiamos todavía.
            #
            # El usuario debe pulsar Enter solo.
            # ------------------------------------------------

            print(
                "Pulsa Enter para continuar: ",
                end="",
                flush=True
            )

            try:

                if not esperar_enter():

                    break

            except KeyboardInterrupt:

                break

            mostrar_cabecera()

            continue

        # =====================================================
        # TRADUCIR
        # =====================================================

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
        print("Enter      →  Siguiente")
        print("Ctrl+C     →  Salir")

        print()
        print("-" * 60)
        print()

        print(
            "Texto:",
            texto
        )

        print()

        print(
            "Traduciendo...",
            flush=True
        )

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

            # ------------------------------------------------
            # Ahora el usuario puede:
            #
            # C + Enter → copiar
            # L + Enter → cambiar idioma
            # Enter     → siguiente
            #
            # ------------------------------------------------

            print(
                "C + Enter → copiar | "
                "L + Enter → cambiar idioma | "
                "Enter → siguiente"
            )

            while True:

                try:

                    siguiente = input()

                except KeyboardInterrupt:

                    raise

                except EOFError:

                    return

                # --------------------------------------------
                # ENTER SOLO
                # --------------------------------------------

                if siguiente == "":

                    limpiar_terminal()

                    mostrar_cabecera()

                    break

                # --------------------------------------------
                # COPIAR
                # --------------------------------------------

                if siguiente == "C":

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
                        "Pulsa Enter para continuar: ",
                        end="",
                        flush=True
                    )

                    continue

                # --------------------------------------------
                # CAMBIAR IDIOMA
                # --------------------------------------------

                if siguiente == "L":

                    cambiar_idiomas()

                    ultima_traduccion = ""

                    traduccion_recibida = False

                    limpiar_terminal()

                    mostrar_cabecera()

                    break

                # --------------------------------------------
                # CUALQUIER OTRA COSA
                # --------------------------------------------

                print(
                    "Introduce C, L o pulsa solamente Enter.",
                    flush=True
                )

        except Exception as error:

            ultima_traduccion = ""

            traduccion_recibida = False

            print("-" * 60)
            print("ERROR:")
            print()
            print(error)
            print("-" * 60)
            print()

            print(
                "Pulsa Enter para continuar: ",
                end="",
                flush=True
            )

            try:

                if not esperar_enter():

                    break

            except KeyboardInterrupt:

                break

            mostrar_cabecera()


# ============================================================
# INICIO
# ============================================================

if __name__ == "__main__":

    main()
