import json
import os
import logging
from datetime import datetime

# Configuración del log
logging.basicConfig(filename="task_manager.log", 
                    level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Clase que representa una tarea
class Task:
    def __init__(self, title, description, due_date, tags):

        # Convertir la fecha ingresada (DD-MM-YYYY) a un objeto datetime
        try:
            self.due_date = datetime.strptime(due_date, "%d-%m-%Y")
        except ValueError:
            logging.error("Error en el formato de la fecha. Use DD-MM-YYYY.")
            raise ValueError("La fecha esta incorrecta. Por favor ingrese una fecha valida.")
        
        self.title = title
        self.description = description
        self.tags = tags
        # Obtener la fecha actual
        current_date = datetime.now()

        # Comparar la fecha de vencimiento con la fecha actual
        if self.due_date < current_date:
            self.status = "Atrasado"
        else:
            self.status = "Pendiente"  # Estado inicial: pendiente

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date.strftime("%d-%m-%Y"),  # Convertir de vuelta a cadena para almacenar
            "tags": self.tags,
            "status": self.status
        }

# Clase que maneja la gestión de tareas
class TaskManager:
    def __init__(self, file_path="tasks.json"):
        self.file_path = file_path
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    logging.error("Error al decodificar el archivo JSON")
                    return []
        else:
            return []

    def save_tasks(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.tasks, file, indent=4)

    def create_task(self, title, description, due_date, tags):
        try:
            task = Task(title, description, due_date, tags)
            self.tasks.append(task.to_dict())
            self.save_tasks()
            logging.info(f"Tarea creada: {title}")
            return f"Tarea '{title}' creada correctamente."
        except ValueError as e:
            logging.error(f"Error al crear tarea: {e}")
            return str(e)

    def list_tasks(self):
        if not self.tasks:
            logging.info("No hay tareas para mostrar.")
            return "No hay tareas creadas."
        task_list = "\n".join([f"{i+1}. {task['title']} - Estado: {task['status']}" for i, task in enumerate(self.tasks)])
        logging.info("Listado de tareas consultado.")
        return task_list

    def update_task_status(self, task_index, new_status):
        try:
            task = self.tasks[task_index]
            if new_status == "Completada":
                self.delete_task(task_index)
                return f"Tarea '{task['title']}' completada y eliminada."
            task["status"] = new_status
            self.save_tasks()
            logging.info(f"Estado de la tarea '{task['title']}' actualizado a '{new_status}'.")
            return f"Estado de la tarea '{task['title']}' actualizado a '{new_status}'."
        except IndexError:
            logging.error("Intento de actualizar una tarea no existente.")
            return "Error: No se encontró la tarea especificada."

    def delete_task(self, task_index):
        try:
            task = self.tasks.pop(task_index)
            self.save_tasks()
            logging.info(f"Tarea eliminada: {task['title']}")
            return f"Tarea '{task['title']}' eliminada correctamente."
        except IndexError:
            logging.error("Intento de eliminar una tarea no existente.")
            return "Error: No se encontró la tarea especificada."
