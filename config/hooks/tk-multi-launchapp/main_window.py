from sgtk.platform.qt import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QMessageBox
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Create and Read Example")
        self.setGeometry(300, 300, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Enter text here")
        self.layout.addWidget(self.input_field)

        self.add_button = QPushButton("Add", self)
        self.add_button.clicked.connect(self.add_item)
        self.layout.addWidget(self.add_button)

        self.list_widget = QListWidget(self)
        self.layout.addWidget(self.list_widget)

    def add_item(self):
        text = self.input_field.text()
        if text:
            self.list_widget.addItem(text)
            self.input_field.clear()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter some text.")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()