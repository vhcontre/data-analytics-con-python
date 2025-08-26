# backend/app/console/main_console.py
from app.console.producto_console import main as producto_menu


def main_menu():
    while True:
        print("\n===== MENÚ PRINCIPAL =====")
        print("1. Gestión de Productos")        
        print("0. Salir")

        opcion = input("Ingrese una opción: ").strip()

        if opcion == "1":
            producto_menu()        
        elif opcion == "0":
            print("¡Hasta luego!")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

if __name__ == "__main__":
    main_menu()
