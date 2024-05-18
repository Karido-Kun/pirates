from game import event
import random
from game.combat import Combat
from game.combat import Donflamingo
from game.display import announce

class Dofy (event.Event):
    
        def __init__(self):
            self.name = "Donflamingo"
            self.health = 100
    
        def process(self, world):
            result = {}
            result["message"] = "You have defeated Donflamingo and his minions!"
            monsters = []
    
            # Create the leader of the Donflamingo
            leader = Donflamingo("Donflamingo")
            leader.speed = 1.2 * leader.speed
            leader.health = 2 * leader.health
            monsters.append(leader)
            announce("You are attacked by the Donflamingo!")
            Combat(monsters).combat()
            result["newevents"] = [self]
            return result