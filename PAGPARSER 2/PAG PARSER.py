import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QTextEdit, QDialog, QAction, QMenu, QFileDialog, QMessageBox, QInputDialog, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor ,  QIcon
from datetime import datetime

class HowToUseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Info')
        self.setGeometry(200, 200, 400, 300)
        self.instructions_label = QLabel("How to use tool / info:\n\n"
        "1. COMMANDS:\n\n"
        "• Commas \n"
        "comma example: 1,2,3,4,5 \n"
        "This will show dex # (1 2 3 4 5) only! \n\n"
                                         
        "•Dashes \n"
        "Dash example: 1-250\n"
        "This will show dex # 1 though 250 only! \n\n"
                                         
        "•Breaks \n"
        "Breaks example: 1-5;100-200\n"
        "This will show dex # 1-5 then skip to 100-200 \n\n"
                                         
        "2. Data Source:\n\n"
        "Data is provided by 'pvpoke.com' , all data is manaully reviewed.\n"
        "Rest assured, all data is correct!\n\n"

        "3. Credits:\n\n"
        "Script and Data was created by Crunchy. \n"
        "Special thanks to others for helping with this long script :)"




                                         )
                                          
        layout = QVBoxLayout()
        layout.addWidget(self.instructions_label)
        layout.setAlignment(Qt.AlignTop)
        self.setLayout(layout)

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
        
            default_filename = 'output.txt'
            file_name, ok = QInputDialog.getText(self, 'Save as TXT', 'Enter filename:', text=default_filename)
            if ok and file_name.strip():  
                file_path = file_name.strip()
                if not file_path.endswith('.txt'):
                    file_path += '.txt'
                try:
                    with open(file_path, 'w') as file:
                        file.write(text)
                    QMessageBox.information(self, 'Success', f'Text saved as {file_path}')
                except Exception as e:
                    QMessageBox.critical(self, 'Error', f'Error occurred while saving: {str(e)}')
            elif not file_name.strip():
                QMessageBox.warning(self, 'Warning', 'Filename cannot be empty.')
        else:
            QMessageBox.warning(self, 'Warning', 'There is no text to save.')

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
            "ultra": [
                # kanto 1-151 (gen 1) (UL)
                (3, [1, 15, 14]), #Venusaur
                (6, [0, 13, 15]), #Charizard
                (9, [0, 12, 15]), #Blastoise
                (15, [15, 15, 15]), #Beedrill
                (18, [15, 15, 15]), #Pidgeot
                (20, [15, 15, 15]), #Raticate (Alolan)
                (24, [15, 15, 15]), #Arbok
                (28, [0, 14, 15]), #Sandslash (Alolan)
                (28, [2, 14, 15]), # Sandslash
                (31, [0, 14, 15]), # Nidoqueen
                (34, [0, 14, 14]), # Nidoking
                (38, [9, 15, 15]), # Ninetales
                (38, [7, 15, 15]), # Ninetales (Alolan)
                (42, [15, 15, 15]), # Golbat
                (45, [0, 15, 14]), # Vileplume
                (49, [15, 15, 15]), # Venomoth
                (55, [0, 13, 13]), # Golduck    
                (59, [0, 15, 15]), # Arcanine
                (62, [0, 14, 14]), # Poliwrath
                (65, [0, 14, 15]), #Alakazam
                (67, [15, 15, 15]), #Machoke
                (68, [0, 15, 14]), #Machamp
                (71, [0, 15, 12]), # Victreebel
                (73, [0, 13, 15]), # Tentacruel
                (75, [15, 15, 15]), #Graveler / Alolan Graveler(same  R1 ivs)
                (76, [0, 15, 15]), # Golem / Alolan Golem (same  R1 ivs)
                (80, [0, 14, 14]), # Slowbro
                (82, [0, 15, 15]), # Magneton
                (89, [0, 15, 15]), # Muk / Muk (Alolan) (same  R1 ivs)
                (91, [0, 14, 14]), # Cloyster
                (94, [0, 15, 14]), # Gengar 
                (97, [15, 15, 15]), # Hypno
                (101, [15, 15, 15]), # Electrode
                (103, [1, 15, 15]), # Exeggutor / Exeggutor (Alolan)(same  R1 ivs)
                (105, [15, 15, 15]), # Marowak / Marowak (Alolan)(same  R1 ivs)
                (106, [0, 14, 15]), # Hitmonlee
                (107, [4, 15, 15]), # Hitmonchan
                (110, [8, 15, 15]), # Weezing
                (112, [0, 14, 14]), # Rhydon
                (114, [12, 15, 15]), # Tangela
                (117, [15, 15, 15]), # Seadra
                (123, [0, 13, 15]), # Scyther
                (125, [5, 15, 15]), # Electabuzz
                (126, [0, 14, 15]), # Magmar
                (127, [0, 14, 15]), # Pinsir
                (130, [0, 15, 13]), # Gyarados
                (131, [0, 15, 15]), # Lapras
                (139, [0, 14, 15]), # Omastar
                (142, [0, 13, 15]), # Aerodactyl
                (143, [0, 12, 15]), # Snorlax
                (144, [6, 14, 15]), # Articuno
                (145, [8, 15, 14]), # Zapdos 
                (146, [7, 15, 15]), # Moltres
                (149, [0, 13, 15]), # Dragonite
                (150, [7, 15, 14]), # Mewtwo

                # johto 152-251 (gen 2) (UL)
                (154, [0, 14, 15]), #Meganium
                (157, [0, 13, 15]), #Typhlosion
                (160, [1, 15, 14]), #Feraligatr 
                (169, [0, 15, 14]), #Crobat
                (178, [15, 15, 15]), #Xatu
                (181, [0, 13, 15]), #Ampharos
                (182, [9, 15, 15]), #Bellossom
                (185, [15, 15, 15]), #Sudowoodo
                (186, [0, 15, 14]), #Politoed
                (189, [15, 15, 15]), # Jumpluff
                (195, [15, 15, 15]), #Quagsire
                (199, [0, 14, 14]), #Slowking
                (200, [15, 15, 15]), # Misdreavus
                (203, [15, 15, 15]), # Girafarig
                (205, [9, 15, 15]), #Forretress
                (207, [15, 15, 15]),  #Gligar
                (208, [2, 15, 15]), #Steelix
                (210, [0, 15, 14]), #Granbull
                (212, [0, 15, 15]), #Scizor
                (215, [15, 15, 15]), #Sneasel / Hisuian Sneasel (same  R1 ivs)
                (217, [0, 15, 13]), #Ursaring
                (221, [5, 15, 12]), #Piloswine
                (227, [15, 15, 15]), # Skarmory
                (229, [0, 15, 14]), # Houndoom
                (230, [0, 15, 15]), # Kingdra
                (232, [0, 15, 15]), #Donphan
                (233, [1, 15, 15]), #Porygon2 
                (234, [15, 15, 15]), #Stantler
                (237, [15, 15, 15]), #Hitmontop 
                (243, [6, 13, 13]), #Raikou
                (244, [7, 15, 15]), #Entei
                (245, [6, 13, 13]), #Suicune
                (248, [0, 13, 11]), #Tyranitar
                (249, [7, 15, 15]), #Lugia
                (250, [1, 15, 14]), # Ho-Oh
                
  

                #hoenn 252-386 (gen 3) (UL)

                (254, [0, 15, 13]), #Sceptile
                (257, [1, 15, 15]), #Blaziken 
                (259, [15, 15, 15]), #Marshtomp
                (260, [0, 14, 13]), #Swampert
                (262, [15, 15, 15]), #Mightyena
                (275, [3, 15, 15]), #Shiftry
                (282, [0, 12, 15]), #Gardevoir
                (295, [4, 15, 14]), #Exploud
                (297, [1, 15, 15]), #Hariyama
                (305, [15, 15, 15]), #Lairon
                (306, [0, 13, 15]), #Aggron
                (310, [2, 15, 15]), #Manectric
                (319, [15, 15, 15]), #Sharpedo
                (321, [9, 15, 15]), # Wailord
                (323, [15, 15, 15]), #Camerupt
                (326, [3, 14, 15]), #Grumpig
                (330, [0, 13, 15]), #Flygon
                (332, [6, 15, 15]), #Cacturne
                (340, [15, 15, 15]), #Whiscash
                (342, [0, 15, 15]), #Crawdaunt
                (346, [15, 15, 15]), #Cradily 
                (348, [2, 15, 15]), #Armaldo
                (354, [6, 15, 15]), #Banette
                (359, [0, 15, 14]), #Absol
                (362, [15, 15, 15]), #Glalie
                (364, [15, 15, 15]), # Sealeo
                (365, [0, 15, 15]), #Walrein
                (372, [15, 15, 15]), #Shelgon
                (373, [1, 15, 15]), #Salamence
                (375, [15, 15, 15]), #Metang
                (376, [0, 15, 13]), #Metagross
                (377, [6, 14, 14]), #Regirock
                (378, [6, 14, 14]), #Regice
                (379, [6, 11, 15]), #Registeel 
                (380, [6, 15, 13]), #Latias
                (381, [9, 15, 14]), #Latios
                (382, [6, 15, 14]), #Kyogre 
                (383, [6, 15, 14]), #Groudon

                #Sinnoh 387-492 (gen 4) (UL)

                (388, [15, 15, 15]), #Grotle
                (389, [0, 15, 15]), #Torterra
                (392, [1, 15, 14]), #Infernape
                (395, [1, 15, 14]), #Empoleon
                (398, [2, 15, 14]), #Staraptor
                (400, [15, 15, 15]), #Bibarel
                (405, [0, 15, 15]), #Luxray
                (409, [0, 14, 15]), #Rampardos
                (411, [15, 15, 15]), #Bastiodon
                (424, [0, 15, 14]), #Ambipom
                (426, [1, 15, 15]), #Drifblim
                (429, [0, 14, 15]), #Mismagius
                (430, [0, 15, 15]), #Honchkrow
                (432, [15, 15, 15]), #Purugly
                (435, [3, 15, 14]), #Skuntank
                (444, [15, 15, 15]), #Gabite
                (445, [0, 14, 13]), #Garchomp
                (450, [0, 14, 15]), #Hippowdon
                (452, [0, 15, 15]), #Drapion
                (454, [0, 15, 12]), #Toxicroak
                (460, [3, 15, 14]), #Abomasnow
                (461, [0, 14, 15]), #Weavile
                (462, [0, 15, 15]), #Magnezone 
                (464, [0, 14, 14]), #Rhyperior
                (465, [0, 14, 15]), #Tangrowth
                (466, [1, 15, 15]), #Electivire
                (467, [1, 15, 15]), #Magmortar 
                (472, [0, 14, 15]), #Gliscor
                (473, [0, 15, 13]), #Mamoswine
                (474, [0, 13, 14]), #Porygon-Z
                (475, [0, 12, 15]), #Gallade
                (476, [15, 15, 15]), #Probopass
                (477, [0, 15, 15]), #Dusknoir
                (478, [15, 15, 15]), #Froslass
                (486, [6, 13, 11]), #Regigigas

                 #Unova 494-649 (gen 5) (UL)
                
                (521, [2, 15, 13]), #Unfezant
                (523, [0, 13, 15]), #Zebstrika
                (530, [0, 15, 15]), #Excadrill
                (538, [0, 14, 15]), #Throh
                (539, [0, 15, 11]), #Sawk
                (558, [0, 14, 15]), #Crustle
                (576, [0, 14, 15]), #Gothitelle
                (579, [0, 13, 14]), #Reuniclus
                (581, [15, 15, 15]), #Swanna
                (591, [15, 15, 15]), #Amoonguss
                (596, [15, 15, 15]), #Galvantula
                (598, [7, 14, 15]), #Ferrothorn
                (609, [0, 15, 12]), #Chandelure
                (623, [0, 13, 14]), #Golurk      
                
            ],            
            "great": [
                # kanto 1-151 (gen 1) (GL)
                (1, [15, 15, 15]), #Bulbasaur
                (2, [0, 13, 14]), #Ivysaur
                (3, [0, 14, 11]), #Venusaur
                (5, [0, 13, 15]), #Charmeleon
                (6, [0, 15, 13]), #Charizard 
                (8, [0, 14, 15]), #Wartortle
                (9, [1, 15, 15]), #Blastoise
                (15, [0, 13, 14]), #Beedrill
                (17, [15, 15, 15]), #Pidgeotto
                (18, [0, 14, 14]), #Pidgeot
                (20, [0, 14, 15]), #Raticate
                (20, [0, 13, 14]), #Raticate (Alolan)
                (24, [0, 11, 14]), #Arbok
                (27, [15, 15, 15]), #Sandshrew / Sandshrew (Alolan)
                (28, [0, 14, 15]), # Sandslash
                (28, [0, 14, 14]), # Sandslash (Alolan)
                (30, [15, 15, 15]), #Nidorina
                (31, [0, 15, 12]), #Nidoqueen
                (33, [8, 15, 15]), #Nidorino
                (34, [0, 14, 15]), #Nidoking
                (38, [0, 15, 15]), #Ninetales
                (38, [0, 14, 12]), #Ninetales (Alolan)
                (42, [0, 15, 15]), #Golbat
                (43, [15, 15, 15]), #Oddish
                (44, [0, 12, 14]), #Gloom
                (45, [0, 15, 15]), #Vileplume
                (49, [0, 13, 15]), #Venomoth
                (51, [0, 15, 13]), #Dugtrio
                (51, [0, 12, 15]), #Dugtrio (Alolan)
                (53, [0, 14, 13]), #Persian
                (55, [0, 10, 14]), #Golduck
                (58, [15, 15, 15]), #Growlithe
                (59, [0, 14, 15]), #Arcanine
                (61, [6, 15, 15]), #Poliwhirl
                (62, [0, 14, 15]), #Poliwrath
                (65, [1, 15, 15]), #Alakazam
                (66, [15, 15, 15]), #Machop
                (67, [0, 15, 15]), #Machoke
                (68, [0, 14, 11]), #Machamp
                (70, [1, 15, 15]), #Weepinbell
                (71, [1, 15, 15]), #Victreebel
                (73, [1, 15, 15]), #Tentacrue
                (74, [15, 15, 15]), #Geodude/ Geodude (Alolan)
                (75, [0, 14, 15]), #Graveler / Graveler (Alolan)
                (76, [1, 14, 15]), # Golem / Golem (Alolan)
                (79, [15, 15, 15]), #Slowpoke
                (80, [0, 13, 15]), #Slowbro
                (81, [12, 15, 13]), #Magnemite
                (82, [0, 15, 15]), #Magneton
                (88, [10, 15, 14]), #Grimer / Grimer (Alolan)
                (89, [0, 15, 15]), #Muk / Muk (Alolan)
                (91, [0, 13, 13]), #Cloyster
                (93, [1, 15, 14]), #Haunter
                (94, [0, 13, 13]), #Gengar
                (95, [15, 15, 15]), #Onix
                (96, [15, 15, 15]), #Drowzee
                (97, [0, 13, 13]), #Hypno
                (101, [1, 15, 15]), #Electrode
                (102, [15, 15, 15]), #Exeggcute
                (103, [1, 15, 14]), #Exeggutor / Exeggutor (Alolan)
                (104, [15, 15, 15]), #Cubone
                (105, [0, 14, 14]), #Marowak / Marowak (Alolan)
                (106, [2, 15, 15]), #Hitmonlee
                (107, [0, 11, 15]), #Hitmonchan
                (109, [15, 15, 15]), #Koffing
                (110, [0, 14, 14]), #Weezing
                (111, [0, 13, 15]), #Rhyhorn
                (112, [2, 15, 14]), #Rhydon
                (114, [0, 13, 15]), #Tangela
                (117, [1, 15, 14]), #Seadra
                (123, [0, 14, 11]), #Scyther
                (125, [0, 14, 11]), #Electabuzz
                (126, [0, 15, 15]), #Magmar
                (127, [0, 13, 14]), #Pinsir
                (130, [0, 14, 15]), #Gyarados
                (131, [0, 10, 14]), #Lapras
                (137, [0, 13, 15]), #Porygon
                (138, [0, 13, 15]), #Omanyte
                (139, [0, 9, 15]), #Omastar
                (142, [1, 15, 15]), #Aerodactyl
                (143, [1, 15, 14]), #Snorlax 
                (144, [6, 15, 14]), #Articuno
                (145, [6, 15, 12]), #Zapdos
                (146, [6, 10, 12]), #Moltres
                (148, [1, 15, 15]), #Dragonair 
                (149, [3, 15, 14]), #Dragonite 
                (150, [6, 13, 15]), #Mewtwo

                # johto 152-251 (gen 2) (GL)

                
                (153, [3, 15, 15]), #Bayleef
                (154, [0, 10, 15]), #Meganium
                (156, [0, 13, 15]), #Quilava
                (157, [0, 15, 13]), #Typhlosion
                (158, [15, 15, 15]), #Totodile
                (159, [0, 13, 15]), #Croconaw
                (160, [0, 11, 13]), #Feraligatr
                (166, [13, 15, 15]), #Ledian
                (169, [0, 15, 12]), #Crobat
                (178, [0, 13, 15]), #Xatu
                (180, [0, 15, 14]), #Flaaffy
                (182, [1, 14, 14]), #Bellossom
                (185, [0, 14, 11]), #Sudowoodo
                (186, [0, 15, 11]), #Politoed
                (189, [0, 14, 14]), #Jumpluff
                (190, [14, 15, 14]), #Aipom
                (195, [0, 15, 14]), #Quagsire
                (198, [0, 15, 14]), #Murkrow
                (199, [0, 13, 15]), #Slowking
                (200, [1, 15, 15]), #Misdreavus
                (202, [15, 15, 15]), #Wobbuffet
                (203, [0, 15, 12]), #Girafarig
                (204, [15, 15, 15]), #Pineco
                (205, [0, 9, 15]), #Forretress
                (207, [0,15,12]), # Gligar
                (208, [0, 14, 15]), #Steelix
                (209, [15, 15, 15]), #Snubbull
                (210, [0, 15, 15]), #Granbull
                (212, [1, 15, 15]), #Scizor
                (215, [1, 15, 14]), #Sneasel
                (216, [15, 15, 14]), #Teddiursa
                (217, [0, 14, 15]), #Ursaring
                (221, [0, 15, 10]), #Piloswine
                (227, [0, 15, 14]), #Skarmory
                (228, [15, 15, 15]), #Houndour
                (229, [0, 13, 13]), #Houndoom
                (230, [0, 15, 13]), #Kingdra
                (231, [15, 15, 15]), #Phanpy
                (233, [0, 12, 15]), #Porygon2
                (234, [0, 11, 15]), #Stantler
                (237, [0, 14, 15]), #Hitmontop
                (243, [6, 11, 12]), #Raikou
                (244, [6, 9, 13]), #Entei
                (245, [6, 15, 14]), #Suicune
                (246, [0, 14, 14]), #Pupitar
                (247, [0, 15, 15]), #Tyranitar
                (249, [4, 14, 15]), #Lugia
                (250, [8, 14, 15]), #Ho-Oh


                 #hoenn 252-386 (gen 3) (GL)
                (251, [6, 10, 13]), #Lugia
                (253, [0, 15, 14]), #Grovyle
                (254, [0, 12, 15]), #Sceptile
                (256, [0, 15, 14]), #Combusken
                (257, [1, 15, 15]), #Blaziken
                (259, [0, 14, 15]), #Marshtomp
                (260, [0, 14, 14]), #Swampert
                (262, [0, 12, 14]), #Mightyena
                (274, [15, 15, 15]), #Nuzleaf
                (275, [0, 14, 11]), #Shiftry
                (282, [0, 15, 15]), #Gardevoir
                (294, [15, 15, 15]), #Loudred
                (295, [0, 15, 10]), #Exploud
                (297, [0, 14, 14]), #Hariyama
                (302, [0, 15, 15]), #Sableye
                (303, [1, 15, 15]), #Mawile
                (305, [0, 14, 15]), #Lairon
                (306, [0, 14, 12]), #Aggron
                (310, [0, 15, 15]), #Manectric
                (319, [0, 15, 15]), #Sharpedo
                (320, [0, 15, 15]), #Wailmer
                (321, [0, 15, 15]), #Wailord
                (323, [0, 14, 13]), #Camerupt
                (325, [15, 15, 15]), #Spoink
                (326, [1, 14, 15]), #Grumpig
                (328, [15, 15, 15]), #Trapinch
                (329, [15, 15, 15]), #Vibrava
                (330, [0, 15, 9]), #Flygon
                (332, [0, 14, 15]), #Cacturne
                (340, [0, 14, 13]), #Whiscash
                (341, [15, 15, 15]), #Corphish
                (342, [2, 15, 14]), #Crawdaunt
                (345, [15, 15, 15]), #Lileep
                (346, [0, 15, 15]), #Cradily
                (347, [0, 15, 15]), #Anorith
                (348, [0, 9, 15]), #Armaldo
                (354, [0, 14, 15]), #Banette
                (356, [0, 11, 15]), #Dusclops
                (359, [0, 15, 15]), #Absol
                (362, [0, 13, 13]), #Glalie
                (364, [0, 15, 14]), #Sealeo
                (365, [0, 12, 15]), #Walrein
                (372, [1, 15, 14]), #Shelgon
                (373, [0, 10, 14]), #Salamence
                (375, [0, 13, 15]), #Metang
                (376, [2, 15, 15]), #Metagross
                (377, [8, 14, 14]), #Regirock
                (378, [8, 14, 14]), #Regice
                (379, [6, 11, 13]), #Registeel
                (380, [7, 15, 14]), #Latias
                (381, [6, 13, 9]), #Latios
                (382, [11, 15, 13]), #Kyogre
                (383, [11, 15, 13]), #Groudon

                 #Sinnoh 387-492 (gen 4) (GL)

                 
                (387, [15, 15, 15]), #Turtwig
                (388, [0, 15, 11]), #Grotle
                (389, [0, 11, 13]), #Torterra
                (391, [0, 15, 14]), #Monferno
                (392, [0, 13, 15]), #Infernape
                (393, [15, 15, 15]), #Piplup
                (394, [0, 15, 14]), #Prinplup
                (395, [0, 13, 15]), #Empoleon
                (397, [15, 15, 15]), #Staravia
                (398, [0, 13, 13]), #Staraptor
                (400, [0, 14, 13]), #Bibarel
                (404, [0, 15, 15]), #Luxio
                (405, [0, 15, 12]), #Luxray
                (409, [1, 14, 8]), #Rampardos
                (411, [0, 15, 14]), #Bastiodon
                (424, [0, 13, 14]), #Ambipom
                (425, [15, 15, 15]), #Drifloon
                (426, [0, 15, 12]), #Drifblim
                (429, [0, 15, 15]), #Mismagius
                (430, [0, 15, 15]), #Honchkrow
                (432, [0, 12, 15]), #Purugly
                (434, [15, 15, 15]), #Stunky
                (435, [0, 15, 15]), #Skuntank
                (444, [0, 15, 14]), #Gabite
                (445, [0, 15, 15]), #Garchomp
                (449, [13, 15, 14]), #Hippopotas
                (450, [0, 14, 10]), #Hippowdon
                (451, [15, 15, 15]), #Skorupi
                (452, [2, 15, 14]), #Drapion
                (454, [1, 15, 15]), #Toxicroak
                (459, [15, 15, 15]), #Snover
                (460, [0, 15, 15]), #Abomasnow
                (461, [0, 15, 15]), #Weavile
                (462, [0, 13, 15]), #Magnezone
                (464, [0, 14, 14]), #Rhyperior
                (465, [1, 15, 15]), #Tangrowth
                (466, [1, 15, 15]), #Electivire
                (467, [0, 10, 15]), #Magmortar
                (472, [1, 15, 14]), #Gliscor
                (473, [0, 15, 7]), #Mamoswine
                (474, [1, 15, 13]), #Porygon-Z
                (475, [0, 15, 15]), #Gallade
                (476, [0, 15, 15]), #Probopas
                (477, [0, 14, 13]), #Dusknoir
                (478, [0, 15, 15]), #Froslas
                (486, [6, 13, 15]), #Regigigas

                 #Unova 494-649 (gen 5) (GL)
                (505, [0, 15, 15]), #Watchog
                (510, [0, 15, 14]), #Liepard
                (520, [2, 15, 15]), #Tranquill
                (521, [0, 15, 14]), #Unfezant
                (523, [0, 15, 9,]), #Zebstrika
                (529, [10, 15, 15]), #Drilbur
                (530, [2, 15, 15]), #Excadrill
                (538, [2, 15, 15]), #Throh
                (539, [0, 15, 15]), #Sawk
                (555, [0, 15, 11]), #Darmanitan
                (557, [15, 15, 15]), #Dwebble
                (558, [0, 13, 13]), #Crustle
                (575, [0, 15, 14]), #Gothorita
                (576, [0, 15, 15]), #Gothitelle
                (577, [9, 15, 15]), #Solosis
                (578, [0, 15, 13]), #Duosion
                (579, [2, 15, 15]), #Reuniclus
                (581, [1, 15, 15]), #Swanna
                (591, [0, 14, 15]), #Amoonguss
                (596, [0, 15, 15]), #Galvantula
                (597, [15, 15, 15]), #Ferroseed
                (598, [0, 13, 13]), #Ferrothorn
                (608, [0, 15, 14]), #Lampent
                (609, [0, 15, 14]), #Chandelure
                (622, [15, 15, 15]), #Golett
                (623, [2, 15, 14]), #Golurk      
            ], 
            "little": [
                # kanto 1-151 (gen 1) (LC)
                (1,[0,11,15]),#Bulbasaur
                (2,[0,10,15]),#Ivysaur
                (3,[3,15,14]),#Venusaur
                (4,[0,15,11]),#Charmander
                (5,[1,15,15]),#Charmeleon
                (6,[6,15,15]),#Charizard
                (7,[0,15,14]), #Squirtle
                (8,[0,12,10]), #Wartortle
                (9,[0,15,7]),#Blastoise
                (13,[13,15,15]), #Weedle
                (14,[15,15,15]), #Kakuna
                (15,[0,12,13]), #Beedrill
                (19,[1,15,15]), #Rattata
                (20,[0,15,12]), #Raticate
                (23,[0,14,15]), #Ekans
                (24,[0,14,14]), #Arbok
                (27,[0,10,14]), #Sandshrew
                (28,[0,15,11]), #Sandslash (ALOLAN)
                (28,[3,14,14]), #Sandslash 
                (29,[0,13,14]), #Nidoran Female
                (30,[1,15,14]), #Nidorina
                (31,[0,12,4]), #Nidoqueen
                (32,[0,15,12]), # Nidoran Male
                (33,[0,14,15]), #Nidorino
                (34,[0,14,14]), #Nidoking
                (37,[0,15,14]), #Vulpix
                (38,[0,8,14]), #Ninetails (ALOLAN)
                (38,[0,13,14]), #Ninetails
                (41,[0,15,15]), #Zubat
                (42,[4,15,14]), #Golbat
                (43,[0,15,13]), #Oddish
                (44,[0,15,13]), #Gloom
                (45,[0,14,15]), #Vileplume
                (48,[0,15,15]), #Venonat
                (49,[4,15,14]), #Venomoth
                (50,[0,15,13]), #Diglett (Alolan)
                (50,[1,15,13]), #Diglett
                (51,[0,15,13]), #Dugtrio (Alolan)
                (51,[0,11,12]), #Dugtrio
                (52,[1,15,14]), #Meowth
                (53,[0,15,12]), #Persian
                (54,[0,12,15]), #Psyduck
                (55,[0,11,10]), #Golduck
                (58,[0,10,15]), #Growlithe
                (59,[0,8,14]), #Arcanine
                (60,[0,13,15]), #Poliwag
                (61,[0,11,14]), #Poliwhirl
                (62,[0,14,14]), #Poliwrath
                (63,[1,15,14]), #Abra
                (64,[4,15,13]), #Kadabra
                (65,[0,0,15]), #Alakazam
                (66,[2,15,14]), #Machop
                (67,[0,15,10]), #Machoke
                (68,[0,7,11]), #Machamp
                (69,[0,15,11]), #Bellsprout
                (70,[0,13,13]), #Weepinbell
                (71,[0,14,8]), #Victreebel
                (72,[0,15,14]), #Tentacool
                (73,[1,14,13]), #Tentacruel 
                (74,[1,15,14]), #Geodude (Alolan)
                (74,[1,15,14]), #Geodude
                (75,[1,15,15]), #Graveler (Alolan)
                (75,[1,15,15]), #Graveler
                (76,[3,15,13]), #Golem (Alolan)
                (76,[3,15,13]), #Golem
                (79,[2,15,14]), #Slowpoke
                (80,[3,15,14]), #Slowbro
                (81,[1,15,14]), #Magnemite
                (82,[5,15,15]), #Magneton
                (88,[1,15,15]), #Grimer (Alolan)
                (88,[1,15,15]), #Grimer
                (89,[1,15,14]), #Muk (Alolan)
                (89,[1,15,14]), #Muk
                (90,[0,12,15]), #Shellder
                (91,[2,14,15]), #Cloyster
                (92,[0,14,15]), #Gastly
                (93,[2,15,14]), #Haunter 
                (95,[0,15,11]), #Onix
                (96,[0,12,13]), #Drowzee
                (97,[0,11,9]), #Hypno
                (100,[0,12,14]), #Voltorb
                (101,[4,14,13]), #Electrode 
                (102,[0,15,15]), #Exeggcute
                (103,[0,12,11]), #Exeggutor (Alolan)
                (103,[0,14,8]), #Exeggutor
                (104,[0,15,15]), #Cubone
                (105,[1,15,14]), #Marowak (Alolan) / Marowak
                (106,[0,13,12]), #Hitmonlee
                (107,[5,15,15]), #Hitmonchan 
                (109,[0,15,11]), #Koffing
                (110,[0,15,10]), #Weezing
                (111,[0,13,9]), #Rhyhorn
                (112,[4,15,15]), #Rhydon
                (114,[2,15,13]), #Tangela
                (116,[0,15,15]), #Horsea
                (117,[2,15,15]), #Seadra
                (123,[2,15,15]), #Scyther
                (125,[5,15,14]), #Electabuzz
                (126,[0,15,13]), #Magmar
                (127,[1,15,13]), #Pinsir
                (129,[15,15,15]), #Magikarp
                (130,[12,15,13]), #Gyarados
                (131,[0,12,10]), #Lapras
                (137,[3,15,14]), #Porygon
                (138,[0,14,14]), #Omanyte
                (139,[0,13,12]), #Omastar
                (142,[0,15,8]), #Aerodactyl
                (143,[3,15,14]), #Snorlax
                (147,[0,15,15]), #Dratini
                (148,[0,13,9]), #Dragonair
                (149,[9,15,15]), #Dragonite
                (150,[15,15,15]), #Mewtwo

                
                # Johto 152-248 (gen 2) (LC)
                
                (152,[0,14,13]), #Chikorita
                (153,[0,15,15]), #Bayleef
                (154,[1,15,14]), #Meganium
                (155,[0,15,11]), #Cyndaquil
                (156,[1,15,15]), #Quilava
                (157,[6,15,15]), #Typhlosion
                (158,[0,15,14]), #Totodile
                (159,[3,15,14]), #Croconaw
                (160,[0,1,14]), #Feraligatr
                (165,[0,15,15]), #Ledyba
                (166,[0,11,15]), #Ledian
                (169,[0,6,12]), #Crobat
                (177,[1,15,15]), #Natu
                (178,[0,13,5]), #Xatu
                (179,[0,15,15]), #Mareep
                (180,[0,12,11]), #Flaaffy
                (181,[0,7,8]), #Ampharos
                (182,[0,14,13]), #Bellossom
                (185,[0,13,14]), #Sudowoodo
                (186,[0,14,9]), #Politoed
                (187,[0,15,14]), #Hoppip
                (188,[0,14,15]), #Skiploom
                (189,[1,15,14]), #Jumpluff
                (190,[0,14,14]), #Aipom
                (194,[0,15,15]), #Wooper
                (195,[0,5,14]), #Quagsire
                (198,[3,15,14]), #Murkrow
                (199,[3,15,14]), #Slowking
                (200,[0,13,14]), #Misdreavus
                (202,[0,15,9]), #Wobbuffet
                (203,[0,14,8]), #Girafarig
                (204,[0,15,15]), #Pineco
                (205,[0,15,14]), #Forretress
                (207,[0,12,15]), #Gligar
                (208,[2,15,15]), #Steelix
                (209,[0,12,14]), #Snubbull
                (210,[0,15,14]), #Granbull
                (212,[0,11,13]), #Scizor
                (213,[15,15,15]), #Shuckle
                (215,[0,11,10]), #Sneasel (Hisuian) and #Sneasel
                (216,[0,15,15]), #Teddiursa
                (217,[1,15,14]), #Ursaring
                (220,[0,15,15]), #Swinub
                (221,[4,15,15]), #Piloswine
                (225,[0,13,15]), #Delibird
                (227,[3,15,15]), #Skarmory
                (228,[0,15,15]), #Houndour
                (229,[0,10,7]), #Houndoom
                (230,[0,3,15]), #Kingdra
                (231,[0,15,15]), #Phanpy
                (232,[0,13,11]), #Donphan
                (233,[4,15,14]), #Porygon2
                (234,[0,11,11]), #Stantler
                (237,[0,15,11]), #Hitmontop
                (246,[0,15,15]), #Larvitar
                (247,[0,15,11]), #Pupitar
                (248,[7,15,14]), #Tyranitar


                #Hoenn 248-387 (gen 3) (LC)
                (252,[1,15,15]), #Treecko
                (253,[0,15,12]), #Grovyle
                (254,[0,15,12]), #Sceptile
                (255,[0,13,15]), #Torchic
                (256,[1,15,15]), #Combusken
                (257,[0,9,5]), #Blaziken
                (258,[0,14,14]), #Mudkip
                (259,[0,13,11]), #Marshtomp
                (260,[0,15,15]), #Swampert
                (261,[0,15,14]), #Poochyena
                (262,[0,12,15]), #Mightyena
                (273,[0,15,15]), #Seedot
                (274,[0,15,12]), #Nuzleaf
                (275,[4,15,15]), #Shiftry
                (280,[1,15,15]), #Ralts
                (281,[0,14,15]), #Kirlia
                (282,[0,9,4]), #Gardevoir
                (293,[0,15,13]), #Whismur
                (294,[0,15,6]), #Loudred
                (295,[5,15,14]), #Exploud
                (296,[0,14,13]), #Makuhita
                (297,[0,13,2]), #Hariyama
                (299,[0,14,14]), #Nosepass
                (302,[2,14,15]), #Sableye
                (303,[0,13,10]), #Mawile
                (304,[1,14,14]), #Aron 
                (305,[0,11,13]), #Lairon
                (306,[0,15,13]), #Aggron
                (309,[0,14,14]), #Electrike
                (310,[3,15,15]), #Manectric
                (318,[1,15,15]), #Carvanha
                (319,[4,15,14]), #Sharpedo
                (320,[0,12,15]), #Wailmer
                (321,[0,14,12]), #Wailord
                (322,[1,15,15]), #Numel
                (323,[4,15,15]), #Camerupt
                (325,[0,12,12]), #Spoink
                (326,[4,15,13]), #Grumpig
                (328,[0,15,15]), #Trapinch
                (329,[0,15,13]), #Vibrava
                (330,[0,8,6]), #Flygon
                (331,[0,15,14]), #Cacnea
                (332,[7,15,15]), #Cacturne
                (339,[0,15,13]), #Barboach
                (340,[0,11,11]), #Whiscash
                (341,[0,14,12]), #Corphish
                (342,[6,15,15]), #Crawdaunt
                (345,[0,15,15]), #Lileep
                (346,[0,6,13]), #Cradily
                (347,[0,14,14]), #Anorith
                (348,[0,7,8]), #Armaldo
                (353,[1,15,14]), #Shuppet
                (354,[0,9,11]), #Bantte
                (355,[0,15,15]), #Duskull
                (356,[0,14,12]), #Dusclops
                (359,[0,15,15]), #Absol
                (361,[0,15,13]), #Snorunt
                (362,[4,14,13]), #Glalie
                (363,[0,15,15]), #Spheal
                (364,[0,14,10]), #Sealeo
                (365,[4,15,13]), #Walrein
                (371,[0,15,12]), #Bagon
                (372,[0,11,15]), #Shelgon
                (373,[12,15,15]), #Salamence
                (374,[0,12,14]), #Beldum
                (375,[0,8,15]), #Metang
                (376,[10,15,14]), #Metagross
                (380,[6,11,13]), #Latias
                (381,[8,15,14]), #Latios
                (382,[15,15,15]), #Kyogre
                


                #Sinnoh 387-492 (gen 4) (LC)
                (387,[0,10,14]), #Turtwig
                (388,[4,15,11]), #Grotle
                (389,[4,15,14]), #Torterra
                (390,[0,13,14]), #Chimchar
                (391,[0,11,12]), #Monferno
                (392,[4,15,15]), #Infernape
                (393,[0,14,15]), #Piplup
                (394,[0,14,11]), #Prinplup
                (395,[5,15,15]), #Empoleon
                (396,[0,14,12]), #Starly
                (397,[0,15,13]), #Staravia
                (398,[0,5,14]), #Staraptor
                (399,[0,15,13]), #Bidoof
                (400,[0,15,15]), #Bibarel
                (403,[0,15,15]), #Shinx
                (404,[0,14,14]), #Luxio
                (405,[6,15,14]), #Luxray
                (408,[0,12,14]), #Cranidos
                (409,[0,10,9]), #Rampardos
                (410,[0,11,13]), #Shieldon
                (411,[0,14,8]), #Bastiodon
                (424,[0,11,14]), #Ambipom
                (425,[0,15,15]), #Drifloon
                (426,[2,15,14]), #Drifblim
                (429,[0,13,8]), #Mismagius
                (430,[2,15,13]), #Honchkrow
                (431,[0,14,14]), #Glameow
                (432,[0,9,13]), #Purugly
                (434,[0,11,14]), #Stunky
                (435,[4,15,13]), #Skuntank
                (443,[0,11,15]), #Gible 
                (444,[3,15,14]), #Gabite
                (445,[0,13,13]), #Garchomp
                (449,[0,15,14]), #Hippopotas
                (450,[0,2,15]), #Hippowdon
                (451,[1,15,14]), #Skorupi
                (452,[0,10,12]), #Drapion
                (453,[0,13,15]), #Croagunk
                (454,[5,15,15]), #Toxicroak
                (459,[1,14,15]), #Snover
                (460,[3,15,15]), #Abomasnow
                (461,[0,13,10]), #Weavile
                (462,[1,15,15]), #Magnezone
                (464,[0,3,4]), #Rhyperior
                (465,[0,12,11]), #Tangrowth
                (466,[0,7,7]), #Electivire
                (467,[8,15,13]), #Magmortar
                (472,[6,15,14]), #Gliscor
                (473,[0,13,1]), #Mamoswine
                (474,[0,12,11]), #Porygon-Z
                (475,[0,9,4]), #Gallade
                (476,[0,11,13]), #Probopass
                (477,[2,15,14]), #Dusknoir

                #Unova 494-649 (gen 5) (UL)

                (478,[0,12,13]), #Froslass
                (504,[0,15,15]), #Patrat
                (505,[0,15,15]), #Watchog
                (509,[0,14,13]), #Purrloin
                (510,[0,10,14]), #Liepard
                (522,[0,15,13]), #Blitzle
                (523,[0,12,11]), #Zebstrika
                (529,[0,15,14]), #Drilbur
                (530,[0,14,11]), #Excadrill 
                (538,[2,15,14]), #Throh
                (539,[0,14,8]), #Sawk
                (557,[1,15,15]), #Dwebble
                (558,[3,15,13]), #Crustle
                (580,[0,15,15]), #Ducklett
                (581,[2,15,15]), #Swanna
                (590,[1,15,14]), #Foongus
                (591,[0,15,15]), #Amoonguss
                (595,[0,15,14]), #Joltik
                (596,[3,15,14]), #Galvantula
                (597,[1,15,12]), #Ferroseed
                (598,[0,10,12]), #Ferrothorn
                (607,[0,15,12]), #Litwick
                (608,[2,15,15]), #Lampent
                (609,[1,15,7]), #Chandelure
                (622,[0,14,15]), #Golett
                (623,[0,3,13]), #Golurk
            ]
            }
        self.selected_league = None

    def initUI(self):
        self.setWindowTitle('GRUNT PARSER')
        self.setGeometry(100, 100, 400, 300)

        self.command_input = QLineEdit(placeholderText='Enter Dex Numbers')
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

        self.how_to_use_button = QPushButton('How to Use?')  
        self.how_to_use_button.clicked.connect(self.open_how_to_use_dialog)  

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
        main_layout.addWidget(self.how_to_use_button)

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
        commands = self.command_input.text().split(';')
        results_set = set()

        for command_segment in commands:
            try:
                
                if ',' in command_segment:
                    pokemon_ids = map(int, command_segment.strip().split(','))
                    if not self.selected_league:
                        raise ValueError("Please select a league first.")
                    league_name = self.selected_league.lower()
                    league_data = self.league_data[league_name]
                    for pokemon_id in pokemon_ids:
                        matching_entries = [(entry[0], entry[1]) for entry in league_data if entry[0] == pokemon_id]
                        if matching_entries:
                            result_str = '\n'.join(f"{pokemon_id},{','.join(map(str, stats))}" for pokemon_id, stats in matching_entries)
                            results_set.add(result_str)
                else:
                    command_parts = command_segment.strip().split('-')
                    if len(command_parts) == 2: 
                        range_start, range_end = map(int, command_parts)
                        if range_start < 1 or range_end > 9999 or range_start > range_end:
                            raise ValueError("Invalid range. Please provide a valid range between 1 and 9999.")
                        if not self.selected_league:
                            raise ValueError("Please select a league first.")
                        league_name = self.selected_league.lower()
                        league_data = self.league_data[league_name]
                        matching_entries = [(entry[0], entry[1]) for entry in league_data if range_start <= entry[0] <= range_end]
                        if matching_entries:
                            result_str = '\n'.join(f"{pokemon_id},{','.join(map(str, stats))}" for pokemon_id, stats in matching_entries)
                            results_set.add(result_str)
                    elif len(command_parts) == 1:  
                        pokemon_id = int(command_parts[0])
                        if not self.selected_league:
                            raise ValueError("Please select a league first.")
                        league_name = self.selected_league.lower()
                        league_data = self.league_data[league_name]
                        matching_entries = [(entry[0], entry[1]) for entry in league_data if entry[0] == pokemon_id]
                        if matching_entries:
                            result_str = '\n'.join(f"{pokemon_id},{','.join(map(str, stats))}" for pokemon_id, stats in matching_entries)
                            results_set.add(result_str)
            except ValueError as e:
                results_set.add(f"Invalid command: {str(e)}")

        current_text = self.console.toPlainText().strip()  
        if current_text:
            new_text = current_text + '\n' + '\n'.join(results_set)
        else:
            new_text = '\n'.join(results_set)
        self.console.setPlainText(new_text)



    def open_how_to_use_dialog(self):
        dialog = HowToUseDialog(self)
        dialog.exec_()



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
    app_icon = QIcon('pgtool_icon.ico')  
    app.setWindowIcon(app_icon) 
    stats_input_app = StatsInputApp()
    stats_input_app.show()
    sys.exit(app.exec_())
