from game import config, event
from game import  event
import random
from game.combat import Combat
from game.display import announce


class Ace(event.Event):

    def __init__(self):
        self.name = "Marine Ford War"

    def process(self, world):
        result = {}
        result["message"] = "You have been defeated by the Marine Admirals and couldn't save your brother!"
        announce("You are attacked by the Marine Admirals!")
        result["newevents"] = [self]
        return result
