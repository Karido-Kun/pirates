from game import event
import random
from game.combat import Combat
from game.combat import Kaido
from game.display import announce

class Shogun (event.Event):

    def __init__(self):
        self.name = "Kaido the Beast pirates"
        self.health = 100

    def process(self, world):
        result = {}
        result["message"] = "You have defeated Kaido and his minions!"
        monsters = []

        # Create the leader of the Shougan
        leader = Kaido("Kaido the Beast pirates")
        leader.speed = 1.2 * leader.speed
        leader.health = 2 * leader.health
        monsters.append(leader)
        announce("You are attacked by the Kaido the Beast pirates!")
        Combat(monsters).combat()
        result["newevents"] = [self]
        return result

   