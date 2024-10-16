from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton, QMainWindow, \
    QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox, QToolBar, QStatusBar
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

        # Create status bar and add elements to it
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect a cell click
        self.table.cellClicked.connect(self.cell_clicked)


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

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        # Clean buttons that could have been created already
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        # Create the buttons in the statusbar
        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
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
        self.accept()


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
        self.accept()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # get student name from selected row
        index = main_window.table.currentRow()
        student_name = main_window.table.item(index, 1).text()

        # get id from selected row
        self.student_id = main_window.table.item(index, 0).text()

        # add student name widget
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # add combo box
        current_course_name = main_window.table.item(index, 2).text()
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(current_course_name)
        layout.addWidget(self.course_name)

        # add mobile widget
        current_mobile = main_window.table.item(index, 3).text()
        self.mobile = QLineEdit(current_mobile)
        self.mobile.setPlaceholderText("Mobile")
        layout.addWidget(self.mobile)

        # add a submit button
        button = QPushButton("Update")
        button.clicked.connect(self.update_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def update_student(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
                      (self.student_name.text(),
                       self.course_name.itemText(self.course_name.currentIndex()),
                       self.mobile.text(),
                       self.student_id))
        connection.commit()
        cursor.close()
        connection.close()
        # refresh the table
        main_window.load_data()
        self.accept()



class DeleteDialog(QDialog):
    pass


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())