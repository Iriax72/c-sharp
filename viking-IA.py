import random

class Game():
    def __init__(self, datas, analyse):
        self.datas = datas
        self.analyse = analyse
        self.playerA = None
        self.playerB = None
        self.playerC = None

    @property
    def players(self):
        return [self.playerA, self.playerB, self.playerC]

    def play(self, count):
        for game in range(count):
            self.reset()
            while not(self.playerA.win or self.playerB.win or self.playerC.win):
                self.analyse.turn_per_game[-1] += 1
                print(f"tour numero: {self.analyse.turn_per_game[-1]}, A: {self.playerA.glory}, B: {self.playerB.glory}, C: {self.playerC.glory}")
                self.playerA.play_turn()
                self.playerB.play_turn()
                self.playerC.play_turn()

    def reset(self):
        self.analyse.turn_per_game.append(0)
        self.playerA = Player("playerA", self.datas, self)
        self.playerB = Player("playerB", self.datas, self)
        self.playerC = Player("playerC", self.datas, self)
        self.playerA.get_technologie()
        self.playerB.get_technologie()
        self.playerC.get_technologie()

class Player():
    def __init__(self, name, datas, game):
        self.name = name
        self.datas = datas
        self.game = game

        self.glory = 0
        self.gold = 0
        self._prisonnier = 0
        self.army = 0
        self.cheap = 0
        self.infinite_cheap = False

        self.dieux = []

        self.technologies = []
        self.boost_technologies_x2 = False
        self.army_per_turn = 0
        self.glory_each_fight = 0

        self.buildings_level = {
            "mairie": 1,
            "port": 1,
            "forge": 0,
            "temple": 0,
            "champs": 0
        }

        self.win = False

    @property
    def ressources(self):
        return f"glory: {self.glory}, gold: {self.gold}, cheap: {self.cheap}, prisonniers: {self.prisonnier}, army: {self.army}"
    
    @property
    def prisonnier(self):
        return self._prisonnier
    
    @prisonnier.setter
    def prisonnier(self, value):
        self._prisonnier = value
        if not self.infinite_cheap and self._prisonnier > self.cheap:
            self._prisonnier = self.cheap

    @property
    def possibles_raids(self):
        possibles = []
        for raid in self.datas.raids:
            if self.test_raid(raid):
                possibles.append(raid)
        return possibles

    @property
    def improvables_buildings(self):
        improvables = []
        for building in self.buildings_level.keys():
            if self.buildings_level[building] < 4 and self.test_building(building):
                improvables.append(building)
        return improvables

    def play_turn(self):
        self.cheap += 1
        self.army += self.army_per_turn
        if random.randint(1, 3) == 1 and self.improvables_buildings:
            self.build(random.choice(self.improvables_buildings))
        elif random.randint(1, 2) == 1:
            self.raid()
        else:
            self.attaque()
        self.verify_gods()
        if self.glory >= 50:
            self.win = True
    
    def verify_gods(self):
        pass

    def raid(self):
        self.apply_raid_effects(random.choice(self.possibles_raids))

    def build(self, building):
        self.gold -= self.datas.buildings_cost[building][self.buildings_level[building]].get("gold", 0)
        self.cheap -= self.datas.buildings_cost[building][self.buildings_level[building]].get("cheap", 0)
        self.buildings_level[building] += 1
        self.apply_effects_building(building, self.buildings_level[building])

    def attaque(self):
        oppenents = [player for player in self.game.players if player != self]
        defenseur = random.choice(oppenents)
        self.army -= random.randint(1, 6)
        if self.army < 0:
            self.army = 0
        defenseur.army -= random.randint(1, 6)
        if defenseur.army < 0:
            defenseur.army = 0
        if self.army > defenseur.army:
            if random.randint(1, 2) == 1:
                self.get_victory()
            else:
                defenseur.get_lose()
        elif self.army < defenseur.army:
            if random.randint(1, 2) == 1:
                self.get_lose()
            else:
                defenseur.get_victory()
        if self.glory_each_fight:
            self.glory += 1
            
    def test_raid(self, raid):
        if isinstance(raid.get("glory", 0), tuple):
            if self.glory + self.tuple_effect(raid.get("glory", 0)) < 0:
                return False
        elif self.glory + raid.get("glory", 0) < 0:
            return False
        if isinstance(raid.get("gold", 0), tuple):
            if self.gold + self.tuple_effect(raid.get("gold", 0)) < 0:
                return False
        elif self.gold + raid.get("gold", 0) < 0:
            return False
        if isinstance(raid.get("prisonnier", 0), tuple):
            if self.prisonnier + self.tuple_effect(raid.get("prisonnier", 0)) < 0:
                return False
        elif self.prisonnier + raid.get("prisonnier", 0) < 0:
            return False
        if isinstance(raid.get("army", 0), tuple):
            if self.army + self.tuple_effect(raid.get("army", 0)) < 0:
                return False
        elif self.army + raid.get("army", 0) < 0:
            return False
        return True
    
    
    def test_building(self, building):
        building_cost = self.datas.buildings_cost[building][self.buildings_level[building]]
        if self.gold < building_cost.get("gold", 0):
            return False
        if self.prisonnier < building_cost.get("prisonnier", 0):
            return False
        if self.cheap < building_cost.get("cheap", 0):
            return False
        if building_cost.get("dieu", 0) != 0 and building_cost.get("dieu", 0) not in self.dieux:
            return False
        return True

    def apply_raid_effects(self, raid):
        chainable = True
        if isinstance(raid.get("gold", 0), tuple) or isinstance(raid.get("glory", 0), tuple) or isinstance(raid.get("prisonnier", 0), tuple) or isinstance(raid.get("army", 0), tuple) or isinstance(raid.get("gold_bonus", 0), tuple):
            return #faut gérer ca !!!
        while chainable:
            if not(isinstance(raid.get("gold", 0), tuple)):
                self.glory += raid.get("glory", 0)
            else:
                self.glory += self.tuple_effect(raid.get("glory", 0))
            if not(isinstance(raid.get("gold", 0), tuple)):
                self.gold += raid.get("gold", 0)
            else:
                self.gold += self.tuple_effect(raid.get("gold", 0))
            if not(isinstance(raid.get("prisonnier", 0), tuple)):
                self.prisonnier += raid.get("prisonnier", 0)
            else:
                self.prisonnier += self.tuple_effect(raid.get("prisonnier", 0))
            if not(isinstance(raid.get("army", 0), tuple)):
                self.army += raid.get("army", 0)
            else:
                self.army += self.tuple_effect(raid.get("army", 0))
            chainable = raid.get("chainable", False)
            if (chainable and random.randint(1, self.datas.chainable_chances) == 1) or not(self.test_raid(raid)):
                self.gold += raid.get("gold_bonus", 0)
                break
    
    def apply_effects_building(self, building, level):
        effects = self.datas.buildings_effects[building][level-1]
        self.gold += effects.get("gold", 0)
        self.cheap += effects.get("cheap", 0)
        self.army += effects.get("army", 0)
        for i in range(effects.get("technologie", 0)):
            self.get_technologie()
        for i in range(effects.get("grace divine", 0)):
            self.get_grace_divine()
        self.boost_technologies_x2 = effects.get("boost_technologies_x2", False)
        self.glory_each_fight = effects.get("glory_each_fight", False)
        self.army_per_turn = effects.get("army_per_turn", 0)
        self.infinite_cheap = effects.get("infinite_cheap", False)
        self.win = effects.get("win", False)
    
    def tuple_effect(self, tuple_param):
        if tuple_param[1] == "gold":
            return int(tuple_param[0] * self.gold)
        elif tuple_param[1] == "glory":
            return int(tuple_param[0] * self.glory)
        elif tuple_param[1] == "prisonnier":
            return int(tuple_param[0] * self.prisonnier)
        elif tuple_param[1] == "army":
            return int(tuple_param[0] * self.army)

    def get_victory(self):
        pass
    
    def get_lose(self):
        pass

    def get_technologie(self):
        technologies = list(self.datas.technologies)
        self.technologies += random.choice(technologies)
        if self.boost_technologies_x2:
            self.technologies += random.choice(technologies)
        # s'arranger pour supprimer la tchnologie piochée de datas.technologies !!!!!!!!!!!!!!!!!

    def get_grace_divine(self):
        pass

class Analyse():
    def __init__(self):
        self.turn_per_game = []

class Datas():
    def __init__(self, chainable_chances=2):
        self.chainable_chances = chainable_chances
        self.technologies = ["je", "mets", "des", "trucs", "au", "bol", "pour", "pas", "avoir", "d'erreurs"]
        self.lose_cards = []
        self.victory_cards = []
        self.raids = [
            {"nv": 1, "prisonnier": 1},
            {"nv": 1, "glory": 1},
            {"nv": 1, "gold": 3},
            {"nv": 2, "army": -1, "prisonnier": 2},
            {"nv": 2, "prisonnier": -1, "gold": 4},
            {"nv": 2, "army": -1, "gold": 5},
            {"nv": 2, "glory": -1, "prisonnier": 2, "gold": 2},
            {"nv": 2, "army": -1, "gold": 4, "chainable": True},
            {"nv": 2, "gold": (1, "prisonnier")},
            {"nv": 3, "army": -1, "prisonnier": 1, "chainable": True},
            {"nv": 3, "prisonnier": -1, "gold": 2, "chainable": True, "gold_bonus": 1},
            {"nv": 3, "gold": -2, "army": 1, "chainable": True},
            {"nv": 3, "prisonnier": 2},
            {"nv": 3, "gold": -4, "prisonnier": 1, "chainable": True},
            {"nv": 3, "gold": -1, "glory": 2},
            {"nv": 3, "army": -2, "glory": 2, "gold": 1},
            {"nv": 4, "gold": -2, "glory": 2, "chainable": True},
            {"nv": 4, "gold": (2, "army")},
            {"nv": 4, "army": (0.25, "army")}
        ]

        self.buildings_cost = {
            "mairie": [
                {}, 
                {"gold": 5, "prisonnier": 4}, 
                {"gold": 6, "prisonnier": 4}, 
                {"gold": 13, "prisonnier": 5, "dieu": "Odin"}
            ],
            "port": [
                {}, 
                {"gold": 4, "prisonnier": 3},
                {"gold": 6, "prisonnier": 4}, 
                {"gold": 9, "prisonnier": 6, "dieu": "Njord"}
            ],
            "forge": [
                {"gold": 4}, 
                {"gold": 5, "prisonnier": 2}, 
                {"gold": 7, "prisonnier": 2}, 
                {"gold": 10, "prisonnier": 3, "dieu": "Thor"}
            ],
            "temple": [
                {"gold": 3}, 
                {"gold": 3, "cheap": 1}, 
                {"gold": 3, "prisonnier": 4}, 
                {"gold": 5, "prisonnier": 5, "dieu": "Loki"}
            ],
            "champs": [
                {"gold": 5, "prisonnier": 1}, 
                {"gold": 4}, 
                {"gold": 3, "prisonnier": 2}, 
                {"gold": 5, "prisonnier": 3, "dieu": "Freyr"}
            ]
        }

        self.buildings_effects = {
            "mairie": [
                {"technologie": 1}, 
                {"boost_technologies_x2": True}, 
                {"boost_technologies_x2": False, "technologies": 2}, 
                {"win": True}
            ],
            "port": [{}, {}, {}, {}],
            "forge": [
                {"army_per_turn": 1},
                {"army_per_turn": 1, "army": 3},
                {"army_per_turn": 2},
                {"glory_each_fight": True}
            ],
            "temple": [
                {"gold": 2},
                {"technologie": 1},
                {"cheap": 2},
                {"grace_divine": 2}
            ],
            "champs": [
                {"cheap": 1},
                {"cheap": 2},
                {"infinite_cheap": True},
                {}
            ]
        }

datas = Datas(2)
analyse = Analyse()
game = Game(datas, analyse)
game.play(1)

# À ajouter:
# - analyse
# - dieux