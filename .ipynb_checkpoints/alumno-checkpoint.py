"" " Juan Esteban Palacio Ibarra """ 

class Alumno:
    """
    Clase usada para el tratamiento de las notas de los alumnos. Cada uno
    incluye los atributos siguientes:

    numIden:   Número de identificación. Es un número entero que, en caso
               de no indicarse, toma el valor por defecto 'numIden=-1'.
    nombre:    Nombre completo del alumno.
    notas:     Lista de números reales con las distintas notas de cada alumno.
    """

    def __init__(self, nombre, numIden=-1, notas=[]):
        self.numIden = numIden
        self.nombre = nombre
        self.notas = [nota for nota in notas]

    def __add__(self, other):
        """
        Devuelve un nuevo objeto 'Alumno' con una lista de notas ampliada con
        el valor pasado como argumento. De este modo, añadir una nota a un
        Alumno se realiza con la orden 'alumno += nota'.
        """
        return Alumno(self.nombre, self.numIden, self.notas + [other])

    def media(self):
        """
        Devuelve la nota media del alumno.
        """
        return sum(self.notas) / len(self.notas) if self.notas else 0

    def __repr__(self):
        """
        Devuelve la representación 'oficial' del alumno. A partir de copia
        y pega de la cadena obtenida es posible crear un nuevo Alumno idéntico.
        """
        return f'Alumno("{self.nombre}", {self.numIden!r}, {self.notas!r})'

    def __str__(self):
        """
        Devuelve la representación 'bonita' del alumno. Visualiza en tres
        columnas separadas por espacios: el número de identificación,
        el nombre completo y la nota media del alumno con un decimal.
        """
        return f'{self.numIden:<5} {self.nombre:<20} {self.media():.1f}'


def prueba_alumno():
    """
    >>> a = Alumno("Juan Pérez", 101)
    >>> a += 7.5
    >>> a += 8.0
    >>> a += 9.0
    >>> print(a)
    101   Juan Pérez           8.2
    >>> print(f"{a.media():.2f}")
    8.17
    >>> b = Alumno("María López", 202, [6.0, 7.5, 8.0])
    >>> print(b)
    202   María López          7.2
    >>> print(repr(b))
    Alumno("María López", 202, [6.0, 7.5, 8.0])
    """


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
