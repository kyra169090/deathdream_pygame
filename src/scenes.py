import pygame
from objects import GameObject
from slots_n_boxes import Slot, Box, Node

class GameState:
    def __init__(self):
        self.all_papers_collected = False
        self.paper1_collected = False
        self.paper2_collected = False
        self.paper3_collected = False

game_state = GameState()  # Shared game state

class Start(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=1270, y=650, width=230, height=200, next_scene=None),
            Box(x=0, y=924, width=600, height=100, next_scene=None),
            Box(x=600, y=600, width=200, height=140, next_scene=None)  
        ]
        self.show_dialogue = True

    def render(self, screen, inventory):
        super().render(screen, inventory)
        self.check_dialogue(screen)

    def check_dialogue(self, screen):
        if self.show_dialogue:
            self.render_text(screen, "Where am I?")

    def click_dialogue(self):
        self.show_dialogue = False

# first house
class CityPart1Door(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=700, y=300, width=250, height=650, next_scene=None),
            Box(x=0, y=900, width=400, height=150, next_scene=None)
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)

class CityPart1Corridor(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            #door to living room
            Box(x=970, y=350, width=150, height=220, next_scene=None),
            #door to pantry
            Box(x=700, y=350, width=120, height=400, next_scene=None),
            #going back
            Box(x=600, y=900, width=550, height=150, next_scene=None)            
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)

class CityPart1LivingRoom(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=300, y=930, width=800, height=100, next_scene=None)           
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)

class CityPart1Pantry(Node):
    def __init__(self, background_image, changed_background_image):
        super().__init__(background_image, changed_background_image)
        self.lightbulb_used = False
         # Defining a slot where the lightbulb can be used
        self.slots = [
            Slot(x=10, y=10, width=110, height=120, required_item="Lightbulb", action=self.use_lightbulb)
        ]
        self.boxes = [
            Box(x=0, y=910, width=620, height=110, next_scene=None)
        ]
        self.objects = [
            GameObject(name="Crowbar", image_path="../assets/images/scenes/location1/crowbar.png", x=900, y=780, width=200, height=200, interactable=False)
        ]
        self.lightbulb_sound = pygame.mixer.Sound('../assets/sounds/lightbulb_sound.mp3')

    def use_lightbulb(self):
        # Change the background image to show the lit room
        if not self.lightbulb_used and self.changed_background_image:
            self.lightbulb_sound.play()
            pygame.time.delay(2000)
            self.background_image = self.changed_background_image
            self.lightbulb_used = True

            # Make the crowbar interactable now
            for obj in self.objects:
                if obj.name == "Crowbar":
                    obj.interactable = True

    def render(self, screen, inventory):
        super().render(screen, inventory)


# way to the shop
class CityPart2(Node):
    def __init__(self, background_image, game_state, next_scene):
        super().__init__(background_image)
        self.next_scene = next_scene
        self.boxes = [
            Box(x=100, y=924, width=1000, height=100, next_scene=None),
            Box(x=810, y=615, width=180, height=150, next_scene=None)  
        ]
        self.game_state = game_state
        self.new_box = None

    def render(self, screen, inventory):
        super().render(screen, inventory)
        if self.game_state.all_papers_collected and not self.new_box:
            self.new_box = Box(x=560, y=420, width=200, height=300, next_scene=self.next_scene)
            self.boxes.append(self.new_box)

# inside the shop
class CityPart2Shop(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=300, y=920, width=800, height=120, next_scene=None),
            Box(x=890, y=315, width=170, height=300, next_scene=None)
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)

# Shelf in the shop
class CityPart2ShopShelf(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=200, y=900, width=1250, height=150, next_scene=None)
        ]
        self.objects = [
            GameObject(name="Lightbulb", image_path="../assets/images/scenes/location2/lightbulb.png", x=1005, y=453, width=235, height=277)
        ]

    def render(self, screen, inventory):
        super().render(screen, inventory)

# way to the creepy house with locked door
class CityPart3(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=500, y=900, width=950, height=150, next_scene=None),
            Box(x=860, y=600, width=200, height=150, next_scene=None)  
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)


# creepy house with locked door
class CityPart3Door(Node):
    def __init__(self, background_image, next_scene):
        super().__init__(background_image)
        self.isOpen = False
        self.next_scene = next_scene
        self.slots = [
            Slot(x=920, y=480, width=270, height=430, required_item="Crowbar", action=self.use_crowbar)
        ]
        self.boxes = [
            Box(x=300, y=960, width=1180, height=64, next_scene=None)
        ]
        self.new_box = None
        self.door_crowbar_sound = pygame.mixer.Sound('../assets/sounds/door_with_crowbar.mp3')

    def use_crowbar(self):
        # you can enter house after using the crowbar
        if not self.isOpen:
            self.door_crowbar_sound.play()
            pygame.time.delay(1000)
            self.isOpen = True
            self.add_new_box()


    def add_new_box(self):
        # Add the new box and set its next scene
        if self.isOpen and not self.new_box:
            self.new_box = Box(x=920, y=480, width=270, height=430, next_scene=self.next_scene)
            self.boxes.append(self.new_box)

    def render(self, screen, inventory):
        # If the door is open, add the extra box
        if self.isOpen and not self.new_box:
            self.add_new_box()
        super().render(screen, inventory)

# creepy house corridor
class CityPart3Corridor(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=400, y=900, width=900, height=100, next_scene=None),
            Box(x=900, y=400, width=200, height=200, next_scene=None),
            Box(x=600, y=400, width=200, height=400, next_scene=None)
        ]

    def render(self, screen, inventory):
        super().render(screen, inventory)

# creepy house last room
class CityPart3Room(Node):
    def __init__(self, background_image, changed_background_image, next_scene):
        super().__init__(background_image, changed_background_image)
        self.ceiling_broken = False
        self.next_scene = next_scene  # Store the next scene
        self.slots = [
            Slot(x=900, y=130, width=110, height=120, required_item="Crowbar", action=self.break_ceiling)
        ]
        self.boxes = [
            Box(x=0, y=950, width=850, height=70, next_scene=None)
        ]
        self.breathing_sound = pygame.mixer.Sound('../assets/sounds/citypart3room/breathing_sound.mp3')
        self.break_sound = pygame.mixer.Sound('../assets/sounds/break_sound.mp3')

        # Flag to check if breathing sound has been played already
        self.breathing_sound_played = False

    def break_ceiling(self):
        # Changing the background image
        if not self.ceiling_broken and self.changed_background_image:
            self.break_sound.play()
            self.background_image = self.changed_background_image
            self.add_new_box()
            self.add_new_item_to_screen()
            self.ceiling_broken = True

    def add_new_box(self):
        # Add the new box and set its next scene
        self.new_box = Box(x=900, y=850, width=150, height=80, next_scene=self.next_scene)
        self.boxes.append(self.new_box)

    def add_new_item_to_screen(self):
        # Add the new box and set its next scene
        self.new_item = GameObject(name="Key", image_path="../assets/images/scenes/location3/key.png", x=840, y=920, width=75, height=25)
        self.objects.append(self.new_item)

    def render(self, screen, inventory):
        super().render(screen, inventory)
        # Play the breathing sound only once when the player first enters
        if not self.breathing_sound_played:
            self.breathing_sound.play()
            self.breathing_sound_played = True

class CityPart3RoomLetter(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=0, y=0, width=300, height=1024, next_scene=None),
            Box(x=1300, y=0, width=200, height=1024, next_scene=None)
        ]
        self.paper_sound = pygame.mixer.Sound('../assets/sounds/paper_collect.mp3')
        self.paper_sound_played = False

    def render(self, screen, inventory):
        super().render(screen, inventory)
        if not self.paper_sound_played:
            self.paper_sound.play()
            self.paper_sound_played = True


class CityPart3CorridorWardrobe(Node):
    def __init__(self, background_image, changed_background_image, game_state, next_scene1, next_scene2, next_scene3):
        super().__init__(background_image, changed_background_image)
        self.key_used = False
        self.next_scene1 = next_scene1
        self.next_scene2 = next_scene2
        self.next_scene3 = next_scene3
        self.slots = [
            Slot(x=700, y=600, width=100, height=150, required_item="Key", action=self.use_key)
        ]
        self.boxes = [
            Box(x=0, y=920, width=1500, height=104, next_scene=None)
        ]
        self.new_box = None
        self.unlocking_sound = pygame.mixer.Sound('../assets/sounds/unlocking.mp3')
        self.game_state = game_state
        self.show_dialogue = False
        self.dialogue_is_clicked = False

    def use_key(self):
        # Change the background image to show the lit room
        if not self.key_used and self.changed_background_image:
            self.unlocking_sound.play()
            pygame.time.delay(1000)
            self.background_image = self.changed_background_image
            self.add_new_boxes()
            self.key_used = True

    def add_new_boxes(self):
        # Add the new box and set its next scene
        self.new_box1 = Box(x=355, y=795, width=180, height=100, next_scene=self.next_scene1)
        self.new_box2 = Box(x=655, y=790, width=180, height=100, next_scene=self.next_scene2)
        self.new_box3 = Box(x=1040, y=620, width=180, height=100, next_scene=self.next_scene3)
        self.boxes.append(self.new_box1)
        self.boxes.append(self.new_box2)
        self.boxes.append(self.new_box3)

    def render(self, screen, inventory):
        super().render(screen, inventory)
        if self.game_state.paper1_collected and self.game_state.paper2_collected and self.game_state.paper3_collected:
            self.game_state.all_papers_collected = True
            if not self.dialogue_is_clicked:
                self.show_dialogue = True
                self.check_dialogue(screen)

    def check_dialogue(self, screen):
        if self.show_dialogue:
            self.render_text(screen, "I had enough, this house is scaring me! I want to leave this place, now!")

    def click_dialogue(self):
        if self.game_state.all_papers_collected:
            self.show_dialogue = False
            self.dialogue_is_clicked = True

class CityPart3Photo1(Node):
    def __init__(self, background_image, game_state):
        super().__init__(background_image)
        self.boxes = [
            Box(x=0, y=0, width=1500, height=1024, next_scene=None)
        ]
        self.paper_sound = pygame.mixer.Sound('../assets/sounds/paper_collect.mp3')
        self.paper_sound_played = False
        self.game_state = game_state

    def render(self, screen, inventory):
        super().render(screen, inventory)
        if not self.paper_sound_played:
            self.paper_sound.play()
            self.paper_sound_played = True
            self.game_state.paper1_collected = True


class CityPart3Photo2(Node):
    def __init__(self, background_image, game_state):
        super().__init__(background_image)
        self.boxes = [
            Box(x=0, y=0, width=1500, height=1024, next_scene=None)
        ]
        self.paper_sound = pygame.mixer.Sound('../assets/sounds/paper_collect.mp3')
        self.paper_sound_played = False
        self.game_state = game_state

    def render(self, screen, inventory):
        super().render(screen, inventory)
        if not self.paper_sound_played:
            self.paper_sound.play()
            self.paper_sound_played = True
            self.game_state.paper2_collected = True


class CityPart3CorridorWardrobeLetter(Node):
    def __init__(self, background_image, game_state):
        super().__init__(background_image)
        self.boxes = [
            Box(x=0, y=0, width=1500, height=1024, next_scene=None)
        ]
        self.paper_sound = pygame.mixer.Sound('../assets/sounds/paper_collect.mp3')
        self.paper_sound_played = False
        self.game_state = game_state

    def render(self, screen, inventory):
        super().render(screen, inventory)
        if not self.paper_sound_played:
            self.paper_sound.play()
            self.paper_sound_played = True
            self.game_state.paper3_collected = True

class CityPart4Street1(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=1000, y=620, width=240, height=160, next_scene=None)
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)

class CityPart4Street2(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=1200, y=520, width=300, height=160, next_scene=None)
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)

class CityPart4Street3(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=750, y=620, width=240, height=160, next_scene=None)
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)

class CityPart4FamilyHouse(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=1180, y=580, width=300, height=200, next_scene=None)
        ]
        self.show_dialogue = True

    def render(self, screen, inventory):
        super().render(screen, inventory)
        self.check_dialogue(screen)

    def check_dialogue(self, screen):
        if self.show_dialogue:
            self.render_text(screen, "I know this place.... I grew up in this house... but I could not recognize the street at all?!")

    def click_dialogue(self):
        self.show_dialogue = False

class CityPart4FamilyHouseYard(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=480, y=370, width=150, height=300, next_scene=None)
        ]
        self.objects = [
            GameObject(name="Shovel", image_path="../assets/images/scenes/location4/shovel.png", x=900, y=850, width=200, height=74)
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)


class CityPart4FamilyHouseFirstRoom(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=520, y=280, width=280, height=500, next_scene=None),
            Box(x=1120, y=290, width=200, height=500, next_scene=None),
            Box(x=0, y=920, width=1500, height=104, next_scene=None)
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)

class CityPart4FamilyHouseSecondRoom(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=410, y=280, width=190, height=300, next_scene=None),
            Box(x=1200, y=880, width=300, height=200, next_scene=None)
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)

class CityPart4FamilyHouseThirdRoom(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=1100, y=880, width=300, height=200, next_scene=None)
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)

class CityPart4FamilyHouseBasement(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=610, y=280, width=300, height=200, next_scene=None),
            Box(x=0, y=900, width=1000, height=124, next_scene=None)
        ]
        self.show_dialogue = True

    def render(self, screen, inventory):
        super().render(screen, inventory)
        self.check_dialogue(screen)

    def check_dialogue(self, screen):
        if self.show_dialogue:
            self.render_text(screen,"What the heck is this? We never had a basement.")

    def click_dialogue(self):
        self.show_dialogue = False

class CityPart4FamilyHouseBasement2(Node):
    def __init__(self, background_image, changed_background_image, next_scene):
        super().__init__(background_image, changed_background_image)
        self.shovel_used = False
        self.next_scene = next_scene
        self.slots = [
            Slot(x=500, y=770, width=400, height=140, required_item="Shovel", action=self.use_shovel)
        ]
        self.boxes = [
            Box(x=230, y=350, width=300, height=200, next_scene=None),
            Box(x=0, y=930, width=1500, height=94, next_scene=None)
        ]
        self.new_box = None
        self.digging_sound = pygame.mixer.Sound('../assets/sounds/citypart4room/digging.mp3')

    def use_shovel(self):
        # Change the background image to show the lit room
        if not self.shovel_used and self.changed_background_image:
            self.digging_sound.play()
            pygame.time.delay(4000)
            self.background_image = self.changed_background_image
            self.add_new_box()
            self.shovel_used = True

    def add_new_box(self):
        # Add the new box and set its next scene
        pygame.time.delay(2500)
        self.new_box = Box(x=650, y=770, width=200, height=150, next_scene=self.next_scene)
        self.boxes.append(self.new_box)

    def render(self, screen, inventory):
        super().render(screen, inventory)

class CityPart4FamilyHouseBasement3(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=450, y=370, width=300, height=200, next_scene=None),
            Box(x=950, y=700, width=150, height=120, next_scene=None)
        ]
        self.show_dialogue = True

    def render(self, screen, inventory):
        super().render(screen, inventory)
        self.check_dialogue(screen)

    def check_dialogue(self, screen):
        if self.show_dialogue:
            self.render_text(screen,
                             "Why are these desks and benches here? It looks like a secret place for a gathering")

    def click_dialogue(self):
        self.show_dialogue = False

class CityPart4FamilyHouseBasement3Letter(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=0, y=0, width=1500, height=1024, next_scene=None)
        ]
        self.paper_sound = pygame.mixer.Sound('../assets/sounds/paper_collect.mp3')
        self.paper_sound_played = False

    def render(self, screen, inventory):
        super().render(screen, inventory)
        if not self.paper_sound_played:
            self.paper_sound.play()
            self.paper_sound_played = True

class CityPart4FamilyHoleInTheGround(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=0, y=924, width=1500, height=100, next_scene=None),
            Box(x=265, y=320, width=600, height=450, next_scene=None)
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)

class CityPart4Cave1(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=265, y=320, width=600, height=380, next_scene=None),
            Box(x=850, y=840, width=200, height=120, next_scene=None)
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)


class CityPart4Cave1Letter(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=0, y=0, width=1500, height=1024, next_scene=None)
        ]
        self.paper_sound = pygame.mixer.Sound('../assets/sounds/paper_collect.mp3')
        self.paper_sound_played = False

    def render(self, screen, inventory):
        super().render(screen, inventory)
        if not self.paper_sound_played:
            self.paper_sound.play()
            self.paper_sound_played = True


class CityPart4Cave2(Node):
    def __init__(self, background_image, next_scene):
        super().__init__(background_image)
        self.doom_sound_played = False
        self.doom_sound = pygame.mixer.Sound('../assets/sounds/citypart4room/doom.mp3')
        self.flicker_duration = 2000
        self.flicker_interval = 30  # Time between flickers in ms
        self.flicker_start_time = None
        self.darkness_timer = None
        self.flicker_enabled = True
        self.next_scene = next_scene

    def render(self, screen, inventory):
        super().render(screen, inventory)

        # Initial sound and flicker start delay
        if not self.doom_sound_played:
            self.doom_sound.play()
            self.doom_sound_played = True
            self.flicker_start_time = pygame.time.get_ticks() + 1000  # Delay of 1000 ms before flickering starts

        current_time = pygame.time.get_ticks()

        # Flickering effect
        if self.flicker_enabled and current_time >= self.flicker_start_time:
            if current_time - self.flicker_start_time < self.flicker_duration:
                if (current_time // self.flicker_interval) % 2 == 0:
                    screen.blit(self.background_image, (0, 0))
                else:
                    screen.fill((0, 0, 0))  # Flicker to black
            else:
                self.flicker_enabled = False
                self.darkness_timer = pygame.time.get_ticks()

        # Transition to pitch black, then switch to next scene after 2 seconds
        elif self.darkness_timer is not None:
            if current_time - self.darkness_timer > 500:
                screen.fill((0, 0, 0))
                if current_time - self.darkness_timer > 4000:  # Wait 4 seconds, then switch to next scene
                    return self.next_scene

class CityPart5Street1(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=50, y=320, width=300, height=400, next_scene=None),
            Box(x=600, y=500, width=350, height=300, next_scene=None),
            Box(x=1150, y=600, width=300, height=300, next_scene=None)
        ]
        self.fade_alpha = 255  # Start fully opaque
        self.fade_duration = 2000  # 2 seconds (2000 milliseconds)
        self.fade_start_time = None

    def render(self, screen, inventory):
        # Capture the fade start time if this is the first frame
        if self.fade_start_time is None:
            self.fade_start_time = pygame.time.get_ticks()

        # Render the scene normally
        super().render(screen, inventory)

        # Calculate how much time has passed since fade started
        elapsed_time = pygame.time.get_ticks() - self.fade_start_time
        fade_progress = min(elapsed_time / self.fade_duration, 1)

        # Update fade_alpha based on progress (0 to 255)
        self.fade_alpha = 255 * (1 - fade_progress)

        # Apply black overlay with decreasing transparency
        if self.fade_alpha > 0:
            black_overlay = pygame.Surface(screen.get_size())
            black_overlay.fill((0, 0, 0))
            black_overlay.set_alpha(self.fade_alpha)
            screen.blit(black_overlay, (0, 0))


class CityPart5Street1Shop(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=0, y=910, width=1500, height=114, next_scene=None)
        ]
        self.objects = [
            GameObject(name="Ladder", image_path="../assets/images/scenes/location5/png/ladder.png", x=280, y=700,
                       width=584, height=205)
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)

class CityPart5Street2(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=0, y=910, width=1500, height=114, next_scene=None),
            Box(x=1000, y=750, width=300, height=250, next_scene=None)
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)

class CityPart5Street3(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=0, y=910, width=1500, height=114, next_scene=None),
            Box(x=600, y=650, width=500, height=200, next_scene=None)
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)

class CityPart5Apartments(Node):
    def __init__(self, background_image, changed_background_image, next_scene):
        super().__init__(background_image, changed_background_image)
        self.ladder_used = False
        self.slots = [
            Slot(x=1000, y=200, width=300, height=400, required_item="Ladder", action=self.use_ladder)
        ]
        self.boxes = [
            Box(x=0, y=910, width=1500, height=114, next_scene=None)
        ]
        self.next_scene = next_scene
        self.new_box = None

    def use_ladder(self):
        # Change the background image to show the lit room
        if not self.ladder_used and self.changed_background_image:
            self.background_image = self.changed_background_image
            self.ladder_used = True
            self.add_new_box()

    def add_new_box(self):
        if self.ladder_used and not self.new_box:
            self.new_box = Box(x=940, y=220, width=270, height=450, next_scene=self.next_scene)
            self.boxes.append(self.new_box)

    def render(self, screen, inventory):
        super().render(screen, inventory)

class CityPart5Apartments2(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=0, y=910, width=1500, height=114, next_scene=None),
            Box(x=1000, y=300, width=300, height=400, next_scene=None)
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)

class CityPart5ApartmentsRoom(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=0, y=910, width=1500, height=114, next_scene=None),
            Box(x=1130, y=430, width=200, height=150, next_scene=None)
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)

class CityPart5ApartmentsRoomSuitcase(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=0, y=910, width=1500, height=114, next_scene=None),
            Box(x=80, y=440, width=200, height=250, next_scene=None)
        ]
        self.objects = [
            GameObject(name="Busticket", image_path="../assets/images/scenes/location5/png/ticket.png", x=540, y=300,
                   width=190, height=150)
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)


class CityPart5ApartmentsTelephone1(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=0, y=910, width=1500, height=114, next_scene=None),
            Box(x=490, y=170, width=550, height=710, next_scene=None)
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)

class CityPart5ApartmentsTelephone2(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            # 5 SMS
            Box(x=950, y=930, width=150, height=150, next_scene=None),
            Box(x=510, y=340, width=540, height=100, next_scene=None),
            Box(x=510, y=445, width=540, height=100, next_scene=None),
            Box(x=510, y=570, width=540, height=100, next_scene=None),
            Box(x=510, y=700, width=540, height=100, next_scene=None),
            Box(x=510, y=810, width=540, height=100, next_scene=None)
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)

class CityPart5ApartmentsSMS1(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=950, y=930, width=150, height=150, next_scene=None)
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)

class CityPart5ApartmentsSMS2(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=950, y=930, width=150, height=150, next_scene=None)
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)

class CityPart5ApartmentsSMS3(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=950, y=930, width=150, height=150, next_scene=None)
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)

class CityPart5ApartmentsSMS4(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=950, y=930, width=150, height=150, next_scene=None)
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)

class CityPart5ApartmentsSMS5(Node):
    def __init__(self, background_image):
        super().__init__(background_image)
        self.boxes = [
            Box(x=950, y=930, width=150, height=150, next_scene=None)
        ]
    def render(self, screen, inventory):
        super().render(screen, inventory)

class CityPart5BusStation(Node):
    def __init__(self, background_image, bus_image_path):
        super().__init__(background_image)
        self.boxes = [
            Box(x=0, y=910, width=1500, height=114, next_scene=None)
        ]
        self.bus_image = pygame.image.load(bus_image_path).convert_alpha()
        self.bus_x = 950
        self.bus_y = 690
        self.fade_alpha = 0  # Alpha value starts at 0 (fully transparent)
        self.fade_speed = 1

    def render(self, screen, inventory):
        super().render(screen, inventory)

        if any(item.name == "Busticket" for item in inventory.items):
            if self.fade_alpha < 255:  # Incrementally increase alpha until fully opaque
                self.fade_alpha += self.fade_speed
                if self.fade_alpha > 255:
                    self.fade_alpha = 255  # Cap at 255

            # Create a copy of the bus image with transparency
            bus_with_alpha = self.bus_image.copy()
            bus_with_alpha.fill((255, 255, 255, self.fade_alpha), special_flags=pygame.BLEND_RGBA_MULT)

            # Blit the bus image onto the screen
            screen.blit(bus_with_alpha, (self.bus_x, self.bus_y))