import PyQt5
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit, QListWidget

tasks = []
task_counter = 1  # Compteur pour les numéros de tâches

def NewTask(task_text):
    global task_counter
    numbered_task = f"{task_text}{task_counter}"
    tasks.append(numbered_task)
    task_counter += 1
    update_task_list()

def update_task_list():
    task_list_widget.clear()
    task_list_widget.addItems(tasks)

class TaskManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Task Manager")
        self.setGeometry(100, 100, 400, 300)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter new task")
        layout.addWidget(self.task_input)

        add_task_button = QPushButton("Add Task")
        add_task_button.clicked.connect(self.add_task)
        layout.addWidget(add_task_button)

        global task_list_widget
        task_list_widget = QListWidget()
        layout.addWidget(task_list_widget)

    def add_task(self):
        task_text = self.task_input.text()
        if task_text:
            NewTask(task_text)
            self.task_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TaskManager()
    window.show()
    sys.exit(app.exec_())
