from predictor import PicoPlacaPredictor

def main():
    """
    Ejemplo de uso interactivo del predictor.
    Aqui dejo para personalizar la forma de entrada/salida preferida
    """
    print("=== Pico y Placa Predictor ===")
    print("Por favor, ingresa la información solicitada.\n")

    plate = input("Número de placa (ej. PBX-1234): ").strip()
    date_str = input("Fecha (formato YYYY-MM-DD, ej. 2025-02-10): ").strip()
    time_str = input("Hora (formato HH:MM en 24h, ej. 08:30): ").strip()

    predictor = PicoPlacaPredictor()
    can_drive = predictor.can_circulate(plate=plate, date=date_str, time=time_str)

    if can_drive:
        print(f"\nEl vehículo con placa {plate} SÍ puede circular en esa fecha y hora.")
    else:
        print(f"\nEl vehículo con placa {plate} NO puede circular en esa fecha y hora")

if __name__ == "__main__":
    main()
