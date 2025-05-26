"""
horas.py
Autor: Juan Esteban Palacio Ibarra

Función para normalizar expresiones horarias en textos en varios formatos al estándar HH:MM.
"""

import re

def normalizaHoras(ficText, ficNorm):
    """
    Lee el fichero ficText, busca expresiones horarias en diferentes formatos
    y escribe en ficNorm el texto con las horas normalizadas al formato HH:MM.

    Expresiones válidas soportadas y ejemplos de normalización:
    - 18:30  -> 18:30
    - 8h     -> 08:00
    - 10h30m -> 10:30
    - 4 y media de la tarde -> 16:30
    - 7h de la mañana -> 07:00
    - 5 menos cuarto -> 04:45
    - 17h5m -> 17:05
    - 12 de la noche -> 00:00

    Las expresiones incorrectas se dejan igual.

    Ejemplo:
    La llegada del tren está prevista a las 18:30
    -> La llegada del tren está prevista a las 18:30

    >>> normalizaHoras('horas.txt', 'horas_norm.txt')
    (No hay salida, pero el fichero 'horas_norm.txt' se crea con las horas normalizadas.)
    """

    # Mapas para conversiones de partes de la tarde/noche etc (12h->24h)
    periodo_map = {
        "de la mañana": lambda h: h if h != 12 else 0,
        "del mediodía": lambda h: 12 if h == 12 else h,
        "de la tarde": lambda h: h + 12 if 1 <= h <= 7 else None,
        "de la noche": lambda h: h + 12 if 1 <= h <= 4 else None,
        "de la madrugada": lambda h: h if 1 <= h <= 6 else None,
    }

    # Regex patrones para los distintos formatos
    patrones = {
        # Formato HH:MM (24h, minutos dos dígitos)
        'hhmm': re.compile(r'\b([01]?\d|2[0-3]):([0-5]\d)\b'),

        # Formato Hh o HhMm (ej: 8h, 10h30m, 17h5m)
        'hhmm_alt': re.compile(r'\b(\d{1,2})h(\d{1,2})?m?\b'),

        # Formato "H en punto"
        'en_punto': re.compile(r'\b(\d{1,2}) en punto\b'),

        # Formato "H y cuarto", "H y media", "H menos cuarto"
        'cuarto': re.compile(r'\b(\d{1,2}) (y media|y cuarto|menos cuarto)\b'),

        # Formato "H de la mañana/tarde/noche/mediodía/madrugada"
        'periodo': re.compile(r'\b(\d{1,2}) (de la mañana|del mediodía|de la tarde|de la noche|de la madrugada)\b'),

        # Formato "H y media de la tarde" (combina y media + periodo)
        'cuarto_periodo': re.compile(r'\b(\d{1,2}) (y media|y cuarto|menos cuarto) (de la mañana|del mediodía|de la tarde|de la noche|de la madrugada)\b'),
    }

    def es_valido_hora_min(h, m):
        return 0 <= h <= 23 and 0 <= m <= 59

    def es_valido_hora12(h):
        return 1 <= h <= 12

    def normalizar_hhmm(match):
        h = int(match.group(1))
        m = int(match.group(2))
        if es_valido_hora_min(h, m):
            return f"{h:02d}:{m:02d}"
        else:
            return match.group(0)  # Incorrecto, dejar igual

    def normalizar_hhmm_alt(match):
        h = int(match.group(1))
        m_str = match.group(2)
        m = int(m_str) if m_str else 0
        if es_valido_hora_min(h, m):
            return f"{h:02d}:{m:02d}"
        else:
            return match.group(0)

    def normalizar_en_punto(match):
        h = int(match.group(1))
        if es_valido_hora12(h):
            # En punto = minutos 00
            # Se asume rango 00:00 a 11:59 sin especificar periodo, dejamos en rango 0-11h
            return f"{h:02d}:00"
        else:
            return match.group(0)

    def normalizar_cuarto(match):
        h = int(match.group(1))
        tipo = match.group(2)
        if not es_valido_hora12(h):
            return match.group(0)

        if tipo == 'y media':
            m = 30
        elif tipo == 'y cuarto':
            m = 15
        elif tipo == 'menos cuarto':
            m = 45
            h -= 1
            if h == 0:
                h = 12
        else:
            return match.group(0)

        return f"{h:02d}:{m:02d}"

    def normalizar_periodo(match):
        h = int(match.group(1))
        periodo = match.group(2)
        if not es_valido_hora12(h):
            return match.group(0)

        f = periodo_map.get(periodo)
        if f is None:
            return match.group(0)
        h24 = f(h)
        if h24 is None or not (0 <= h24 <= 23):
            # Si no está en rango válido, dejamos igual
            return match.group(0)
        return f"{h24:02d}:00"

    def normalizar_cuarto_periodo(match):
        h = int(match.group(1))
        tipo = match.group(2)
        periodo = match.group(3)
        if not es_valido_hora12(h):
            return match.group(0)

        # Primero convertimos el tipo a minutos
        if tipo == 'y media':
            m = 30
        elif tipo == 'y cuarto':
            m = 15
        elif tipo == 'menos cuarto':
            m = 45
            h -= 1
            if h == 0:
                h = 12
        else:
            return match.group(0)

        # Convertimos a 24h según periodo
        f = periodo_map.get(periodo)
        if f is None:
            return match.group(0)
        h24 = f(h)
        if h24 is None or not (0 <= h24 <= 23):
            return match.group(0)

        return f"{h24:02d}:{m:02d}"

    def reemplazar(texto):
        # El orden de las sustituciones importa para no romper cosas ya reemplazadas

        # Primero normalizamos formatos con "y media/cuarto/menos cuarto + periodo"
        texto = patrones['cuarto_periodo'].sub(normalizar_cuarto_periodo, texto)

        # Luego formatos con periodo solo
        texto = patrones['periodo'].sub(normalizar_periodo, texto)

        # Formato "H y media/cuarto/menos cuarto" sin periodo
        texto = patrones['cuarto'].sub(normalizar_cuarto, texto)

        # Formato "H en punto"
        texto = patrones['en_punto'].sub(normalizar_en_punto, texto)

        # Formato Hh o HhMm
        texto = patrones['hhmm_alt'].sub(normalizar_hhmm_alt, texto)

        # Formato HH:MM 24h
        texto = patrones['hhmm'].sub(normalizar_hhmm, texto)

        return texto

    with open(ficText, encoding='utf-8') as f_in, open(ficNorm, 'w', encoding='utf-8') as f_out:
        for linea in f_in:
            linea_norm = reemplazar(linea)
            f_out.write(linea_norm)


# Si quieres probar rápido, puedes usar esto:
if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
