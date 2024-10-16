from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox, QToolBar
from PyQt6.QtCore import Qt
import sys
import sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        # Call the constructor of the parent class (QMainWindow) using super().
        # This ensures that all the functionality of QMainWindow is properly initialized.
        # Without this call, the QMainWindow part of MainWindow would not be set up correctly,
        # which could cause issues when adding widgets or using built-in features like the status bar, toolbar, etc.
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.resize(600, 400) # set main window size

        # Create menu items
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        # Add student action
        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        # Add search to edit menu and connect the search action
        search_action = QAction(QIcon("icons/search.png"),"Search", self)
        search_action.triggered.connect(self.open_search_dialog)
        edit_menu_item.addAction(search_action)

        # Display data table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))
        self.table.verticalHeader().setVisible(False) # this line disables the default index column of the table
        self.setCentralWidget(self.table)

        # Create toolbar with add and search shortcuts
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)


    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0) # this line resets the table so we don't duplicate the data on each load
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def open_search_dialog(self):
        search_dialog = SearchDialog()
        search_dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        register_button = QPushButton("Register")
        register_button.clicked.connect(self.add_student)
        layout.addWidget(register_button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name,course, mobile) VALUES (?, ?, ?)",
                       (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        main_window.load_data() # this line makes the main window show the newly added row


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_student)
        layout.addWidget(search_button)

        self.setLayout(layout)

    def search_student(self):
        name = self.student_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        #result = cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
        #rows = list(result)
        items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            main_window.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())