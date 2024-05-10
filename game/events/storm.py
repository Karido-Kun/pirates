from game import event
from game.player import Player
from game.context import Context
import game.config as config
import random

class Storm(Context, event.Event):
    '''Encounter with a severe storm at sea. Decisions here determine how well the player and their crew handle the situation.'''
    def __init__(self):
        super().__init__()
        self.name = "severe storm"
        self.intensity = random.randint(1, 10)  # Random intensity on a scale of 1 to 10
        self.verbs['navigate'] = self
        self.verbs['reinforce'] = self
        self.verbs['panic'] = self
        self.result = {}
        self.go = False

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "navigate":
            self.go = True
            skill_check = random.randint(1, 10)
            if skill_check <= self.intensity:
                self.result["message"] = "You fail to navigate through the storm successfully."
                damage = self.intensity - skill_check  # More intense the storm, greater the damage
                self.result["damage"] = damage
            else:
                self.result["message"] = "You navigate through the storm successfully with minimal issues."
                self.result["damage"] = 0
        elif verb == "reinforce":
            self.go = True
            preparedness = random.randint(1, 10)
            if preparedness < self.intensity:
                self.result["message"] = "You reinforce but the storm is too strong."
                damage = (self.intensity - preparedness) // 2
                self.result["damage"] = damage
            else:
                self.result["message"] = "You're well prepared and weather the storm safely."
                self.result["damage"] = 0
        elif verb == "panic":
            self.go = True
            self.result["message"] = "Panic ensues and the situation worsens."
            damage = self.intensity + 2  # Panic increases the damage
            self.result["damage"] = damage
        else:
            print("The only sensible options are to navigate, reinforce, or panic.")
            self.go = False

    def process(self, world):
        self.go = False
        self.result = {}
        self.result["newevents"] = [self]
        self.result["message"] = "A storm approaches rapidly, what do you want to do?"

        while not self.go:
            print(f"A storm of intensity {self.intensity} approaches. Your options: navigate, reinforce, or panic.")
            Player.get_interaction([self])

        return self.result

