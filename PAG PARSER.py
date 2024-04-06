import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QTextEdit, QDialog, QAction, QMenu, QFileDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
from datetime import datetime


# made by crunchy , free to use but do not use sell , or claim this as your own. Thanks. This is the public version.

class CustomTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

    def showContextMenu(self, pos):
        context_menu = QMenu(self)

        
        delete_all_action = QAction("Delete All", self)
        delete_all_action.triggered.connect(self.clear)
        context_menu.addAction(delete_all_action)

        delete_last_query_action = QAction("Delete Last Query", self)
        delete_last_query_action.triggered.connect(self.deleteLastQuery)
        context_menu.addAction(delete_last_query_action)

        create_txt_action = QAction("Create TXT", self)
        create_txt_action.triggered.connect(self.createTxt)
        context_menu.addAction(create_txt_action)

        context_menu.exec_(self.mapToGlobal(pos))

    def deleteLastQuery(self):
        cursor = self.textCursor()
        if cursor.hasSelection():
            cursor.movePosition(QTextCursor.StartOfBlock, QTextCursor.KeepAnchor)
            cursor.removeSelectedText()

    def createTxt(self):
        text = self.toPlainText()
        if text:
            current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            file_name = f"console_output_{current_datetime}.txt"
            with open(file_name, 'w') as file:
                file.write(text)

class PokemonSearchDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Search Pokemon')
        self.setGeometry(200, 200, 400, 300)

        self.search_label = QLabel('Enter Pokemon Name:')
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.search_pokemon)

        self.pokemon_list = CustomTextEdit()
        self.pokemon_list.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.search_label)
        layout.addWidget(self.search_input)
        layout.addWidget(self.pokemon_list)

        self.setLayout(layout)

        self.fetch_pokemon_names()

    def fetch_pokemon_names(self):
        try:
            response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1000")
            if response.status_code == 200:
                data = response.json()
                pokemon_names = []
                for pokemon in data["results"]:
                    pokemon_names.append(f'{pokemon["url"].split("/")[-2]}: {pokemon["name"].capitalize()}')
                self.pokemon_list.setPlainText("\n".join(pokemon_names))
            else:
                self.pokemon_list.setPlainText("Failed to fetch Pokemon names")
        except Exception as e:
            print("Error fetching Pokemon names:", e)
            self.pokemon_list.setPlainText("Failed to fetch Pokemon names")

    def search_pokemon(self):
        search_text = self.search_input.text().lower()
        if not search_text:
            self.fetch_pokemon_names()
        else:
            pokemon_list = self.pokemon_list.toPlainText().split('\n')
            filtered_pokemon = [line for line in pokemon_list if search_text in line.lower()]
            self.pokemon_list.setPlainText('\n'.join(filtered_pokemon))

class StatsInputApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.league_data = {
            "ultra": {
                1: [0, 15, 15],
                2: [15, 15, 15],
                3: [15, 15, 15]
            },
            "great": {
                1: [1, 15, 15],
                2: [1, 15, 15],
                3: [1, 15, 15]
            },
            "little": {
                1: [2, 15, 15],
                2: [2, 15, 15],
                3: [2, 15, 15]
            }
        }
        self.selected_league = None

    def initUI(self):
        self.setWindowTitle('Crunchy - pvp')
        self.setGeometry(100, 100, 400, 300)

        self.command_input = QLineEdit(placeholderText='Enter Command')
        self.command_input.returnPressed.connect(self.on_next_button_clicked)

        self.enter_button = QPushButton('Enter')
        self.enter_button.clicked.connect(self.on_next_button_clicked)

        self.ultra_button = QPushButton('Ultra League')
        self.ultra_button.clicked.connect(self.on_ultra_button_clicked)

        self.great_button = QPushButton('Great League')
        self.great_button.clicked.connect(self.on_great_button_clicked)

        self.little_button = QPushButton('Little Cup')
        self.little_button.clicked.connect(self.on_little_button_clicked)

        self.console = CustomTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet("font-size: 14px;")  

        self.search_button = QPushButton('Search Pokemon')
        self.search_button.clicked.connect(self.open_search_dialog)

        main_layout = QVBoxLayout()

        command_layout = QHBoxLayout()
        command_layout.addWidget(self.command_input)
        command_layout.addWidget(self.enter_button)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ultra_button)
        button_layout.addWidget(self.great_button)
        button_layout.addWidget(self.little_button)

        main_layout.addLayout(command_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.console)
        main_layout.addWidget(self.search_button)

        self.setLayout(main_layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #111;
                color: #ddd;
                font-family: Arial, sans-serif;
            }
            QLabel {
                font-size: 14px;
            }
            QLineEdit {
                font-size: 14px;
                padding: 5px;
                background-color: #222;
                border: 1px solid #444;
                color: #fff;
            }
            QPushButton {
                font-size: 14px;
                padding: 5px 10px;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #333;
            }
        """)

    def open_search_dialog(self):
        dialog = PokemonSearchDialog(self)
        dialog.exec_()

    def on_next_button_clicked(self):
        commands = self.command_input.text().split(',')
        results = []

        for command in commands:
            try:
                command_int = int(command.strip())
                if not self.selected_league:
                    raise ValueError("Please select a league first.")
                league_name = self.selected_league.lower()
                league_data = self.league_data[league_name].get(command_int)
                if league_data:
                    result_str = f"{command_int},{','.join(map(str, league_data))}"  
                    results.append(result_str)
                else:
                    results.append(f"No data found for command {command}.")
            except ValueError:
                results.append(f"Invalid command: {command}")

        self.console.append('\n'.join(results))  

    def on_ultra_button_clicked(self):
        self.reset_league_buttons()
        self.selected_league = "Ultra"
        self.ultra_button.setStyleSheet("background-color: #007bff; color: #fff;")

    def on_great_button_clicked(self):
        self.reset_league_buttons()
        self.selected_league = "Great"
        self.great_button.setStyleSheet("background-color: #007bff; color: #fff;")

    def on_little_button_clicked(self):
        self.reset_league_buttons()
        self.selected_league = "Little"
        self.little_button.setStyleSheet("background-color: #007bff; color: #fff;")

    def reset_league_buttons(self):
        self.selected_league = None
        self.ultra_button.setStyleSheet("background-color: #222; color: #fff;")
        self.great_button.setStyleSheet("background-color: #222; color: #fff;")
        self.little_button.setStyleSheet("background-color: #222; color: #fff;")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    stats_input_app = StatsInputApp()
    stats_input_app.show()
    sys.exit(app.exec_())
