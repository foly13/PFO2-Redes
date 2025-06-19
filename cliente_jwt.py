import requests

BASE_URL = "http://127.0.0.1:5000"
token = None

def registrar_usuario():
    usuario = input("Ingrese nombre de usuario: ")
    contraseña = input("Ingrese contraseña: ")
    data = {"usuario": usuario, "contraseña": contraseña}
    r = requests.post(f"{BASE_URL}/registro", json=data)
    print(r.json())

def iniciar_sesion():
    global token
    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ")
    data = {"usuario": usuario, "contraseña": contraseña}
    r = requests.post(f"{BASE_URL}/login", json=data)
    if r.status_code == 200:
        print(r.json()["mensaje"])
        token = r.json()["token"]
    else:
        print(r.json()["mensaje"])

def ver_tareas():
    if not token:
        print("Debés iniciar sesión primero.")
        return
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(f"{BASE_URL}/tareas", headers=headers)
    if r.status_code == 200:
        print(r.text)
    else:
        print(r.json())

def menu():
    while True:
        print("\n=== CLIENTE CON JWT ===")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Ver tareas")
        print("0. Salir")

        opcion = input("Seleccioná una opción: ")

        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            iniciar_sesion()
        elif opcion == "3":
            ver_tareas()
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()
