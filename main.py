import sys
import requests
from PyQt5 import QtWidgets
#from sqlalchemy import create_engine
from jsonpath_rw import parse
import json

def get_json_paths(json_data, path=''):
        if isinstance(json_data, dict):
            for k, v in json_data.items():
                new_path = f'{path}.{k}' if path else f'$.{k}'
                yield from get_json_paths(v, new_path)
        elif isinstance(json_data, list) and json_data:
            new_path = f'{path}[*]' if path else '$[*]'
            yield new_path
            yield from get_json_paths(json_data[0], new_path)
        else:
            yield path

class RestRequestDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('REST Request')
        self.setFixedSize(800, 600)
        layout = QtWidgets.QVBoxLayout(self)
        self.url_input = QtWidgets.QLineEdit(self)
        self.url_input.setPlaceholderText('Enter REST endpoint URL')
        layout.addWidget(self.url_input)

        self.request_button = QtWidgets.QPushButton('Make Request', self)
        self.request_button.clicked.connect(self.make_request)
        layout.addWidget(self.request_button)

        self.json_path_list = QtWidgets.QListWidget(self)
        layout.addWidget(self.json_path_list)

        self.confirm_button = QtWidgets.QPushButton('Confirm Selection', self)
        self.confirm_button.clicked.connect(self.confirm_selection)
        layout.addWidget(self.confirm_button)

        self.show_json_button = QtWidgets.QPushButton('Show Raw JSON', self)
        self.show_json_button.clicked.connect(self.show_raw_json)
        layout.addWidget(self.show_json_button)

        self.raw_json_text_edit = QtWidgets.QTextEdit(self)
        self.raw_json_text_edit.setReadOnly(True)
        layout.addWidget(self.raw_json_text_edit)

    def make_request(self):
        response = requests.get(self.url_input.text())
        if response.status_code == 200:
            self.json_data = response.json()
            self.populate_json_paths(self.json_data)

    def populate_json_paths(self, json_data):
        self.json_path_list.clear()
        json_paths = set(get_json_paths(json_data)) 
        for path in json_paths:
            self.json_path_list.addItem(path)

    def show_raw_json(self):
        if hasattr(self, 'json_data'):
            formatted_json = json.dumps(self.json_data, indent=4)  
            self.raw_json_text_edit.setText(formatted_json)

    def confirm_selection(self):
        selected_paths = [item.text() for item in self.json_path_list.selectedItems()]
        self.accept()

class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.rest_request_button = QtWidgets.QPushButton('REST Request', self)
        self.rest_request_button.setGeometry(100, 110, 200, 50)
        self.rest_request_button.clicked.connect(self.show_rest_request_dialog)

    def show_rest_request_dialog(self):
        dialog = RestRequestDialog(self)
        if dialog.exec_():
            pass

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
