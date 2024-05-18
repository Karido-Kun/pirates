from game import location
import game.config as config
from game.display import announce
from game.events import *
from game.events.train import Haki, LogPose
from game.items import Item
import random
import numpy
from game import event
from game.combat import Monster
import game.combat as combat
from game.display import menu



class OnePieceWorld(location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "OnePieceWorld"
        self.symbol = 'O'
        self.visitable = True
        self.starting_location = Loguetown(self)
        self.locations = {}
        self.locations["Loguetown"] = self.starting_location
        self.locations["Arabasta"] = Arabasta(self)
        self.locations["Ohara"] = Ohara(self)
        self.locations["Marineford"] = Marineford(self)
        self.locations["Sabaody"] = Sabaody(self)
        self.locations["Dressrosa"] = Dressrosa(self)
        self.locations["Wano"] = Wano(self)
        

    def enter (self, ship):
        announce("You have arrived at OnePieceWorld.")
        announce("In this world you are a pirate and you are sailing the Grand Line in search of the One Piece treasure.")
    def visit (self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

class Loguetown (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "Loguetown"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.event_chance = 100
        self.events.append(storm.Storm())


    def enter (self):
        announce ("You have arrived at the first island of the Grand Line, Loguetown.")
        announce ("You have docked your ship on the beach and are making your way to the island entrance.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce ("You return to your ship Thousand Sunny.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["Arabasta"]
        else:
            announce ("The entrance of the island is covered in Mist."" You can only choose to go 'north' or 'south'!")

    

class Arabasta(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "Arabasta"
        self.verbs['help'] = self
        self.verbs['info'] = self
        self.event_chance = 100
        self.BaroqueWorks_event = BaroqueWorks.BaroqueWorks()
        self.knows_about_baroque_works = False

    def enter(self):
        announce("You have arrived at the second island of the Grand Line, Arabasta.")
        announce("This island is known for its vast deserts and the Alabasta Kingdom.")

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "south":
            config.the_player.next_loc = self.main_location.locations["Loguetown"]
        elif verb == "north":
            config.the_player.next_loc = self.main_location.locations["Ohara"]
        elif verb == "info":
            announce("You found out that the Baroque Works organization led by one of the Seven Warlords of the Sea, Desert King Sir Crocodile, is planning to take over the kingdom of Alabasta.")
            announce("You have to help the princess of Alabasta, Vivi, to stop Crocodile and save the kingdom.")
            self.knows_about_baroque_works = True
        elif verb == "help":
            if self.knows_about_baroque_works:
                announce("You decided to help the princess of Alabasta, Vivi.")
                announce("You can find them in the desert of Arabasta.")
                # Trigger the event after processing the verb
                self.trigger_event()
            else:
                announce("You need to find out more information about the situation in Alabasta before you can help.")

    def trigger_event(self):
        result = self.BaroqueWorks_event.process(self.main_location)
        announce(result["message"])
        for new_event in result.get("newevents", []):
            self.events.append(new_event)
    
        if "You have defeated the Desert King Sir Crocodile and his minions!" in result["message"]:
            announce("By defeating Crocodile, you have obtained the devil fruit Gumo-Gumo-no Mi! ")
            announce("Gumo-Gumo-no is now added to your inventory. You can use it to attack your enemies.")
            config.the_player.add_to_inventory([Gumo_Gumo_no()])
            config.the_player.next_loc = self.main_location.locations["Ohara"]

        

class Ohara (location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "Ohara"
        self.verbs['read'] = self
        self.tries = 0
        self.solved = False

    def enter (self):
        announce("You have arrived at the third island of the Grand Line, Ohara.")
        announce("This island is known for its vast libraries and scholars.")
        announce("The marine has captured the scholars and you have to save them.")
        announce("To figure out the location of the scholars and save them you have solve the riddle on the Poneglyph.")

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["Arabasta"]
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["Marineford"]
        elif (verb == "read"):
            while self.solved == False:
                print("I stretch and bend, twist and fight,"
                        "A rubber man, in every right."
                        "From a fruit, my power came,"
                        "To be the Pirate King, my aim."

                        "A straw hat sits upon my head,"
                        "With a crew, through seas we tread."
                        "What is my name, known far and wide,"
                        "As I sail the Grand Line's tide?"

                        "What am I?")
                
                print("You can enter the answer to the riddle or ask for a hint ")
                answer = input("What is the answer to the riddle?: ")
                if answer == "Monkey D. Luffy":
                    announce("You have saved the scholars!")
                    announce("By saving the scholars, you have obtained the item Rumble Ball!")
                    config.the_player.add_to_inventory([RumbleBall()])
                    config.the_player.next_loc = self.main_location.locations["Marineford"]
                    self.solved = True
                elif answer == "hint":
                    print("I am a stretchy pirate with a straw hat.")
                elif self.tries >= 2:
                    print("You have gotten it wrong. It was an easy riddle!")
                    config.the_player.gameInProgress = False
                    config.the_player.kill_all_pirates("You have failed to save the scholars! Game Over!")
                self.tries += 1



class Marineford(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "Marineford"
        self.verbs['save'] = self
        self.event_chance = 100
        self.Ace_event = Ace.Ace()

    def enter(self):
        announce("You made it past Ohara! Congratulations.")
        announce("Your brother Ace is set to be executed at Marineford.")
        announce("You have to defeat the Marine Admirals to save your brother.")

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["Ohara"]
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["Sabaody"]
        elif (verb == "save"):
            announce("You decided to save your brother Ace.")
            announce("You can find him at Marineford.")
            # Trigger the event after processing the verb
            self.trigger_event()

    def trigger_event(self):
        result = self.Ace_event.process(self.main_location)
        announce(result["message"])
        for new_event in result.get("newevents", []):
            self.events.append(new_event)

        if "You have been defeated by the Marine Admirals and couldn't save your brother!" in result["message"]:
            announce("You were not strong enough to save your brother Ace. You have failed to save him!")
            announce("You are retreating to Sabaody.")
            config.the_player.next_loc = self.main_location.locations["Sabaody"]

class Sabaody(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "Sabaody"
        self.verbs['train'] = self
        self.event_chance = 100
        self.train_event = train.Training()



    def enter(self):
        announce("You have made it to the Sabaody Archipelago.")
        announce("You Were not able to save your brother Ace. You have to train harder to become stronger.")


    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["Marineford"]
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["Dressrosa"]
        elif (verb == "train"):
            announce("You have decided to train to become stronger.")
            announce("You can find a training room in the Sabaody .")
            # Trigger the event after processing the verb
            self.trigger_event()
    
    def trigger_event(self):
        result = self.train_event.process(self.main_location)
        announce(result["message"])
        for new_event in result.get("newevents", []):
            self.events.append(new_event)

        if "You have completed your training!" in result["message"]:
            announce("While training, you have obtained the item Haki!")
            config.the_player.add_to_inventory([Haki()])
            announce("Haki is now added to your inventory. You can use it to increase your combat abilities.")
            announce("By completing your training, you have obtained Log Pose!")
            announce("Log Pose is now added to your inventory. You can use it to navigate.")
            config.the_player.add_to_inventory([LogPose()])
            config.the_player.next_loc = self.main_location.locations["Dressrosa"]




class Dressrosa(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "Dressrosa"
        self.verbs['help'] = self
        self.verbs['info'] = self
        self.event_chance = 100
        self.toy_event = toys.Dofy()
        self.knows_about_Donquixote_Family = False

    def enter(self):
        announce("You have made it to the Dressrosa.")
        announce("This island is known for its colosseum and the Riku Family.")
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["Sabaody"]
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["Wano"]
        elif (verb == "info"):
            announce("You have found out that the Donquixote Family took over the kingdom of Dressrosa.")
            announce("You have found out that many people are being forced to fight in the colosseum.")
            announce("Many people are being turned into toys by the Donquixote Family.")
            announce("You have to help the Riku Family to stop the Donquixote Family and save the kingdom.")
            self.knows_about_Donquixote_Family = True
        elif (verb == "help"):
            if self.knows_about_Donquixote_Family:
                announce("You decided to help the Riku Family.")
                announce("You can find them in the colosseum of Dressrosa.")
                # Trigger the event after processing the verb
                self.trigger_event()
            else:
                announce("You need to find out more information about the situation in Dressrosa before you can help.")

    def trigger_event(self):
        result = self.toy_event.process(self.main_location)
        announce(result["message"])
        for new_event in result.get("newevents", []):
            self.events.append(new_event)
    
        if "You have defeated Donflamingo and his minions!" in result["message"]:
            announce("By defeating Donflamingo, you have obtained Gear Fourth!")
            announce("Gear Fourth is now added to your inventory. You can use it to increase your combat abilities.")
            config.the_player.add_to_inventory([Gear_Fourth()])
            announce("By defeating Donflamingo, you have also obtained Enma!")
            announce("Enma is now added to your inventory. You can use it to attack your enemies.")
            config.the_player.add_to_inventory([Enma()])
            config.the_player.next_loc = self.main_location.locations["Wano"]
            
#
class Wano(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "Wano"
        self.verbs['help'] = self
        self.verbs['info'] = self
        self.event_chance = 100
        self.Shogun_event = shogun.Shogun()
        self.knows_about_kaido = False

        

    def enter(self):
        announce("You have made it to the Wano Country.")
        announce("This island is known for its samurai and the Kozuki Family.")

    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["Dressrosa"]
        elif (verb == "info"):
            announce("You have found out that the Shogun of Wano has taken over the island with the help of Kaido.")
            announce("You have found out that the Kozuki Family is in danger.")
            announce("You have to defeat the Kaido and Shogun of Wano to save the Kozuki Family and the island.")
            self.knows_about_kaido = True
        elif (verb == "help"):
            if self.knows_about_kaido:
                announce("You decided to help the Kozuki Family.")
                announce("You can find them in the castle of Wano.")
            # Trigger the event after processing the verb
            self.trigger_event()
        
    def trigger_event(self):
        result = self.Shogun_event.process(self.main_location)
        announce(result["message"])
        for new_event in result.get("newevents", []):
            self.events.append(new_event)

        if "You have defeated Kaido and his minions!" in result["message"]:
            announce("By defeating the Kaido of Wano, you have found the One Piece treasure and become the Pirate King!")
            announce("You have completed your journey in the Grand Line.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        






class Gumo_Gumo_no(Item):
    def __init__(self):
        super().__init__("Gumo-Gumo-no", 1)
        self.damage = (40, 400)  # Min and max damage
        self.charges = 2  # Number of uses
        self.skill = "brawling"  # Skill associated with the item
        self.verb = "Kick"  # Singular verb for the action
        self.verb2 = "Kicks"  # Plural verb for the action
        self.cooldown = 3  # Cooldown in turns between uses
        self.critical_chance = 0.1  # 10% chance to deal critical damage
        self.description = "A powerful attack that can deal significant damage with a chance to critically hit."

    def use_item(self, target):
        if self.charges > 0:
            damage_dealt = self.calculate_damage()
            target.take_damage(damage_dealt)
            self.charges -= 1
            announce(f"You use {self.verb} on {target.name}, dealing {damage_dealt} damage.")
            if self.charges == 0:
                announce(f"The {self.name} has been depleted.")
        else:
            announce(f"You have no more charges left for the {self.name}.")

    def calculate_damage(self):
        base_damage = random.randint(*self.damage)
        if random.random() < self.critical_chance:
            critical_multiplier = 2
            announce("Critical hit!")
            return base_damage * critical_multiplier
        return base_damage


class Enma(Item):
    def __init__(self):
        super().__init__("Enma", 1)
        self.damage = (100, 700)  # Increased damage range
        self.skill = "swords"
        self.verb = "slashes"
        self.verb2 = "slashes through"
        self.critical_hit_chance = 0.2  # 20% chance for a critical hit
        self.bleed_effect = True  # Inflicts bleeding

    def attack(self, target):
        damage = random.randint(*self.damage)
        if random.random() < self.critical_hit_chance:
            damage *= 2  # Critical hit doubles the damage
            print(f"Critical hit! {self.verb2} {target} with Enma for {damage} damage!")
        else:
            print(f"{self.verb} {target} with Enma for {damage} damage!")
        
        if self.bleed_effect:
            print(f"{target} is bleeding!")
            target.apply_bleed()  # Assuming target has a method to handle bleeding

        return damage



class RumbleBall(Item):
    def __init__(self):
        super().__init__("Rumble Ball", 1)  # Ensure the name is "Rumble Ball"
        self.use_item()  # Use the item upon creation or change as needed
        self.description = "A special drug that allows the user to increase their health. It can be used to heal pirates in your crew."


    def use_item(self):
        pirates_in_island = config.the_player.pirates
        for pirate in pirates_in_island:
            if 0 < pirate.health <= 50:
                health_increase = random.randint(1, 29)
                new_health = pirate.health + health_increase
                if new_health > 100:
                    new_health = 100  # Ensure health does not exceed 100
                pirate.health = new_health
                announce(f"{pirate.name}'s health increased by {health_increase} and is now {pirate.health}.")
            elif pirate.health > 50 and pirate.health < 100:
                health_increase = random.randint(1, 20)
                new_health = pirate.health + health_increase
                if new_health > 100:
                    new_health = 100  # Ensure health does not exceed 100
                pirate.health = new_health
                announce(f"{pirate.name}'s health increased by {health_increase} and is now {pirate.health}.")
            elif pirate.health >= 100:
                announce(f"{pirate.name}'s health is already at maximum.")

class Gear_Fourth(Item):
    def __init__(self):
        super().__init__("Gear Fourth", 1)
        self.description = "A powerful combat technique that significantly increases your combat abilities."

    def use_item(self, player):
        """Use the item to enhance the player's combat abilities."""
        player.combat_skill += 20  # Example: Increase combat skill by 20
        announce(f"Your combat skill has increased! Current level: {player.combat_skill}")
