from task_manager import TaskManager

def display_menu():
    print("\n--- MENÚ GESTIÓN DE TAREAS ---")
    print("1. Crear nueva tarea")
    print("2. Listar tareas")
    print("3. Actualizar estado de tarea")
    print("4. Eliminar tarea")
    print("5. Salir")

def main():
    manager = TaskManager()

    while True:
        display_menu()
        option = input("Selecciona una opción: ")

        if option == '1':
            title = input("\nTítulo de la tarea: ")
            description = input("Descripción de la tarea: ")
            due_date = input("Fecha de vencimiento (YYYY-MM-DD): ")
            tags = input("Etiquetas (separadas por comas): ").split(",")
            print(manager.create_task(title, description, due_date, tags))

        elif option == '2':
            print("\nTareas Pendientes:")
            print(manager.list_tasks())

        elif option == '3':
            task_index = int(input("\nNúmero de tarea para actualizar el estado: ")) - 1
            new_status = input("Nuevo estado (pending/in_progress/completed): ")
            print(manager.update_task_status(task_index, new_status))

        elif option == '4':
            task_index = int(input("\nNúmero de tarea a eliminar: ")) - 1
            print(manager.delete_task(task_index))

        elif option == '5':
            print("\nSaliendo del gestor de tareas.")
            break

        else:
            print("\nOpción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    main()
