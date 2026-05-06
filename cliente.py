import requests
import webbrowser

# URL base del servidor Flask
URL = "http://127.0.0.1:5000"

def menu():
    while True:
        print("\n--- Cliente de Consola ---")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Ver tareas")
        print("4. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            # Registro de usuario
            usuario = input("Usuario: ")
            contrasena = input("Contraseña: ")
            r = requests.post(f"{URL}/registro", json={"usuario": usuario, "contraseña": contrasena})
            print(r.json(), r.status_code)

        elif opcion == "2":
            # Login de usuario
            usuario = input("Usuario: ")
            contrasena = input("Contraseña: ")
            r = requests.post(f"{URL}/login", json={"usuario": usuario, "contraseña": contrasena})
            print(r.json(), r.status_code)

        elif opcion == "3":
            # Consultar tareas: muestra HTML en consola y abre navegador
            r = requests.get(f"{URL}/tareas")
            print("Contenido HTML recibido:\n", r.text)

            # Abrimos la página en el navegador para ver estilos aplicados
            webbrowser.open(f"{URL}/tareas")

        elif opcion == "4":
            print("Saliendo del cliente...")
            break

        else:
            print("Opción inválida")

# Punto de entrada principal
if __name__ == "__main__":
    menu()
