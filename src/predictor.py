import datetime

class PicoPlacaPredictor:
    """
    Clase encargada de determinar si un vehículo puede circular 
    bajo la normativa de Pico y Placa.
    En # estaran mis comentarios para explicar bien el codigo 
    """
    #Mapeo de día de la semana -> dígitos restringidos
    # Usamos datetime.weekday() (Monday=0 .. Sunday=6)
    restricted_digits_by_day = {
        0: [1, 2],  # Lunes
        1: [3, 4],  # Martes
        2: [5, 6],  # Miércoles
        3: [7, 8],  # Jueves
        4: [9, 0],  # Viernes
        #Sábado(5) y Domingo(6) no tienen restricción
    }

    #Horarios de restricción (HH, MM)
    RESTRICTION_SCHEDULES = [
        ((7, 0), (9, 30)),   #07:00 -09:30
        ((16, 0), (19, 30))  #16:00- 19:30
    ]

    def __init__(self):
        pass

    def can_circulate(self, plate: str, date: str, time: str) -> bool:
        """
        Retorna True si puede circular, False en caso contrario.
        Antes de cualquier otra cosa, se validan de forma incondicional la fecha y la hora
        """

        #VALIDAR el formato de la fecha siempre
        try:
            date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"ERROR: La fecha '{date}' no cumple con el formato YYYY-MM-DD.")

        #VALIDAR el formato de la hora siempre
        try:
            hour, minute = map(int, time.split(':'))
            time_obj = datetime.time(hour, minute)
        except ValueError:
            raise ValueError(f"La hora '{time}' no cumple el formato HH:MM.")

        #1.Extraer el último dígito de la placa
        last_digit = self._extract_last_digit(plate)
        if last_digit is None:
            #Si no se encuentra ningún dígito en la placa, asumimos (por decisión de diseño)
            # que no hay restricción y retornamos True
            return True

        #2. Obtener el día de la semana (Monday=0, Sunday=6)
        day_of_week = date_obj.weekday()

        # 3.Si es fin de semana, no hay restricción
        if day_of_week >= 5:
            return True

        # 4. Verificar si ese día el dígito está restringido
        if not self._digit_is_restricted_on_day(last_digit, day_of_week):
            return True

        #5. Comprobar si la hora (ya validada y parseada) cae dentro de algún rango de restricción
        for (start_hm, end_hm) in self.RESTRICTION_SCHEDULES:
            start_time = datetime.time(start_hm[0], start_hm[1])
            end_time = datetime.time(end_hm[0], end_hm[1])
            if start_time <= time_obj <= end_time:
                return False  # Está en horario restringido

        return True  #Fuera de horario restringido

    def _extract_last_digit(self, plate: str) -> int:
        """
        Extrae el último dígito de la placa, ignorando letras.
        Por ejemplo: "PBX-1234" -> 4, "HX-244P" -> 4
        Retorna None si no encuentra ningún dígito.
        """
        for char in reversed(plate):
            if char.isdigit():
                return int(char)
        return None

    def _get_day_of_week(self, date_str: str) -> int:
        """
        Convierte la fecha en un objeto datetime y retorna
        el índice del día de la semana (Monday=0, Sunday=6)
        Se espera date_str en formato 'YYYY-MM-DD'.
        """
        try:
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            return date_obj.weekday()
        except ValueError:
            raise ValueError(f"ERROR: La fecha '{date_str}' no cumple con el formato YYYY-MM-DD.")

    def _digit_is_restricted_on_day(self, digit: int, day_of_week: int) -> bool:
        """
        Verifica si el dígito está restringido en ese día.
        """
        if day_of_week not in self.restricted_digits_by_day:
            return False
        return digit in self.restricted_digits_by_day[day_of_week]

    def _time_in_restriction(self, time_str: str) -> bool:
        """
        Determina si la hora dada está dentro de alguno de los rangos de restricción
        :param time_str: Hora en formato "HH:MM" (24-horas)
        :return: True si está en horario restringido, False en caso contrario.
        """
        try:
            hour, minute = map(int, time_str.split(':'))
        except ValueError:
            raise ValueError(f"La hora '{time_str}' no cumple el formato HH:MM.")

        time_obj = datetime.time(hour=hour, minute=minute)
        for (start_hm, end_hm) in self.RESTRICTION_SCHEDULES:
            start_time = datetime.time(start_hm[0], start_hm[1])
            end_time = datetime.time(end_hm[0], end_hm[1])
            if start_time <= time_obj <= end_time:
                return True
        return False
