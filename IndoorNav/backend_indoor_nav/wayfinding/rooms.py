# Notation 
# Floor eg A0
# Quadrant  eg 07

import copy

DIR_1 = 1
DIR_2 = 2
DIR_3 = 3
DIR_4 = 4

NO_ROOM = '-'

""" From which position a room is reachable"""
rooms = {
    ### A0 ### 
    'A0.06': ['A002'],
    'A0.08': ['A004'],
    'A0.09': ['A007'],
    'A0.10': ['A008'],
    'A0.13': ['A010'],
    'A0.14': ['A008'],
    'A0.15': ['A007'],
    'A0.16': ['A006'],
    'A0.17': ['A005'],
    'A0.18': ['A004'],
    'A0.19': ['A002'],
    'A0.20': ['A001'],

    ### A1 ###
    'A1.03': ['A102'],
    'A1.04': ['A103'], #oder A104 (keine Türen engezeichnet
    'A1.05': ['A104'], # oder a105
    'A1.06': ['A106'], 
    'A1.07': ['A107'], #oder a108
    'A1.08': ['A109'], 
    'A1.11': ['A109'],
    'A1.12': ['A108'],
    'A1.13': ['A106'],
    'A1.14': ['A102'], #03 oder 04, keine Türen eingezeichnet
    'A1.15': ['A102'],
    'A1.17': ['A100'],
    'A1.19': ['A100'],

    ### B0 ###
    'B0.02': ['B001'],
    'B0.03': ['B003'],
    'B0.04': ['B005'],
    'B0.05': ['B007'],

    ### C0 ###
    'C0.02': ['C000', 'C004'],
    'C0.05': ['C004'],
    'C0.06': ['C002', 'C004'],
    'cafe': ['C004'],

    ### D0 ###
    'D0.02': ['D003'],
    'D0.03': ['D018'],
    'D0.04': ['D017','D015'],

    ### DU ###
    'DU.04': ['DU00'], #Startup lounge
    'DU.05': ['DU00'],

    ### D1 ###
    'D1.02': ['D116'],
    'D1.03': ['D116'],
    'D1.04': ['D116'],
    'D1.05': ['D116'],
    'D1.06': ['D116'],
    'D1.12': ['D104'],
    'D1.13': ['D105'], # oder 6
    'D1.14': ['D106'], # oder 7
    'D1.15': ['D107'], # oder 8
    'D1.16': ['D109'],
    'D1.17': ['D111'],
    'D1.18': ['D112'], # oder 13 oder 14
    'D1.19': ['D112'], # oder 13 oder 14
    'D1.21': ['D115'],
    'D1.22': ['D107'],

    ### D2 ###
    'D2.03': ['D204'],
    'D2.04': ['D205'],
    'D2.05': ['D206'], # oder 7 oder so
    'D2.08': ['D211'],
    'D2.11': ['D209'],
    'D2.14': ['D203'],
    'D2.18': ['D203','D201'],
    'bib': ['D201'],

    ### E0 ###
    'E0.03': ['E004', 'E005'],
    'E0.04': ['E008'],
    'E0.05': ['E017'],
    'E0.11': ['E017'],
    'E0.14': ['E014'],
    'E0.15': ['E012'],
    'E0.16': ['E011'], #oder 12
    'E0.17': ['E011'],

    ### E1 ###
    'E1.02': ['E104'],
    'E1.03': ['E105'],
    'E1.04': ['E106'],
    'E1.06': ['E106'],
    'E1.07': ['E104'],
    'E1.08': ['E109'],
    'E1.10': ['E109'],
    'E1.11': ['E109'],
    'E1.12': ['E108'],
    'E1.13': ['E107'],
    'E1.19': ['E100'],

    'F0.03': ['F010'],
    'F0.04': ['F017'],
    'F0.05': ['F017'],
    'F0.07': ['F017'],
    'F0.09': ['F002'],
    'F0.10': ['F004'],
    'F0.11': ['F006'],

}

room_to_abbrevation = {
    ### A0 ###
    'A0.06': ['Konferenzraum', 'SR1'],
    'A0.07': ['Kopierraum'],
    'A0.08' : ['ast','tho'], #Andre Stein, Timm Hoffman
    'A0.09': ['Aristoteles', 'SR2'],
    'A0.10.1': ['Agnesi', 'SR3'], 
    'A0.10.2': ['jta'], # Jaime Taboada Aparicio
    'A0.11': ['WC'],
    'A0.12': ['WC'],
    'A0.13': ['Archimedes', 'SR4'],
    'A0.14': ['ot'], # Bettina Otto
    'A0.15': ['fls', 'jpl'], #Florian Schatz, Jan Paul Lüdke
    'A0.16': ['aam'], # Anke Amsel
    'A0.17': ['ens'], #Enja Schmidt
    'A0.18': ['gs'], #Gabi Schümann
    'A0.19': ['eh'], #Eike Harms
    'A0.20': ['abe', 'tha', 'std'], #Anja Behrends, Thurid Harms, Stefanie Einbrodt

    ### A1 ###
    'A1.03': ['fbo'], # Franziska Bönte
    'A1.04': ['gi'], #Giersch
    'A1.05': ['gh'], #Gunnar Harms
    'A1.06': ['afi'], #Alexander Fischer
    'A1.07': ['mvi'], #Markus Vieregge
    'A1.08': ['SmartLab'],
    'A1.09': ['WC'],
    'A1.10': ['WC'],
    'A1.11': ['SmartRoom'],
    'A1.12': ['SmartProject'],
    'A1.13': ['ElektronikLabor'],
    'A1.14': ['InternationalOffice'],
    'A1.15': ['nha'],
    'A1.17': ['Agnodike', 'SR5'],
    'A1.18': ['Mitarbeiterraum'],
    'A1.19': ['web'],

    ### A2 ###
    'A2.03': ['cbu'], #Carsten Burmeister
    'A2.04': ['bos'], #Timm Bostelman
    'A2.05': ['Systeme'],
    'A2.06': ['Ampere', 'SR6'],
    'A2.07': ['WC'],
    'A2.08': ['WC'],
    'A2.09': ['Tematik'],
    'A2.10': ['EmbeddedSystems'],
    'A2.11': ['CAELab'],
    'A2.13': ['saw'], #Sergei Sawitzki
    'A2.14': ['Schaltungstechnik'],
    'A2.16': ['Platinenfertigung'],
    'A2.18': ['hgl'], #Hendrik Glowatzki
    'A2.19': ['Optiklabor'],
    'A2.21': ['ann'], #Hendrik Annuth


    ### B0 ###
    'B0.02': ['nte'],
    'B0.03': ['Bassi', 'SR7'],
    'B0.04': ['fko'], # Fikret Koyuncu
    'B0.05': ['asta'],

    ### C0 ###
    'C0.02': ['HS1'],
    'C0.05': ['PC1'],
    'C0.06': ['HS2'],
    'cafe': ['Cafeteria'],

    ### D0 ###
    'D0.02': ['Daimler', 'SR8'],
    'D0.03': ['HS3'],
    'D0.04': ['HS4'],
    'DU.04': ['hsa', 'cmu', 'mho', 'cre'],
    'DU.05': ['DaVinci', 'SR9'],

    ### D1 ###
    'D1.02': ['Fertigungstechnik'],
    'D1.03': ['Doudna'],
    'D1.04': ['Technik'],
    'D1.05': ['Technik'],
    'D1.06': ['FertigungstechnischesProjekt'],
    'D1.12': ['gb'], #Gerd Beuster
    'D1.13': ['smt'], #Maik Schmitt 
    'D1.14': ['iw'], #Sebastian Iwanowski
    'D1.15': ['ch'], #Dirk Cholewa
    'D1.16': ['Verfahrenstechnik'],
    'D1.17': ['PhysikalischeTechnik'],
    'D1.18': ['Analytik'],
    'D1.19': ['Analytik'],
    'D1.21': ['krg'], #Michael Krug
    'D1.22': ['Chemielabor'],

    ### D2 ###
    'D2.03': ['aha'], #Haase
    'D2.04': ['pfLabor'], #Was für ein Labor?
    'D2.05': ['pf'], #Michael Pfeifers
    'D2.08': ['EcomMarketing'],

    ### E0 ###
    'E0.03': ['HS6'],
    'E0.04': ['PC2'],
    'E0.05': ['PC3'],
    'E0.11': ['PC4'],
    'E0.14': ['PC5'],
    'E0.15': ['ahr'], #Dirk ahrens
    'E0.16': ['uwo'], #Ulf Wohlenberg
    'E0.17': ['WebAdministration'],

    ### E1 ###
    'E1.02': ['ne', 'kar', 'mhe'], #Lars Neumann, Helga Karafiat, Malte Heinz
    'E1.03': ['hs'], # Andreas Häuslein
    'E1.04': ['klk','uhl'], #Gerit Kaleck, Christian Uhlig
    'E1.06': ['uh'], #Ullrich Hoffmann
    'E1.07': ['Einstein', 'SR12'],
    'E1.08': ['gre'], #Gerrit Remané
    'E1.10': ['dsg'], #Dennis Säring
    'E1.11': ['wol'], #Birger Wolter
    'E1.12': ['mpr'], #Michael Predeschly
    'E1.13': ['bo'], #Christian Arved Bohn
    'E1.19': ['tti'], #Torben Tietgen

    ### F0 ###
    'F0.02': ['kal'], #Ilja Kaleck
    'F0.04': ['Netzwerktechnik'],
    'F0.05': ['kch'], #Thorben Koch
    'F0.07': ['Netzwerkschulungslabor'],
    'F0.09': ['LernbereichA'],
    'F0.10': ['LernbereichB'],
    'F0.11': ['LernbereichC'],
}


class Node:
    ''' Represents a node in the Search Graph, is a position in the hallway'''
    name = ''
    dir1 = None
    dir2 = None
    dir3 = None
    dir4 = None

    def __init__(self, name):
        self.name = name

    def wrap_neighbors_in_list(self, direction):
        '''wraps a single neighbor in a list'''
        return direction if type(direction) == list else [direction]

    def set_neighbors(self, dir1, dir2, dir3, dir4):
        ''' sets all neighbors at once'''
        self.dir1 = self.wrap_neighbors_in_list(dir1)
        self.dir2 = self.wrap_neighbors_in_list(dir2)
        self.dir3 = self.wrap_neighbors_in_list(dir3)
        self.dir4 = self.wrap_neighbors_in_list(dir4)

    def get_neighbors_in_dir(self, direction):
        ''' gets neighbors in the given direction '''
        neighbors = []
        if direction == DIR_1:
            return self.dir1
        if direction == DIR_2:
            return self.dir2
        if direction == DIR_3:
            return self.dir3
        if direction == DIR_4:
            return self.dir4
        return neighbors

    @staticmethod
    def get_nodes_and_directions_as_list(neighbors, direction):
        ''' converts (<neighbors list>, direction)
        to [(neighbor1, dir), (neighbor2, dir)...]'''
        res = []
        if type(neighbors) == list:
            for item in neighbors:
                if item != NO_ROOM:
                    res.append((item, direction))
        elif neighbors != NO_ROOM:
            res.append((neighbors, direction))

        return res

    def get_neighbors_as_list(self):
        ''' gets neighbors as list to iterate over all neighbors at once'''
        res = []
        res = res + self.get_nodes_and_directions_as_list(self.dir1, DIR_1)
        res = res + self.get_nodes_and_directions_as_list(self.dir2, DIR_2)
        res = res + self.get_nodes_and_directions_as_list(self.dir3, DIR_3)
        res = res + self.get_nodes_and_directions_as_list(self.dir4, DIR_4)
        return res


class Room:
    ''' is the leaf of the search tree'''
    name = ''
    dir1 = None
    dir2 = None
    dir3 = None
    dir4 = None

    def __init__(self, name):
        self.name = name

    @staticmethod
    def get_neighbors():
        ''' a room has no neighbors'''
        return []

    @staticmethod
    def get_neighbors_in_dir(_):
        ''' a room has no neighbors since it is the destination'''
        return []

    @staticmethod
    def get_nodes_and_directions_as_list(_1, _2):
        ''' a room has no neighbors since it is the destination'''
        return []

### A0 Nodes ###
a0_nodes = [Node('A000'),
            Node('A001'),
            Node('A002'),
            Node('A003'),
            Node('A004'),
            Node('A005'),
            Node('A006'),
            Node('A007'),
            Node('A008'),
            Node('A009'),
            Node('A010'),
            Node('A011'),
            ]

a0_rooms = [Room('A0.06'),
            Room('A0.07'),
            Room('A0.08'),
            Room('A0.09'),
            Room('A0.10.1'),
            Room('A0.10.2'),
            Room('A0.11'),
            Room('A0.12'),
            Room('A0.13'),
            Room('A0.14'),
            Room('A0.15'),
            Room('A0.16'),
            Room('A0.17'),
            Room('A0.18'),
            Room('A0.19'),
            Room('A0.20')]

a0_nodes[0].set_neighbors('-','A001', '-', '-')
a0_nodes[1].set_neighbors(['B000', 'A1S00'], 'A002', 'A0.20', 'A000')
a0_nodes[2].set_neighbors('A0.06', 'A003', 'A0.19', 'A001')
a0_nodes[3].set_neighbors('-', 'A004', '-', 'A002')
a0_nodes[4].set_neighbors('A0.07', 'A005', 'A0.18', 'A003')
a0_nodes[5].set_neighbors('A0.08', 'A006', 'A0.17', 'A004')
a0_nodes[6].set_neighbors('-', 'A007', 'A0.16', 'A005')
a0_nodes[7].set_neighbors('A0.09', 'A008', 'A0.15', 'A006')
a0_nodes[8].set_neighbors('A0.10.1', 'A009', 'A0.14', 'A007')
a0_nodes[9].set_neighbors('A0.10.2', 'A010', 'A0.13', 'A008')
a0_nodes[10].set_neighbors(['A0.11', 'A0.12'], 'A011', '-', 'A009')
a0_nodes[11].set_neighbors('-', 'F017', '-', 'A010')

### A1 ###

a1_nodes = [
    Node('A100'),
    Node('A101'),
    Node('A102'),
    Node('A103'),
    Node('A104'),
    Node('A105'),
    Node('A106'),
    Node('A107'),
    Node('A108'),
    Node('A109'),
    Node('A110'),
    Node('A1S00')
]

a1_rooms = [
    Room('A1.03'),
    Room('A1.04'),
    Room('A1.05'),
    Room('A1.06'),
    Room('A1.07'),
    Room('A1.08'),
    Room('A1.09'),
    Room('A1.10'),
    Room('A1.11'),
    Room('A1.12'),
    Room('A1.13'),
    Room('A1.14'),
    Room('A1.15'),
    Room('A1.17'),
    Room('A1.18'), #MB Küche
    Room('A1.19'), 
]

a1_nodes[0].set_neighbors('A1.19','A101', 'A1.17', 'A1.18')
a1_nodes[1].set_neighbors(['A1S00', 'A2S00'], 'A102', ['A1.15', 'A1.14'], 'A100')
a1_nodes[2].set_neighbors('A1.03', 'A103', 'A1.13', 'A101')
a1_nodes[3].set_neighbors('-', 'A104', '-', 'A102')
a1_nodes[4].set_neighbors(['A1.04', 'A1.05'], 'A105', '-', 'A103')
a1_nodes[5].set_neighbors('-', 'A106', '-', 'A104')
a1_nodes[6].set_neighbors('A1.06', 'A107', 'A1.13', 'A105')
a1_nodes[7].set_neighbors('A1.07', 'A108', '-', 'A106')
a1_nodes[8].set_neighbors('-', 'A109', 'A1.12', 'A107')
a1_nodes[9].set_neighbors('A1.08', 'A110', 'A1.11', 'A108')
a1_nodes[10].set_neighbors(['A1.08', 'A1.09', 'A1.10'], '-', '-', 'A109')
a1_nodes[11].set_neighbors('-', '-', ['A101', 'A001'], '-')

### A2 ###

a2_nodes = [
    Node('A200'),
    Node('A201'),
    Node('A202'),
    Node('A203'),
    Node('A204'),
    Node('A205'),
    Node('A206'),
    Node('A207'),
    Node('A208'),
    Node('A209'),
    Node('A210'),
    Node('A2S00')
]

a2_rooms = [
    Room('A2.03'),
    Room('A2.04'),
    Room('A2.05'),
    Room('A2.06'),
    Room('A2.07'),
    Room('A2.08'),
    Room('A2.09'),
    Room('A2.10'),
    Room('A2.11'),
    Room('A2.12'),
    Room('A2.13'),
    Room('A2.14'),
    Room('A2.15'),
    Room('A2.16'),
    Room('A2.18'),
    Room('A2.19'),
    Room('A2.20'),
    Room('A2.21'),
]

a2_nodes[0].set_neighbors(['A2.20', 'A2.21'],'A201', ['A2.18', 'A2.19'], '-')
a2_nodes[1].set_neighbors('A2S00', 'A202', ['A2.16', 'A2.14', 'A2.15'], 'A200')
a2_nodes[2].set_neighbors('A2.03', 'A203', '-', 'A201')
a2_nodes[3].set_neighbors('A2.04', 'A204', ['A2.14', 'A2.15'], 'A202')
a2_nodes[4].set_neighbors(['A2.05'], 'A205', 'A2.13', 'A203')
a2_nodes[5].set_neighbors('-', 'A206',[ 'A2.11', 'A2.12'], 'A204')
a2_nodes[6].set_neighbors('-', 'A207', '-', 'A205')
a2_nodes[7].set_neighbors('A2.06', 'A208', '-', 'A206')
a2_nodes[8].set_neighbors('-', 'A209', 'A2.10', 'A207')
a2_nodes[9].set_neighbors('A2.07', 'A210', 'A2.09', 'A208')
a2_nodes[10].set_neighbors('A2.08', '-', '-', 'A209')
a2_nodes[11].set_neighbors('-', '-', ['A201', 'A101'], '-')

### B0 ###

b0_nodes = [
    Node('B000'),
    Node('B001'),
    Node('B002'),
    Node('B003'),
    Node('B004'),
    Node('B005'),
    Node('B006'),
    Node('B007'),
    Node('B008'),
]

b0_rooms = [
    Room('B0.02'),
    Room('B0.03'),
    Room('B0.04'),
    Room('B0.05'),
]

b0_nodes[0].set_neighbors('B001','-', 'A001', '-')
b0_nodes[1].set_neighbors('B002', 'B0.02', 'B000', '-')
b0_nodes[2].set_neighbors('B003', 'B0.03', 'B001', '-')
b0_nodes[3].set_neighbors('B004', '-', 'B002', '-')
b0_nodes[4].set_neighbors('B005', '-', 'B003', '-')
b0_nodes[5].set_neighbors('B006', 'B0.04', 'B004', '-')
b0_nodes[6].set_neighbors('B007', '-', 'B005', '-')
b0_nodes[7].set_neighbors('B008', 'B0.05', 'B006', '-')
b0_nodes[8].set_neighbors('D000', '-', 'B007', '-')

### C0 ###

c0_nodes = [
    Node('C000'),
    Node('C001'),
    Node('C002'),
    Node('C003'),
    Node('C004'),
]

c0_rooms = [
    Room('C0.02'), #HS1
    Room('C0.03'),
    Room('C0.05'),
    Room('C0.06'),
]

c0_nodes[0].set_neighbors('C001','-', 'D000', 'C0.02')
c0_nodes[1].set_neighbors('-', '-', 'C000', 'C002')
c0_nodes[2].set_neighbors('C0.06', 'C001', '-', 'C003')
c0_nodes[3].set_neighbors('-', 'C002', '-', 'C004')
c0_nodes[4].set_neighbors(['C0.05','C0.06'], 'C003', ['C0.02', 'C0.03'], '-')

### DU ###
du_nodes = [
    Node('DU00'),
]

du_rooms = [
    Room('DU.04'),
    Room('DU.05')
]

du_nodes[0].set_neighbors('-', 'D018', 'DU.04', 'DU.05')

### D0 ####

d0_nodes = [
    Node('D000'),
    Node('D001'),
    Node('D002'),
    Node('D003'),
    Node('D004'),
    Node('D005'),
    Node('D006'),
    Node('D007'),
    Node('D008'),
    Node('D009'),
    Node('D010'),
    Node('D011'),
    Node('D012'),
    Node('D013'),
    Node('D014'),
    Node('D015'),
    Node('D016'),
    Node('D017'),
    Node('D018'),
    Node('D019'),
    Node('D020'),
]

d0_rooms = [
    Room('D0.02'),
    Room('D0.03'),
    Room('D0.04'),
]

d0_nodes[0].set_neighbors('C001','D001', '-', '-')
d0_nodes[1].set_neighbors('-', 'D002', '-', 'D000')
d0_nodes[2].set_neighbors('-', 'D003', '-', 'D001')
d0_nodes[3].set_neighbors('D0.02', 'D004', '-', 'D002')
d0_nodes[4].set_neighbors('-', 'D005', '-', 'D003')
d0_nodes[5].set_neighbors('-', 'D006', '-', 'D004')
d0_nodes[6].set_neighbors('-', 'D007', '-', 'D005')
d0_nodes[7].set_neighbors('D017', 'D008', '-', 'D006')
d0_nodes[8].set_neighbors('-', 'D009', '-', 'D007')
d0_nodes[9].set_neighbors('-','D010', 'D1S00', 'D008') #
d0_nodes[10].set_neighbors('-', 'D011', '-', 'D009')
d0_nodes[11].set_neighbors('-', 'D012', '-', 'D010')
d0_nodes[12].set_neighbors('-', 'D013', '-', 'D011')
d0_nodes[13].set_neighbors('-', 'D014', '-', 'D012')
d0_nodes[14].set_neighbors('-', 'D015', 'F000', 'D013')
d0_nodes[15].set_neighbors('D0.04', 'D016', '-', 'D014')
d0_nodes[16].set_neighbors('-', 'E000', '-', 'D015')
d0_nodes[17].set_neighbors('D018', '-', 'D007', '-')
d0_nodes[18].set_neighbors('D019', 'D0.04', 'D017', ['D0.03', 'DU00'])
d0_nodes[19].set_neighbors('D020', '-', 'D018', '-')
d0_nodes[20].set_neighbors('-', '-', 'D019', '-')

### D1 ####

d1_nodes =[
    Node('D100'),
    Node('D101'),
    Node('D102'),
    Node('D103'),
    Node('D104'),
    Node('D105'),
    Node('D106'),
    Node('D107'),
    Node('D108'),
    Node('D109'),
    Node('D110'),
    Node('D111'),
    Node('D112'),
    Node('D113'),
    Node('D114'),
    Node('D115'),
    Node('D116'),
    Node('D117'),
    Node('D118'),
    Node('D119'),
    Node('D1S00'),
    Node('D1S01'),
    Node('D1S02'),
    Node('D1S03'),
]

d1_rooms = [
    Room('D1.02'),
    Room('D1.03'),
    Room('D1.04'),
    Room('D1.05'),
    Room('D1.06'),
    Room('D1.07'),
    Room('D1.09'),
    Room('D1.10'),
    Room('D1.12'),
    Room('D1.13'),
    Room('D1.14'),
    Room('D1.15'),
    Room('D1.16'),
    Room('D1.17'),
    Room('D1.18'),
    Room('D1.19'),
    Room('D1.20'),
    Room('D1.21'),
    Room('D1.22'),
    Room('D1.23'),
]

d1_nodes[0].set_neighbors('D101','-', ['D1S03', 'D2S00'], '-')
d1_nodes[1].set_neighbors('D102', 'D115', 'D100', 'D116')
d1_nodes[2].set_neighbors('D103', '-', 'D101', '-')
d1_nodes[3].set_neighbors(['D1.07', 'D1.09', 'D1.10'], 'D104', 'D102', 'D1.02')
d1_nodes[4].set_neighbors('D1.12', 'D105', '-', 'D103')
d1_nodes[5].set_neighbors('D1.13', 'D106', '-', 'D104')
d1_nodes[6].set_neighbors('-', 'D107', 'D1.22', 'D105')
d1_nodes[7].set_neighbors('D1.14', 'D108', '-', 'D106')
d1_nodes[8].set_neighbors('D1.15', '-', 'D109', 'D107')
d1_nodes[9].set_neighbors('D108','D1.16', 'D110', '-')
d1_nodes[10].set_neighbors('D109','-', 'D111', '-')
d1_nodes[11].set_neighbors('D110','-', 'D1.17', '-')
d1_nodes[12].set_neighbors('D1.23','D111', 'D1.18', 'D113')
d1_nodes[13].set_neighbors('-','D112', 'D1.19', 'D114')
d1_nodes[14].set_neighbors('-','D113', 'D1.20', 'D115')
d1_nodes[15].set_neighbors('D1.22','D114', 'D1.21', 'D101')
d1_nodes[16].set_neighbors('D1.02','D101', 'D1.03', 'D117')
d1_nodes[17].set_neighbors('D1.02','D116', '-', 'D118')
d1_nodes[18].set_neighbors('D1.02','D117', ['D1.04', 'D1.05'], 'D119')
d1_nodes[19].set_neighbors('D1.02','D118', 'D1.06', '-')
d1_nodes[20].set_neighbors('D009','-', 'D1S01', '-')
d1_nodes[21].set_neighbors('D1S00','-', '-', 'D1S02')
d1_nodes[22].set_neighbors('D1S03','D1S01', '-', '-')
d1_nodes[23].set_neighbors('D100','-', 'D1S02', '-')

### D2 ####

d2_nodes =[
    Node('D200'),
    Node('D201'),
    Node('D202'),
    Node('D203'),
    Node('D204'),
    Node('D205'),
    Node('D206'),
    Node('D207'),
    Node('D208'),
    Node('D209'),
    Node('D210'),
    Node('D211'),
    Node('D2S00'),
    Node('D2S01'),
    Node('D2S02'),
]

d2_rooms = [
    Room('D2.03'),
    Room('D2.04'),
    Room('D2.05'),
    Room('D2.06'),
    Room('D2.07'),
    Room('D2.08'),
    Room('D2.09'),
    Room('D2.11'),
    Room('D2.14'),
    Room('D2.15'),
    Room('D2.16'),
    Room('D2.17'),
    Room('D2.18'),
    Room('D2.19')]

d2_nodes[0].set_neighbors('D201','-', 'D2S02', '-') #ist die Treppe hier richtig?
d2_nodes[1].set_neighbors('D202', 'D2.19', 'D200', 'D204')
d2_nodes[2].set_neighbors('D203', '-', 'D201', '-')
d2_nodes[3].set_neighbors(['D2.15', 'D2.16', 'D2.17'], 'D2.18', 'D202', 'D2.14')
d2_nodes[4].set_neighbors('-', 'D201', 'D2.03', 'D205')
d2_nodes[5].set_neighbors('-', 'D204', 'D2.04', 'D206')
d2_nodes[6].set_neighbors('-', 'D205', '-', 'D207')
d2_nodes[7].set_neighbors('-', 'D206', 'D2.05', 'D208')
d2_nodes[8].set_neighbors('-', 'D207', '-',  'D209')
d2_nodes[9].set_neighbors('D210', ['D2.11', 'D208'], '-', ['D2.07', 'D2.06'])
d2_nodes[10].set_neighbors('D211','-', 'D209', '-')
d2_nodes[11].set_neighbors('D2.09','-', 'D210', 'D2.08')
d2_nodes[12].set_neighbors('D100','-', '-', 'D2S01')
d2_nodes[13].set_neighbors('D2S02','D2S00', '-', '-')
d2_nodes[14].set_neighbors('D200','-', 'D2S01', '-')

### E0 ###

e0_nodes =[
    Node('E000'),
    Node('E001'),
    Node('E002'),
    Node('E003'),
    Node('E004'),
    Node('E005'),
    Node('E006'),
    Node('E007'),
    Node('E008'),
    Node('E009'),
    Node('E010'),
    Node('E011'),
    Node('E012'),
    Node('E013'),
    Node('E014'),
    Node('E015'),
    Node('E016'),
    Node('E017'),
    Node('E018'),
]

e0_rooms = [
    Room('E0.03'),
    Room('E0.04'),
    Room('E0.05'),
    Room('E0.11'),
    Room('E0.14'),
    Room('E0.15'),
    Room('E0.16'),
    Room('E0.17'),
    Room('E0.18'),
    Room('E0.19')]
 
e0_nodes[0].set_neighbors('E001','-', 'D016', '-')
e0_nodes[1].set_neighbors('E002', '-', 'E000', '-')
e0_nodes[2].set_neighbors('E003', '-', 'E001', '-')
e0_nodes[3].set_neighbors('E004', 'E005', 'E002', '-')
e0_nodes[4].set_neighbors('E0.03', 'E005', 'E003', '-')
e0_nodes[5].set_neighbors('E0.03', 'E006', 'E003', ['E0.03', 'E004'])
e0_nodes[6].set_neighbors('-', 'E007', '-', 'E005')
e0_nodes[7].set_neighbors('-', 'E008', '-', 'E006')
e0_nodes[8].set_neighbors('E0.04', 'E009', '-', 'E007')
e0_nodes[9].set_neighbors('-','E010', 'E0.19', 'E008')
e0_nodes[10].set_neighbors('-', 'E011', 'E0.18', 'E009')
e0_nodes[11].set_neighbors('-', 'E012', 'E0.17', 'E010')
e0_nodes[12].set_neighbors('-','E013', 'E0.16', 'E011')
e0_nodes[13].set_neighbors('-','E014', 'E0.15', 'E012')
e0_nodes[14].set_neighbors('E015', 'E0.14', '-', 'E013')
e0_nodes[15].set_neighbors('E016', '-', 'E014', '-')
e0_nodes[16].set_neighbors('E017','-', 'E015', '-')
e0_nodes[17].set_neighbors('E018','E0.11', 'E016', 'E0.05')
e0_nodes[18].set_neighbors('-', 'E1S00', 'E017', '-')

### E1 ###

e1_nodes =[
    Node('E100'),
    Node('E101'),
    Node('E102'),
    Node('E103'),
    Node('E104'),
    Node('E105'),
    Node('E106'),
    Node('E107'),
    Node('E108'),
    Node('E109'),
    Node('E1S00'),
    Node('E1S01'),
    Node('E1S02'),
    Node('E1S03'),
]

e1_rooms = [
    Room('E1.02'),
    Room('E1.03'),
    Room('E1.04'),
    Room('E1.06'),
    Room('E1.07'),
    Room('E1.08'),
    Room('E1.10'),
    Room('E1.11'),
    Room('E1.14'),
    Room('E1.15'),
    Room('E1.16'),
    Room('E1.17'),
    Room('E1.18'),
    Room('E1.19')]

e1_nodes[0].set_neighbors('E1S03','E104', 'E101', ['E1.18', 'E1.19'])
e1_nodes[1].set_neighbors('E100', '-', 'E102', '-')
e1_nodes[2].set_neighbors('E101', '-', 'E103', '-')
e1_nodes[3].set_neighbors('E102', 'E007', ['E1.14', 'E1.15', 'E1.16'], 'E1.17')
e1_nodes[4].set_neighbors('E1.02', 'E105', 'E1.07', 'E100')
e1_nodes[5].set_neighbors('E1.03', 'E106', '-', 'E104')
e1_nodes[6].set_neighbors('E1.04', 'E1.05', 'E1.06', 'E105')
e1_nodes[7].set_neighbors('-', 'E108', 'E1.13', 'E103')
e1_nodes[8].set_neighbors('-', 'E109', 'E1.12', 'E107')
e1_nodes[9].set_neighbors('E1.08','E1.09', ['E1.10', 'E1.11'], 'E108')
e1_nodes[10].set_neighbors('E1S01', '-', '-', 'E018')
e1_nodes[11].set_neighbors('-', '-', 'E1S00', 'E1S02')
e1_nodes[12].set_neighbors('-','E1S01', 'E1S03', '-')
e1_nodes[13].set_neighbors('E1S02', '-', 'E100', 'E108')

### F0 ###

f0_nodes =[
    Node('F000'),
    Node('F001'),
    Node('F002'),
    Node('F003'),
    Node('F004'),
    Node('F005'),
    Node('F006'),
    Node('F007'),
    Node('F008'),
    Node('F009'),
    Node('F010'),
    Node('F011'),
    Node('F012'),
    Node('F013'),
    Node('F014'),
    Node('F015'),
    Node('F016'),
    Node('F017'),
]

f0_rooms = [
    Room('F0.02'),
    Room('F0.03'),
    Room('F0.04'),
    Room('F0.05'),
    Room('F0.06'),
    Room('F0.07'),
    Room('F0.09'),
    Room('F0.10'),
    Room('F0.11')]

f0_nodes[0].set_neighbors('D014','-', 'F001', '-')
f0_nodes[1].set_neighbors('F000', '-', 'F002', '-')
f0_nodes[2].set_neighbors('F001', '-', 'F003', 'F0.11')
f0_nodes[3].set_neighbors('F002', '-', 'F004', '-')
f0_nodes[4].set_neighbors('F003', ['F0.02', 'F0.03'], 'F005', '-')
f0_nodes[5].set_neighbors('F004', '-', 'F006', '-')
f0_nodes[6].set_neighbors('F005', '-', 'F007', 'F0.10')
f0_nodes[7].set_neighbors('F006', '-', 'F008', '-')
f0_nodes[8].set_neighbors('F007', '-', 'F009', '-')
f0_nodes[9].set_neighbors('F008', ['F0.05', 'F0.04', 'F0.06'], 'F010', 'F0.09')
f0_nodes[10].set_neighbors('F009', '-', 'F011', '-')
f0_nodes[11].set_neighbors('F010', '-', 'F012', '-')
f0_nodes[12].set_neighbors('F011', '-', 'F013', '-')
f0_nodes[13].set_neighbors('F012', '-', 'F014', '-')
f0_nodes[14].set_neighbors('F013', '-', 'F015', '-')
f0_nodes[15].set_neighbors('F014', '-', 'F016', '-')
f0_nodes[16].set_neighbors('F015', '-', 'F017', '-')
f0_nodes[17].set_neighbors('F016', ['F0.07', 'F0.06'], '-', 'A011')

def get_nodes():
    ''' gets all nodes'''
    res =  a0_nodes + a1_nodes + a2_nodes + b0_nodes + c0_nodes + d0_nodes + d1_nodes + d2_nodes + e0_nodes + e1_nodes + f0_nodes + du_nodes
    return res

def get_rooms():
    ''' geets all rooms'''
    res = a0_rooms + a1_rooms + a2_rooms + b0_rooms + c0_rooms + d0_rooms + d1_rooms + d2_rooms + e0_rooms + e1_rooms + f0_rooms + du_rooms
    return res
