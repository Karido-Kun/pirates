from game import config, event
from game import  event
import random
from game.combat import Combat
from game.display import announce
from game.items import Item

class Training (event.Event):
    
        def __init__(self):
            self.name = "Training"
    
        def process(self, world):
            result = {}
            result["message"] = "You have completed your training!"
            announce("You are training with your crewmates!")
            result["newevents"] = [self]
            return result
    
class Haki(Item):
    def __init__(self):
        super().__init__("Haki", 1)  # Correct the item name
        self.damage = (50, 500)
        self.skill = "swords"
        self.verb = "attack"
        self.verb2 = "attacks"
        self.description = "A special item that allows the user to increase their combat abilities. It can be used to increase your combat skills."

    def use_item(self, player):
        """Use the item to increase player's combat abilities."""
        if player.skill_level[self.skill] < 100:
            player.skill_level[self.skill] += 10
            if player.skill_level[self.skill] > 100:
                player.skill_level[self.skill] = 100
            announce(f"Your {self.skill} skill has increased! Current level: {player.skill_level[self.skill]}")
        else:
            announce(f"Your {self.skill} skill is already at its maximum level!")

        player.attack_damage = (
            player.attack_damage[0] + self.damage[0],
            player.attack_damage[1] + self.damage[1]
        )
        announce(f"Your attack damage has increased to {player.attack_damage[0]} - {player.attack_damage[1]}")

class LogPose(Item):
    def __init__(self):
        super().__init__("Log Pose", 1)
        self.description = "A navigation tool that helps you find your way through the Grand Line."

    def use_item(self):
        """Use the item to choose the next destination."""
        announce("The Log Pose allows you to set your next destination.")
        next_location = input("Enter the name of the next location you want to go to: ").strip()
        if self.is_valid_location(next_location):
            config.the_player.set_next_destination(next_location)
        else:
            announce(f"{next_location} is not a valid destination.")

    def is_valid_location(self, location_name):
        # Check if the location name is valid
        possible_destinations = ["Sabaody", "Ohara", "Loguetown", "Arabasta", "Marineford"]
        return location_name in possible_destinations
