import datetime

class PicoPlacaPredictor:
    """
    Clase encargada de determinar si un vehículo puede circular 
    bajo la normativa de Pico y Placa.
    En # estaran mis comentarios para explicar bien el codigo 
    """

    #Mapeo de día de la semana -> dígitos restringidos
    #Se utilizan números (1=lunes, 2=martes, etc.) para ser consistentes con datetime.weekday()
    #O también podemos trabajar con strings. Aquí se elige datetime.weekday() (Monday=0..Sunday=6)
    restricted_digits_by_day = {
        0: [1, 2],  #Lunes
        1: [3, 4],  #Martes
        2: [5, 6],  #Miércoles
        3: [7, 8],  #Jueves
        4: [9, 0],  #Viernes
        #Sábado (5) y Domingo (6) no tienen restricción
    }

    #Horarios de restricción
    #Formato: (hora_inicio, hora_fin)
    #Se toman como tuplas (HH, MM) para comparación
    RESTRICTION_SCHEDULES = [
        ((7, 0), (9, 30)),   #07:00 - 09:30
        ((16, 0), (19, 30))  #16:00 - 19:30
    ]

    def __init__(self):
        pass

    def can_circulate(self, plate: str, date: str, time: str) -> bool:
        """
        Retorna True si puede circular, False en caso contrario.

        :param plate: Número de placa completo (ej. "PBX-1234" o "HX-244P").
        :param date: Fecha en formato 'YYYY-MM-DD' (flexible, se puede modificar).
        :param time: Hora en formato 'HH:MM' 24-horas (ej. "08:30").

        """

        #1. Validar último dígito de la placa
        last_digit = self._extract_last_digit(plate)
        if last_digit is None:
            #Si no pudo extraer dígito, retornamos True por defecto 
            #o podríamos lanzar una excepción. Depende del criterio.
            return True

        #2. Convertir date a un objeto datetime para obtener el día de la semana
        day_of_week = self._get_day_of_week(date)  # Monday=0, Sunday=6

        #3.Verificar si es fin de semana (Sábado=5, Domingo=6)
        #o si la fecha corresponde a un feriado (no encontre feriados específicos en esa fecha segun el .png)
        if day_of_week >= 5:
            return True  #No hay restricción sábados, domingos ni feriados

        #4.Verificar si ese día el dígito está restringido
        if not self._digit_is_restricted_on_day(last_digit, day_of_week):
            return True  #Si el dígito no está restringido ese día, puede circular

        #5.Validar la hora para ver si cae dentro de los rangos de restricción
        if self._time_in_restriction(time):
            return False
        else:
            return True

    def _extract_last_digit(self, plate: str) -> int:
        """
        Extrae el último dígito de la placa, ignorando letras.
        Por ejemplo: "PBX-1234" -> 4, "HX-244P" -> 4.
        Retorna None si no encuentra ningún dígito.
        """
        #Recorremos la placa desde el final hacia el inicio
        for char in reversed(plate):
            if char.isdigit():
                return int(char)
        return None

    def _get_day_of_week(self, date_str: str) -> int:
        """
        Convierte la fecha en un objeto datetime y retorna
        el índice del día de la semana (Monday=0, Sunday=6).
        Se espera date_str en formato 'YYYY-MM-DD'.
        """
        #Ajusta según el formato que más te convenga
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.weekday()

    def _digit_is_restricted_on_day(self, digit: int, day_of_week: int) -> bool:
        """
        Verifica si el dígito está restringido en ese día.
        """
        if day_of_week not in self.restricted_digits_by_day:
            return False
        restricted_list = self.restricted_digits_by_day[day_of_week]
        return digit in restricted_list

    def _time_in_restriction(self, time_str: str) -> bool:
        """
        Determina si la hora dada está dentro de alguno de los rangos de restricción.
        :param time_str: Hora en formato "HH:MM" (24-horas).
        :return: True si está en horario restringido, False en caso contrario.
        """
        hour, minute = map(int, time_str.split(':'))
        time_obj = datetime.time(hour=hour, minute=minute)

        for schedule in self.RESTRICTION_SCHEDULES:
            start, end = schedule
            start_time = datetime.time(start[0], start[1])  #(7,0) -> 07:00
            end_time = datetime.time(end[0], end[1])        #(9,30) -> 09:30

            if start_time <= time_obj <= end_time:
                return True

        return False
