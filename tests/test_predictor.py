import pytest
from src.predictor import PicoPlacaPredictor

@pytest.fixture
def predictor():
    """Fixture para reutilizar la instancia del predictor."""
    return PicoPlacaPredictor()

def test_can_circulate_weekend(predictor):
    """
    Los fines de semana no hay restricción
    Independientemente del dígito y hora, debe retornar True
    Por ejemplo aqui use fechas actuales si es que fuera el caso 2025: Sábado (2025-02-15) y Domingo (2025-02-16)
    """
    assert predictor.can_circulate("ABC-1234", "2025-02-15", "08:00") is True
    assert predictor.can_circulate("ABC-9990", "2025-02-16", "17:00") is True

def test_monday_restriction(predictor):
    """
    Lunes (day_of_week = 0) restringe dígitos 1 y 2.
    Verificamos un caso que debe estar restringido y otro que no
    """
    #Placa termina en 1 - Debe estar restringida en horario pico
    assert predictor.can_circulate("AAA-1231", "2025-02-10", "08:00") is False
    #Mismo dígito pero fuera de horario pico (por ej. 10:00) -> True
    assert predictor.can_circulate("AAA-1231", "2025-02-10", "10:00") is True
    #Placa termina en 3 - No está restringida el lunes
    assert predictor.can_circulate("ABC-9993", "2025-02-10", "08:30") is True

def test_friday_restriction(predictor):
    """
    Viernes (day_of_week = 4) restringe dígitos 9 y 0
    """
    #Placa termina en 9, horario pico
    assert predictor.can_circulate("ABC-1299", "2025-02-14", "07:30") is False
    #Placa termina en 0, horario pico
    assert predictor.can_circulate("XYZ-3400", "2025-02-14", "17:00") is False
    #Placa termina en 0, pero fuera del horario pico
    assert predictor.can_circulate("XYZ-3400", "2025-02-14", "20:00") is True

def test_invalid_plate(predictor):
    """
    Si no hay dígitos válidos en la placa, la función podría retornar True (no restringido)
    o se puede cambiar lógica para marcarlo como un caso especial
    """
    #Ejemplo placa sin números
    assert predictor.can_circulate("ABC-XYZ", "2025-02-10", "08:00") is True
