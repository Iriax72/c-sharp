import random

class Game():
    def __init__(self, datas):
        self.datas = datas
        self.playerA = None
        self.playerB = None
        self.playerC = None

    @property
    def players(self):
        return [self.playerA, self.playerB, self.playerC]

    def play(self, count):
        for game in range(count):
            self.reset()
            while (self.playerA.glory <50) and (self.playerB.glory <50) and (self.playerC.glory <50):
                self.playerA.play_turn()
                self.playerB.play_turn()
                self.playerC.play_turn()

    def reset(self):
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
        self.prisonnier = 0
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
    
    def play_turn(self):
        if random.randint(1, 3) == 1:
            self.raid()
        elif random.randint(1, 2) == 1:
            #build
            pass
        else:
            self.attaque()
        self.verify_gods()
    
    def verify_gods(self):
        pass

    def raid(self):
        self.possibles_raids = [raid for raid in self.datas.raids if self.test(raid)]
        self.apply_effects(random.choice(self.possibles_raids))
    
    def attaque(self):
        defenseur = random.choice(self.game.players.remove(self.name))
        self.army -= random.randint(1,6)
        defenseur.army -= random.randint(1,6)
        if self.army > defenseur.army:
            if random.randint(1,2) == 1:
                self.get_victory()
            else:
                defenseur.get_lose()
        elif self.army < defenseur.army:
            if random.randint(1.2) == 1:
                self.get_lose()
            else:
                defenseur.get_victory()
            
    def test(self, raid):
        if self.glory + raid.get("glory", 0) < 0:
            return False
        if self.gold + raid.get("gold", 0) < 0:
            return False
        if self.prisonnier + raid.get("prisonnier", 0) < 0:
            return False
        if self.army + raid.get("army", 0) < 0:
            return False
        return True
    
    def apply_effects(self, raid):
        chainable = True
        while chainable:
            self.glory += raid.get("glory", 0)
            self.gold += raid.get("gold", 0)
            self.prisonnier += raid.get("prisonnier", 0)
            self.army += raid.get("army", 0)
            chainable = raid.get("chainable", False)
            if chainable and random.randint(1, self.datas.chainable_chances) == 1:
                break
    
    def get_victory(self):
        pass
    
    def get_lose(self):
        pass

    def get_technologie(self):
        self.hand += random.choice(self.datas.technologies)

class Analyse():
    pass

class Datas():
    def __init__(self, chainable_chances=2):
        self.chainable_chances = chainable_chances
        self.technologies = []
        self.raids = []
        self.victory_cards = []
        self.lose_cards = [
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {},
            {}
        ]

datas = Datas(2)
game = Game(datas)
game.play(100)

# À ajouter:
# - effets de raids tuples
# - lvl up batiments
# - analyse
# - dieux