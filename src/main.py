from predictor import PicoPlacaPredictor

#Refactorizacion:
import datetime

def main():
    print("=== Pico y Placa Predictor ===")
    predictor = PicoPlacaPredictor()

    while True:
        plate = input("Número de placa (ej. PBX-1234): ").strip()
        date_str = input("Fecha (formato YYYY-MM-DD, ej. 2025-02-10): ").strip()
        time_str = input("Hora (formato HH:MM en 24h, ej. 08:30): ").strip()

        error_msgs = []

        #Validar la fecha
        try:
            datetime.datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            error_msgs.append(f"La fecha '{date_str}' no cumple con el formato YYYY-MM-DD.")

        #Validar la hora
        try:
            hour, minute = map(int, time_str.split(':'))
            datetime.time(hour, minute)
        except ValueError:
            error_msgs.append(f"La hora '{time_str}' no cumple el formato HH:MM.")

        # Si hay errores, se muestran y se vuelve a pedir la entrada
        if error_msgs:
            print("\nEntrada inválida:")
            for msg in error_msgs:
                print(msg)
            print("Inténtalo nuevamente.\n")
            continue

        #Si la validación previa pasó, llamamos a la lógica de negocio.
        try:
            can_drive = predictor.can_circulate(plate=plate, date=date_str, time=time_str)
        except ValueError as e:
            #En teoría, no se debería llegar aquí, ya que ya validamos.
            print(f"\nEntrada inválida: {e}. Inténtalo nuevamente.\n")
            continue

        if can_drive:
            print(f"\nEl vehículo con placa {plate} SÍ puede circular en esa fecha y hora.\n")
        else:
            print(f"\nEl vehículo con placa {plate} NO puede circular en esa fecha y hora.\n")
        break

if __name__ == "__main__":
    main()
