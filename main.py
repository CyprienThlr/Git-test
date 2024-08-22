import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QPushButton, QListWidget, QCheckBox, QListWidgetItem, QInputDialog, QFrame, QMessageBox, QMenu)
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QPoint
from PyQt5.QtGui import QColor

class TaskWidget(QWidget):
    def __init__(self, title, xp, repeat, modify_task_callback, delete_task_callback, complete_task_callback):
        super().__init__()
        self.title = title
        self.xp = xp
        self.repeat = repeat
        self.modify_task_callback = modify_task_callback
        self.delete_task_callback = delete_task_callback
        self.complete_task_callback = complete_task_callback

        layout = QHBoxLayout()
        layout.setContentsMargins(15, 10, 15, 10)
        self.setLayout(layout)
        self.setStyleSheet("background-color: #f0e5f9; border-radius: 10px;")

        self.checkbox = QCheckBox()
        self.checkbox.stateChanged.connect(self.complete_task)
        layout.addWidget(self.checkbox)

        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("font-size: 16px; color: #4a4a4a;")
        layout.addWidget(self.title_label, stretch=1)

        self.xp_label = QLabel(f"{xp} XP")
        self.xp_label.setStyleSheet("font-size: 14px; color: #666666;")
        layout.addWidget(self.xp_label)

        self.menu_button = QPushButton("⋮")
        self.menu_button.setStyleSheet("background-color: transparent; border: none; font-size: 16px; color: #666666;")
        self.menu_button.clicked.connect(self.show_menu)
        layout.addWidget(self.menu_button)

    def show_menu(self):
        menu = QMenu(self)
        modify_action = menu.addAction("Modifier")
        delete_action = menu.addAction("Supprimer")
        menu.addSeparator()
        repeat_menu = menu.addMenu("Répétition")
        repeat_daily_action = repeat_menu.addAction("Tous les jours")
        repeat_weekly_action = repeat_menu.addAction("Toutes les semaines")
        repeat_once_action = repeat_menu.addAction("Une seule fois")
        repeat_continuous_action = repeat_menu.addAction("En continu")

        modify_action.triggered.connect(self.modify_task)
        delete_action.triggered.connect(self.delete_task)
        repeat_daily_action.triggered.connect(lambda: self.set_repeat("daily"))
        repeat_weekly_action.triggered.connect(lambda: self.set_repeat("weekly"))
        repeat_once_action.triggered.connect(lambda: self.set_repeat("once"))
        repeat_continuous_action.triggered.connect(lambda: self.set_repeat("continuous"))

        menu.exec_(self.menu_button.mapToGlobal(QPoint(0, 0)))

    def set_repeat(self, repeat):
        self.repeat = repeat

    def modify_task(self):
        title, ok = QInputDialog.getText(self, "Modifier la tâche", "Entrez le nouveau titre de la tâche:", text=self.title)
        if ok and title:
            xp, ok = QInputDialog.getInt(self, "Modifier la tâche", "Entrez la nouvelle valeur d'XP:", value=self.xp)
            if ok:
                self.title_label.setText(title)
                self.xp_label.setText(f"{xp} XP")
                self.title = title
                self.xp = xp

    def delete_task(self):
        self.delete_task_callback(self)

    def complete_task(self):
        if self.checkbox.isChecked():
            self.complete_task_callback(self)
            if self.repeat == "once":
                self.delete_task()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LifeRPG App")
        self.setGeometry(100, 100, 420, 650)
        self.setStyleSheet("background-color: #fff; font-family: Arial;")
        self.level = 1
        self.current_xp = 0
        self.xp_for_next_level = 10000
        self.last_level_reached = 1

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # Profile section
        profile_layout = QVBoxLayout()
        main_layout.addLayout(profile_layout)

        header_layout = QHBoxLayout()
        profile_layout.addLayout(header_layout)

        # Avatar and Username
        self.avatar_label = QLabel()
        self.avatar_label.setFixedSize(50, 50)
        self.avatar_label.setStyleSheet("border-radius: 25px; background-color: #9ad0f5;")
        header_layout.addWidget(self.avatar_label)

        self.username_label = QLabel("Username")
        self.username_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #4a4a4a; margin-left: 10px;")
        header_layout.addWidget(self.username_label)

        self.level_label = QLabel(f"Level {self.level}")
        self.level_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #828282; margin-left: 10px;")
        header_layout.addWidget(self.level_label)

        xp_layout = QHBoxLayout()
        profile_layout.addLayout(xp_layout)

        self.xp_bar = QProgressBar()
        self.xp_bar.setValue(0)  # Empty bar
        self.xp_bar.setMaximum(self.xp_for_next_level)
        self.xp_bar.setTextVisible(False)
        self.xp_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #d6d6d6;
                border-radius: 10px;
                background-color: #ededed;
            }
            QProgressBar::chunk {
                background-color: #9ad0f5;
                border-radius: 10px;
                margin: 0.5px;
            }
        """)
        xp_layout.addWidget(self.xp_bar, stretch=1)

        self.points_label = QLabel("Points: 0")
        self.points_label.setStyleSheet("font-size: 12px; color: #666666;")
        xp_layout.addWidget(self.points_label)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        divider.setStyleSheet("background-color: #cccccc; margin-top: 10px;")
        main_layout.addWidget(divider)

        # Task list section
        self.task_list = QListWidget()
        self.task_list.setStyleSheet("background-color: #f5f5f5; border: none; padding: 5px;")
        main_layout.addWidget(self.task_list)

        # Add task button
        add_task_button = QPushButton("+")
        add_task_button.setFixedSize(70, 70)
        add_task_button.setStyleSheet("""
            QPushButton {
                border: 2px solid #9ad0f5;
                border-radius: 35px;
                background-color: #ffffff;
                color: #9ad0f5;
                font-size: 24px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e6f7ff;
            }
        """)
        add_task_button.clicked.connect(self.add_task_dialog)

        # Floating button container
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(add_task_button)
        button_layout.setAlignment(Qt.AlignRight)
        main_layout.addLayout(button_layout)

    def add_task_dialog(self):
        title, ok = QInputDialog.getText(self, "Nouvelle Tâche", "Entrez le titre de la tâche :")
        if ok and title:
            xp, ok = QInputDialog.getInt(self, "Nouvelle Tâche", "Entrez la valeur d'XP :")
            if ok:
                repeat, ok = QInputDialog.getItem(self, "Nouvelle Tâche", "Sélectionnez la répétition :", ["once", "daily", "weekly", "continuous"], 0, False)
                if ok:
                    self.add_task(title, xp, repeat)

    def add_task(self, title, xp, repeat):
        task = TaskWidget(title, xp, repeat, self.modify_task, self.delete_task, self.complete_task)
        task_item = QListWidgetItem(self.task_list)
        task_item.setSizeHint(task.sizeHint() + QSize(0, 20))  # Increase height
        self.task_list.setItemWidget(task_item, task)

        # Animation for adding task
        task_anim = QPropertyAnimation(task, b"pos")
        task_anim.setDuration(500)
        task_anim.setStartValue(QPoint(0, -50))
        task_anim.setEndValue(QPoint(0, 0))
        task_anim.start()

    def modify_task(self, task_widget):
        title, ok = QInputDialog.getText(self, "Modifier la tâche", "Entrez le nouveau titre de la tâche:", text=task_widget.title)
        if ok and title:
            xp, ok = QInputDialog.getInt(self, "Modifier la tâche", "Entrez la nouvelle valeur d'XP:", value=task_widget.xp)
            if ok:
                task_widget.title_label.setText(title)
                task_widget.xp_label.setText(f"{xp} XP")
                task_widget.title = title
                task_widget.xp = xp

    def delete_task(self, task_widget):
        task_widget.deleteLater()

    def complete_task(self, task_widget):
        if task_widget.repeat == "once":
            self.delete_task(task_widget)
        elif task_widget.repeat == "continuous":
            task_widget.checkbox.setChecked(False)  # Uncheck task if continuous

        # Add XP for completed task
        self.add_xp(task_widget.xp)

    def add_xp(self, xp_amount):
        self.current_xp += xp_amount

        while self.current_xp >= self.xp_for_next_level:
            excess_xp = self.current_xp - self.xp_for_next_level
            self.last_level_reached = self.level
            self.level_up()
            self.current_xp = excess_xp

        self.xp_bar.setValue(self.current_xp)
        self.points_label.setText(f"Points: {self.current_xp}/{self.xp_for_next_level}")

    def level_up(self):
        self.level += 1
        self.xp_for_next_level += 5000
        self.xp_bar.setMaximum(self.xp_for_next_level)
        self.xp_bar.setValue(0)
        self.level_label.setText(f"Level {self.level}")

        # Show congratulation message only for the last level up
        if self.level > self.last_level_reached:
            QMessageBox.information(self, "Niveau Supérieur!", f"Félicitations, vous avez atteint le niveau {self.level}!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
