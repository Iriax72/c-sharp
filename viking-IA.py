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
            while (self.playerA.glory <50) or (self.playerB.glory <50) or (self.playerC.glory <50):
                self.analyse.turn_per_game[-1] += 1
                print("tour numero: ", self.analyse.turn_per_game[-1])
                self.playerA.play_turn()
                self.playerB.play_turn()
                self.playerC.play_turn()

    def reset(self):
        self.analyse.turn_per_game.append(0)
        self.playerA = Player("playerA", self.datas, self)
        self.playerB = Player("playerB", self.datas, self)
        self.playerC = Player("playerC", self.datas, self)

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

        self.technologies = []
        self.possibles_raids = []

        self.buildings_level = {
            "mairie": 1,
            "port": 0,
            "forge": 0,
            "temple": 0,
            "champ": 0
        }
    
    @property
    def prisonnier(self):
        return self._prisonnier
    
    @prisonnier.setter
    def prisonnier(self, value):
        self._prisonnier = value
        if self._prisonnier > self.cheap:
            self._prisonnier = self.cheap
    
    @property
    def improvables_buildings(self):
        return [building for building in self.buildings_level.keys() if self.buildings_level[building] < 4]

    def play_turn(self):
        self.cheap += 1
        if random.randint(1, 3) == 1 and self.improvables_buildings:
            self.build(random.choice(self.improvables_buildings))
        elif random.randint(1, 2) == 1:
            self.raid()
        else:
            self.attaque()
        self.verify_gods()
    
    def verify_gods(self):
        pass

    def raid(self):
        self.possibles_raids = [raid for raid in self.datas.raids if self.test(raid)]
        self.apply_effects(random.choice(self.possibles_raids))

    def build(self, building_key):
        self.buildings_level[building_key] += 1

    def attaque(self):
        oppenents = [player for player in self.game.players if player != self]
        defenseur = random.choice(oppenents)
        self.army -= random.randint(1, 6)
        defenseur.army -= random.randint(1, 6)
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
            
    def test(self, raid):
        if not isinstance(raid.get("glory", 0), tuple) and self.glory + raid.get("glory", 0) < 0:
            return False
        if not isinstance(raid.get("gold", 0), tuple) and self.gold + raid.get("gold", 0) < 0:
            return False
        if not isinstance(raid.get("prisonnier", 0), tuple) and self.prisonnier + raid.get("prisonnier", 0) < 0:
            return False
        if not isinstance(raid.get("army", 0), tuple) and self.army + raid.get("army", 0) < 0:
            return False
        return True
    
    def apply_effects(self, raid):
        chainable = True
        if isinstance(raid.get("gold", 0), tuple) or isinstance(raid.get("glory", 0), tuple) or isinstance(raid.get("prisonnier", 0), tuple) or isinstance(raid.get("army", 0), tuple) or isinstance(raid.get("gold_bonus", 0), tuple):
            return
        while chainable:
            self.glory += raid.get("glory", 0)
            self.gold += raid.get("gold", 0)
            self.prisonnier += raid.get("prisonnier", 0)
            self.army += raid.get("army", 0)
            chainable = raid.get("chainable", False)
            if chainable and random.randint(1, self.datas.chainable_chances) == 1:
                self.gold += raid.get("gold_bonus", 0)
                break
    
    def get_victory(self):
        pass
    
    def get_lose(self):
        pass

    def get_technologie(self):
        self.hand += random.choice(self.datas.technologies)

class Analyse():
    def __init__(self):
        self.turn_per_game = []

class Datas():
    def __init__(self, chainable_chances=2):
        self.chainable_chances = chainable_chances
        self.technologies = []
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
            {"nv": 4, "gold": -2, "glory": -2, "chainable": True},
            {"nv": 4, "gold": (2, "army")},
            {"nv": 4, "army": (0.25, "army")}
        ]

datas = Datas(2)
analyse = Analyse()
game = Game(datas, analyse)
game.play(1)

# À ajouter:
# - effets de raids tuples
# - lvl up batiments
# - analyse
# - dieux