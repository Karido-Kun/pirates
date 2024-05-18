from game import event
import random
from game.combat import Combat
from game.combat import Crocodile
from game.combat import BaroqueWorksAgent
from game.display import announce

import random  # Ensure you have the random module imported if not already done

class BaroqueWorks(event.Event):

    def __init__(self):
        self.name = "Baroque Works Agent"
        self.health = 100

    def process(self, world):
        result = {}
        result["message"] = "You have defeated the Desert King Sir Crocodile and his minions!"
        monsters = []

        # Create the leader of the Baroque Works
        leader = Crocodile("Desert King Sir Crocodile")
        leader.speed = 1.2 * leader.speed
        leader.health = 2 * leader.health
        monsters.append(leader)

        # Determine the number of additional agents
        min_agents = 2
        max_agents = 6
        n_appearing = random.randrange(min_agents, max_agents)
        for n in range(1, n_appearing + 1):
            monsters.append(BaroqueWorksAgent(f"Baroque Works Agent {n}"))

        announce("You are attacked by the members of Baroque Works Organization!")
        Combat(monsters).combat()
        result["newevents"] = [self]
        return result
