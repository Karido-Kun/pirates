from game import location
import game.config as config
from game.display import announce
from game.events import *
from game.items import Item
import random
import numpy
from game import event
from game.combat import Monster
import game.combat as combat
from game.display import menu

class OnePieceIsland(location.Location):

    def __init__(self, x, y, world):
        super().__init__(x, y, world)
        self.name = "OnePieceIsland"
        self.symbol = 'Y'
        self.visitable = True
        self.starting_location = Loguetown (self)
        self.locations = {}

        self.locations["Loguetown"] = self.starting_location
        self.locations["Arabasta"] = Arabasta(self)
        self.locations["Sabaody"] = Sabaody(self)
        self.locations["Dressrosa"] = Dressrosa(self)
        self.locations["Wano"] = Wano(self)

    def enter(self, ship):
        announce("You have arrived at OnePieceIsland.")

    def visit(self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

    def move(self, direction):
        next_location = self.current_location.get_next_location(direction)
        if next_location:
            self.current_location = next_location
            self.current_location.enter()
        else:
            announce("You can't go that way.")

class Loguetown(location.SubLocation):

    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name = "Loguetown"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.verbs["investigate"] = self

    def enter(self):
        announce("Sailing the mysterious Grand Line, you and your crew have found yourselves on an uncharted island.\n" +
             "The Jolly Roger flaps in the wind behind you as the salty air stirs a sense of adventure.\n" +
             "'Yohoho,' you think to yourself, 'there be legends of treasures hidden in these lands. 'Tis worth some explorin', mates!'")

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce("You have returned to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["Arabasta"]
        elif (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["Sabaody"]
        elif (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["Dressrosa"]
        elif (verb == "Central"):
            config.the_player.next_loc = self.main_location.locations[f"{verb}Wano"]


class Dressrosa(location.SubLocation):

    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name ="Dressrosa"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.verbs["investigate"] = self

        self.shrineUsed = False
        self.riddle = "What has keys but can't open locks?"
        self.answer = "piano"

    def enter(self):
        announce("You walk to the top of the hill. A finely-crafted shrine sits before you. You can investigate the shrine.")

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "investigate":
            self.handle_shrine()

    def handle_shrine(self):
        if not self.shrineUsed:
            announce("You investigate the shrine and hear a voice in your head.")
            announce("'I am the guardian of this shrine. Answer my riddle and be rewarded.'")
            choice = input("Answer the riddle? ")
            if "yes" in choice.lower():
                self.handle_riddle()
            else:
                announce("You turn away from the shrine.")
        else:
            announce("The shrine lies dormant.")

    def handle_riddle(self):
        announce(self.riddle)
        choice = input("What is your guess? ")
        self.shrineUsed = True
        if choice.lower() == self.answer:
            self.riddle_reward()
            announce("You have guessed correctly and received the Enma!")
            config.the_player.add_item(Enma())
        else:
            announce("You have guessed incorrectly. The shrine grows silent.")

    def RiddleReward(self):
        for i in config.the_player.get_pirates():
            i.health = i.max_health

    def get_next_location(self, direction):
        if direction in ["north", "east", "south", "west"]:
            return self.main_location.locations["Arabasta Kingdom"]
        else:
            return None

class Wano(location.SubLocation):
    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name = "Wano"
        self.event_chance = 50
        # Assuming Kaido is correctly initialized elsewhere as discussed
        self.events.append(Kaido())

        # Verb to initiate the puzzle game
        self.verbs["play puzzle"] = self.play_number_puzzle

    def enter(self):
        print("You've arrived at Wano. To obtain a treasure, solve the Number Puzzle Game.")
        print("Type 'play puzzle' to start the game.")

    def play_number_puzzle(self):
        print("Welcome to the Number Puzzle Game!")
        target_number = random.randint(1, 100)
        print(f"The number is between 1 and 100.")

        while guess != target_number:
                guess = int(input("Enter your guess: "))
                if guess < target_number:
                    print("Go higher.")
                elif guess > target_number:
                    print("Go lower.")
                else:
                    print("Congratulations! You've solved the puzzle and obtained the treasure.")

class Arabasta(location.SubLocation):
    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name = "Wano"
        self.event_chance = 50
        self.events.append(Kaido())

    def enter(self):
        
        print("You've arrived at the Wano. Solve the Number Puzzle Game to obtain a treasure.")

    def play_number_puzzle(self):
        target_number = random.randint(1, 100)
        print(f"Find the number! It's between 1 and 100.")

        while True:
            guess = int(input("Enter your guess: "))

            if guess < target_number:
                print("Go higher.")
            elif guess > target_number:
                print("Go lower.")
            else:
                print("Congratulations! You've solved the puzzle and obtained the treasure.")
class Sabaody(location.SubLocation):
    def __init__(self, mainLocation):
        super().__init__(mainLocation)
        self.name = "Wano"
        self.event_chance = 50
        self.events.append(Kaido())

    def enter(self):
        
        print("You've arrived at the Wano. Solve the Number Puzzle Game to obtain a treasure.")

    def play_number_puzzle(self):
        target_number = random.randint(1, 100)
        print(f"Find the number! It's between 1 and 100.")

        while True:
            guess = int(input("Enter your guess: "))

            if guess < target_number:
                print("Go higher.")
            elif guess > target_number:
                print("Go lower.")
            else:
                print("Congratulations! You've solved the puzzle and obtained the treasure.")

class Kaido(event.Event, Monster):
    def __init__(self):
        event.Event.__init__(self)  # Correctly initialize Event with no additional arguments
        # Monster attributes initialization
        attacks = {
            "bite": ["bites", random.randrange(60, 80), (5, 15)],
            "slash": ["slashes", random.randrange(60, 80), (5, 15)],
            "Dragon Breath": ["Dragon Breath", random.randrange(60, 80), (5, 15)]
        }
        Monster.__init__(self, "Yonko", random.randint(64, 96), attacks, 100 + random.randint(0, 10))
        # Attributes for combat
        self.cur_move = 0
        self.speed = random.randint(1, 10)

    def process(self, world):
        result = {}
        announce("You encounter Kaido on the roof of the shrine and he transforms into a dragon to attack you.")
        combat.Combat([self]).combat()
        announce("Kaido retreats back to his ship.")
        return result





class Enma(Item):
    def __init__(self):
        super().__init__("Enma", 1)
        self.damage = (50,500)
        self.skill = "swords"
        self.verb = "attack"
        self.verb2 = "attacks"


